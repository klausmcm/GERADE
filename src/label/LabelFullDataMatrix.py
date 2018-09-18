import math
import string
import sys
from .LabelComponentText import LabelComponentText
from .LabelComponentBarcodeDataMatrix import LabelComponentBarcodeDataMatrix
from PIL import Image
from PIL import ImageDraw

class LabelFullDataMatrix:
    def __init__(self, text, separator_line_thickness, label_type, dpi=(600, 600)):
        """
        text                     - The text to be encoded and printed on the label. 
        separator_line_thickness - The thickness of the line that will line the label and separates the text from the barcode image.
        label_type               - Determines the layout of the label. One of the below can be chosen.
            0 - Plain data matrix barcode
            1 - Data matrix barcode with text on the barcode
            2 - Data matrix barcode with text on the right side
            3 - Data matrix barcode with text on the right side and rotated
            4 - Data matrix barcode for use with cable ties on cables
        barcode_module_size      - Size of the barcode module in pixels.
        text_font_size           - Size of the text placed on the label.
        """
        
        def get_text_on_label(text, label_type):
            """Format how the text will look on the label.
            
            text       - Text to be placed on the label.
            label_type - One of the types specifying the label layout.
            """
            text_on_label = "".join([c for c in text if c in string.ascii_letters + string.digits])
            if label_type == 0:
                text_on_label = ""
            elif label_type == 1 or label_type == 2 or label_type == 4:
                text_on_label = "\n".join([text_on_label[:4],
                                           text_on_label[4:8],
                                           text_on_label[8:12],
                                           text_on_label[12:]])
            elif label_type == 3:
                text_on_label = "\n".join(["-".join([text_on_label[:4],
                                                     text_on_label[4:8]]),
                                           "-".join([text_on_label[8:12],
                                                     text_on_label[12:]])])
            else:
                text_on_label = ""
            return text_on_label
        
        self.label_image = None
        self.text_on_label = get_text_on_label(text, label_type)
        self.label_type = label_type
        self.separator_line_thickness = separator_line_thickness
        self.dpi = dpi
        
    def set_label(self, size_barcode_module, size_font):
        self._set_label(size_barcode_module, size_font, self.label_type, self.separator_line_thickness)
        
    def set_label_by_barcode_module_size(self, barcode_module_size):
        self._set_label(barcode_module_size, -1, self.label_type, self.separator_line_thickness)
    
    def set_label_by_font_size(self, font_size):
        self._set_label(-1, font_size, self.label_type, self.separator_line_thickness)
    
    def set_label_by_dimensions(self, max_dimensions):
        barcode_module_size = 1
        if max_dimensions[0] == -1: max_dimensions = (sys.maxsize, max_dimensions[1])
        if max_dimensions[1] == -1: max_dimensions = (max_dimensions[0], sys.maxsize)
        while True:
            self._set_label(barcode_module_size, -1, self.label_type, self.separator_line_thickness)
            if self.label_image.size[0] <= max_dimensions[0] and self.label_image.size[1] <= max_dimensions[1]:
                barcode_module_size += 1
            else:
                barcode_module_size -= 1
                break
        self._set_label(barcode_module_size, -1, self.label_type, self.separator_line_thickness)
    
    def _set_label(self, size_barcode_module, size_font, label_type, separator_line_thickness):
        def get_barcode_module_size(size_barcode_module, size_font, text_on_label, label_type):
            """
            """
            #TODO: document
            if size_barcode_module != -1:
                return size_barcode_module
            else:
                text_image = LabelComponentText(text_on_label, size_font).get_image()
                if label_type == 3:
                    text_image = text_image.rotate(90, expand=True)
                module_size = 1
                while True:
                    barcode_image = LabelComponentBarcodeDataMatrix(text_on_label, module_size, quiet_zone_thickness=0).get_image()
                    if (barcode_image.size[0] > text_image.size[0] and
                        barcode_image.size[1] > text_image.size[1]):
                        break
                    else:
                        module_size += 1
                return module_size
        
        def get_font_size(text_on_label, size_font, size_barcode_module, label_type):
            """
            """
            #TODO: document
            if size_font != -1:
                return size_font
            else:
                barcode_image = LabelComponentBarcodeDataMatrix(text_on_label, size_barcode_module, quiet_zone_thickness=0).get_image()
                font_size = -1
                while True:
                    text_image = LabelComponentText(text_on_label, font_size).get_image()
                    if label_type == 3:
                        text_image = text_image.rotate(90, expand=True)
                    if (text_image.size[0] < barcode_image.size[0] and
                        text_image.size[1] < barcode_image.size[1]):
                        font_size += 1
                    else:
                        break
                return max([1, font_size-1])
        
        def calculate_label_dimensions(label_component_barcode, label_component_text, separator_line_thickness, label_type):
            """
            """
            # TODO: document
            image_barcode = label_component_barcode.get_image()
            image_text = label_component_text.get_image()
            if label_type == 0 or label_type == 1:
                width = image_barcode.size[0] + 2*separator_line_thickness
                height = image_barcode.size[1] + 2*separator_line_thickness
            elif label_type == 2 or label_type == 3:
                if label_type == 3:
                    image_text = image_text.rotate(90, expand=True)
                width = image_barcode.size[0] + image_text.size[0] + 3*separator_line_thickness
                height = image_barcode.size[1] + 2*separator_line_thickness
            elif label_type == 4:
                golden_ratio = (1+5**0.5)/2
                width = image_barcode.size[0] + 2*separator_line_thickness
                height = 2*round(golden_ratio*image_barcode.size[1] + separator_line_thickness)
            return (round(width), round(height))
        
        def assemble_components(label_component_barcode, label_component_text, label_dimensions, separator_line_thickness, label_type):
            """
            """
            #TODO: document
            assembled = Image.new("RGB",
                                  label_dimensions,
                                  "white")
            if label_type == 0:
                assembled.paste(label_component_barcode.get_image(),
                                (separator_line_thickness, separator_line_thickness))
            elif label_type == 1:
                assembled.paste(label_component_barcode.get_image(),
                                (separator_line_thickness, separator_line_thickness))
                assembled.paste(label_component_text.get_image(),
                                (round(assembled.size[0]/2 - label_component_text.get_image().size[0]/2),
                                 round(assembled.size[1]/2 - label_component_text.get_image().size[1]/2)),
                                mask=label_component_text.get_image())
            elif label_type == 2 or label_type ==3:
                image_text = label_component_text.get_image()
                image_barcode = label_component_barcode.get_image()
                if label_type == 3:
                    image_text = image_text.rotate(90, expand=True)
                assembled.paste(image_barcode,
                               (separator_line_thickness, separator_line_thickness))
                assembled.paste(image_text,
                                (image_barcode.size[0] + 2*separator_line_thickness,
                                 round(assembled.size[1]/2 - image_text.size[1]/2)),
                                mask=image_text)
            elif label_type == 4:
                image_text = label_component_text.get_image().rotate(180)
                image_barcode = label_component_barcode.get_image()
                height_empty_areas = label_dimensions[1] - 2*separator_line_thickness - 2*image_barcode.size[1]
                circle_diameter = min([88, round(0.5*0.45*height_empty_areas)])
                image_circle = Image.new("RGBA", (circle_diameter, circle_diameter))
                image_circle_draw = ImageDraw.Draw(image_circle)
                image_circle_draw.ellipse([0, 0, circle_diameter-1, circle_diameter-1], fill="white", outline="black")
                image_circle_draw.ellipse([circle_diameter/2 - circle_diameter/(2**2), circle_diameter/2 - circle_diameter/(2**2),
                                           circle_diameter/2 + circle_diameter/(2**2) - 1, circle_diameter/2 + circle_diameter/(2**2) - 1],
                                          fill="white",
                                          outline="black")
                image_circle_draw.ellipse([circle_diameter/2 - circle_diameter/(2**3), circle_diameter/2 - circle_diameter/(2**3),
                                           circle_diameter/2 + circle_diameter/(2**3) - 1, circle_diameter/2 + circle_diameter/(2**3) - 1],
                                          fill="white",
                                          outline="black")
                
                assembled.paste(image_barcode,
                                (separator_line_thickness,
                                 round(label_dimensions[1] - separator_line_thickness - height_empty_areas/2 - image_text.size[1] - image_barcode.size[1] - 1)))
                assembled.paste(image_text,
                                (round(label_dimensions[0]/2 - image_text.size[0]/2),
                                 round(label_dimensions[1] - separator_line_thickness - height_empty_areas/2 - image_text.size[1] - 1)),
                                mask=image_text)
                assembled.paste(image_circle,
                                (round(label_dimensions[0]/2 - image_circle.size[0]/2),
                                 round(separator_line_thickness + height_empty_areas/4 - image_circle.size[1]/2)),
                                mask=image_circle)
            return assembled

        def draw_bounding_lines(label_component_barcode, label_image, separator_line_thickness, label_type):
            """
            """
            # TODO: document
            draw = ImageDraw.Draw(label_image)
            for i in range(separator_line_thickness):
                draw.line([(0, i),
                           (label_image.size[0] - 1, i)],
                          fill="black")
                draw.line([(0, label_image.size[1] - 1 - i),
                           (label_image.size[0] - 1, label_image.size[1] - 1 - i)],
                          fill="black")
                draw.line([(i, 0),
                           (i, label_image.size[1] - 1)],
                           fill="black")
                draw.line([(label_image.size[0] - 1 - i, 0),
                           (label_image.size[0] - 1 - i, label_image.size[1] - 1)],
                          fill="black")
            if label_type == 2 or label_type == 3:
                for i in range(separator_line_thickness):
                    draw.line([(separator_line_thickness + label_component_barcode.get_image().size[0] + i, 0),
                               (separator_line_thickness + label_component_barcode.get_image().size[0] + i, label_image.size[1] - 1)],
                              fill="black")
            else:
                pass
            return label_image

        def draw_corner_trim_lines(label_image, line_width, barcode_padding_thickness, label_type):
            """
            """
            offset = round((math.sqrt(2*math.pow(barcode_padding_thickness, 2)) - barcode_padding_thickness) / math.cos(math.radians(45)))
            draw = ImageDraw.Draw(label_image)
            for i in range(line_width):
                x_start = 0
                x_end = label_image.size[0] - 1
                y_start = 0
                y_end = label_image.size[1] - 1
                
                draw.line([(x_start, offset - i),
                           (offset - i, y_start)],
                          fill="black")
                draw.line([(x_end - offset + i, y_start),
                           (x_end, offset - i)],
                          fill="black")
                draw.line([(x_end, y_end - offset + i),
                           (x_end - offset + i, y_end)],
                          fill="black")
                draw.line([(offset - i, y_end),
                           (x_start, y_end - offset + i)],
                          fill="black")
            if label_type == 4:
                #TODO: implement
                pass
            return label_image
        
        self.size_barcode_module = get_barcode_module_size(size_barcode_module, size_font, self.text_on_label, self.label_type)
        self.size_font = get_font_size(self.text_on_label, size_font, self.size_barcode_module, self.label_type)
        
        if label_type == 4:
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text_on_label, self.size_barcode_module, quiet_zone_thickness=3*self.size_barcode_module)
        else:
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text_on_label, self.size_barcode_module, quiet_zone_thickness=2*self.size_barcode_module)

        if label_type == 1:
            self.component_text = LabelComponentText(self.text_on_label, self.size_font, color="gray")
        else:
            self.component_text = LabelComponentText(self.text_on_label, self.size_font)
            
        if label_type == 4:
            self.component_text.add_white_border(3*self.size_barcode_module)
        else:
            self.component_text.add_white_border(2*self.size_barcode_module)
        
        self.label_dimensions = calculate_label_dimensions(self.component_barcode, self.component_text, separator_line_thickness, label_type)
        self.label_image = assemble_components(self.component_barcode, self.component_text, self.label_dimensions, separator_line_thickness, label_type)
        self.label_image = draw_bounding_lines(self.component_barcode, self.label_image, separator_line_thickness, label_type)
        self.label_image = draw_corner_trim_lines(self.label_image, separator_line_thickness, self.component_barcode.get_border_thickness(), label_type)
        
    def get_image(self):
        return self.label_image
    
    def get_module_size(self):
        return self.size_barcode_module
    
    def get_font_size(self):
        return self.size_font

    def get_border_thickness(self):
        return self.separator_line_thickness

    def save_image_to_file(self, file_path):
        """
        """
        self.label_image.save(file_path, "PNG", dpi=self.dpi)
        return


