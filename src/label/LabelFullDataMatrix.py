import math
import string
from src.label.LabelComponentText import LabelComponentText
from src.label.LabelComponentBarcodeDataMatrix import LabelComponentBarcodeDataMatrix
from PIL import Image
from PIL import ImageDraw



class LabelFullDataMatrix:
    def __init__(self, text, separator_line_thickness, label_type, barcode_module_size=-1, text_font_size=-1):
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
        
        def _get_text_on_label(text, label_type):
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
        
        def _get_barcode_module_size(font_size, text_on_label, label_type):
            """
            """
            #TODO: document
            text_image = LabelComponentText(text_encoded, font_size).get_image()
            if label_type == 3:
                text_image = text_image.rotate(90, expand=True)
            module_size = 1
            while True:
                barcode_image = LabelComponentBarcodeDataMatrix(text_encoded, module_size, whitespace_border_thickness=0).get_image()
                if (barcode_image.size[0] >= text_image.size[0] and
                    barcode_image.size[1] >= text_image.size[1]):
                    break
                else:
                    module_size += 1
            return module_size
        
        def _get_font_size(text_on_label, barcode_module_size, label_type):
            """
            """
            #TODO: document
            barcode_image = LabelComponentBarcodeDataMatrix(text_encoded, barcode_module_size, 0).get_image()
            font_size = -1
            while True:
                text_image = LabelComponentText(text_encoded, font_size).get_image()
                if label_type == 3:
                    text_image = text_image.rotate(90, expand=True)
                if (text_image.size[0] <= barcode_image.size[0] and
                    text_image.size[1] <= barcode_image.size[1]):
                    font_size += 1
                else:
                    break
            return max([1, font_size-1])
        
        def _calculate_label_dimensions(label_component_barcode, label_component_text, separator_line_thickness, label_type):
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
                #TODO: implement
                pass
            return (round(width), round(height))
        
        def _assemble_components(label_component_barcode, label_component_text, label_dimensions, separator_line_thickness):
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
                #TODO: implement - still need the transparent text
                assembled.paste(label_component_barcode.get_image(),
                               (separator_line_thickness, separator_line_thickness))
            elif label_type == 2 or label_type ==3:
                image_text = label_component_text.get_image()
                image_barcode = label_component_barcode.get_image()
                if label_type == 3:
                    image_text = image_text.rotate(90, expand=True)
                assembled.paste(image_barcode,
                               (separator_line_thickness, separator_line_thickness))
                assembled.paste(image_text,
                               (image_barcode.size[0] + 2*separator_line_thickness,
                                round(assembled.size[1]/2 - image_text.size[1]/2)))
            elif label_type == 4:
                pass
            return assembled
        
        def _draw_bounding_lines(label_component_barcode, label_image, separator_line_thickness, label_type):
            """
            """
            # TODO: document
            draw = ImageDraw.Draw(label_image)
            for i in range(separator_line_thickness):
                draw.line([(0, i), 
                           (label_image.size[0]-1, i)], 
                          fill="black")
                draw.line([(0, label_image.size[1]-1-i), 
                           (label_image.size[0]-1, label_image.size[1]-1-i)], 
                          fill="black")
                draw.line([(i, 0), 
                           (i, label_image.size[1]-1)], 
                           fill="black")
                draw.line([(label_image.size[0]-1-i, 0),
                           (label_image.size[0]-1-i, label_image.size[1]-1)],
                          fill="black")
            if label_type == 2 or label_type == 3:
                for i in range(separator_line_thickness):
                    draw.line([(separator_line_thickness + label_component_barcode.get_image().size[0] +i, 0), 
                               (separator_line_thickness + label_component_barcode.get_image().size[0] +i, label_image.size[1]-1)], 
                              fill="black")
            else:
                pass
            return label_image


        self.dpi = (600, 600)
        self.label_type = label_type
        self.barcode_module_size = barcode_module_size
        self.text_font_size = text_font_size
        self.separator_line_thickness = separator_line_thickness
        
        self.text_encoded = _get_text_on_label(text, label_type)
        self.component_barcode = None
        self.component_text = None
        
        if barcode_module_size != -1 and text_font_size != -1:
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text_encoded, self.barcode_module_size)
            self.component_text = LabelComponentText(self.text_encoded, self.text_font_size)
            self.component_text.add_white_border(self.component_barcode.get_border_thickness())
        elif barcode_module_size == -1:
            self.component_text = LabelComponentText(self.text_encoded, self.text_font_size)
            self.barcode_module_size = _get_barcode_module_size(text_font_size, self.text_encoded, label_type)
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text_encoded, self.barcode_module_size)
            self.component_text.add_white_border(self.component_barcode.get_border_thickness())
        elif text_font_size == -1:
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text_encoded, self.barcode_module_size)
            self.text_font_size = _get_font_size(self.text_encoded, barcode_module_size, label_type)
            self.component_text = LabelComponentText(self.text_encoded, self.text_font_size)
            self.component_text.add_white_border(self.component_barcode.get_border_thickness())
        else:
            pass
        
        self.label_dimensions = _calculate_label_dimensions(self.component_barcode, self.component_text, separator_line_thickness, label_type)
        self.label_image = _assemble_components(self.component_barcode, self.component_text, self.label_dimensions, separator_line_thickness)
        self.label_image = _draw_bounding_lines(self.component_barcode, self.label_image, separator_line_thickness, label_type)
#         self._draw_corner_trim_lines()


    def get_image(self):
        """
        """
        return self.label_image

    def _draw_corner_trim_lines(self):
        """
        """
        # TODO: review
        line_width = 2
        to_trim = math.sqrt(2 * math.pow( self.specs["margin"], 2)) - self.specs["margin"]
        diagonal_trim_length = 2 * to_trim * math.tan(math.radians(45))
        label_trim_length = math.sqrt(math.pow(diagonal_trim_length, 2)/2)
        draw = ImageDraw.Draw(self.label_image)

        draw.line([(label_trim_length, 0), 
                   (0, label_trim_length )], 
                  fill="black", 
                  width=line_width)
        draw.line([(self.label_image.size[0] - label_trim_length, 0),
                   (self.label_image.size[0], label_trim_length)],
                  fill="black",
                  width=line_width)
        draw.line([(self.label_image.size[0], self.label_image.size[0] - label_trim_length),
                   (self.label_image.size[0] - label_trim_length, self.label_image.size[0])],
                  fill="black",
                  width=line_width)
        draw.line([(0, self.label_image.size[0] - label_trim_length), 
                   (label_trim_length, self.label_image.size[0])], 
                  fill="black", 
                  width=line_width )

        return

    def save_to_image_file(self, file_path):
        """
        """
        self.label_image.save(file_path, "PNG", dpi=self.dpi)
        return


