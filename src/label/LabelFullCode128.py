import math
import string
import sys
from LabelComponentText import LabelComponentText
from LabelComponentBarcodeCode128 import LabelComponentBarcodeCode128
from PIL import Image
from PIL import ImageDraw
 
class LabelFullCode128:
    def __init__(self, text, separator_line_thickness, label_type, dpi=(600, 600)):
        """
        types
        0 - Plain code 128 barcode - barcode width and height is at least equal to the text width and height
        1 - Code 128 barcode with text on the barcode - barcode has +1/= height as the text and is >=x2 the width of the text
        2 - Code 128 barcode with text at the bottom - barcode has +1/= height as the text and is >=x2 the width of the text
        3 - Code 128 barcode with text on the side (thin but long) - barcode width and height is at least equal to the text width and height
        """
        def _get_text_on_label(text, label_type):
            text_on_label = "".join([c for c in text if c in string.ascii_letters + string.digits])
            text_on_label = "-".join([text_on_label[:4],
                                      text_on_label[4:8],
                                      text_on_label[8:12],
                                      text_on_label[12:]])
            return text_on_label
        
        
        self.dpi = dpi
        self.label_type = label_type
        self.text_on_label = _get_text_on_label(text, label_type)
        self.separator_line_thickness = separator_line_thickness
        
        
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
        def get_font_size(font_size, label_type, text_on_label, barcode_module_size):
            if font_size != -1:
                return font_size
            else:
                font_size = 1
                barcode_image = LabelComponentBarcodeCode128(text_on_label, barcode_module_size, quiet_zone_size_factor=0).get_image()
                if label_type == 1 or label_type == 2:
                    while True:
                        text_image = LabelComponentText(text_on_label, font_size).get_image()
                        if (text_image.size[0] > barcode_image.size[0]/2):
                            font_size -= 1
                            break
                        else:
                            font_size += 1
                elif label_type == 0 or label_type == 3:
                    while True:
                        text_image = LabelComponentText(text_on_label, font_size).get_image()
                        if (text_image.size[0] > barcode_image.size[0]):
                            font_size -= 1
                            break
                        else:
                            font_size += 1
                return max([1, font_size])

        def get_barcode_module_size(barcode_module_size, label_type, font_size, text_on_label):
            if barcode_module_size != -1:
                return barcode_module_size
            else:
                module_size = 1
                text_image = LabelComponentText(text_on_label, font_size).get_image()
                if label_type == 1 or label_type == 2:
                    while True:
                        barcode_image = LabelComponentBarcodeCode128(text_on_label, module_size, quiet_zone_size_factor=0).get_image()
                        if barcode_image.size[0] > 2*text_image.size[0]:
                            break
                        else:
                            module_size += 1
                elif label_type == 0 or label_type == 3:
                    while True:
                        barcode_image = LabelComponentBarcodeCode128(text_on_label, module_size, quiet_zone_size_factor=0).get_image()
                        if barcode_image.size[0] > text_image.size[0]:
                            break
                        else:
                            module_size += 1
                return module_size
        
        def calculate_label_dimensions(component_barcode, component_text, separator_line_thickness, label_type):
            """
            """
            dimensions = (-1, -1)
            if label_type == 0 or label_type == 1:
                width = 2*separator_line_thickness + component_barcode.get_image().size[0]
                height = 2*separator_line_thickness + component_barcode.get_image().size[1]
                dimensions = (width, height)
            elif label_type == 2:
                width = 2*separator_line_thickness + component_barcode.get_image().size[0]
                height = 3*separator_line_thickness + component_barcode.get_image().size[1] + component_text.get_image().size[1]
                dimensions = (width, height)
            elif label_type == 3:
                width = 3*separator_line_thickness + component_barcode.get_image().size[0] + component_text.get_image().size[0]
                height = 2*separator_line_thickness + component_barcode.get_image().size[1]
                dimensions = (width, height)
            else:
                pass
            return dimensions
        
        def assemble_components(label_dimensions, component_barcode, component_text, separator_line_thickness, label_type):
            def draw_separator_lines(label_image, component_barcode, component_text, separator_line_thickness, label_type):
                result = ImageDraw.Draw(label_image)
                for i in range(separator_line_thickness):
                    result.line([(0, i),
                                 (label_dimensions[0]-1, i)],
                                fill="black")
                    result.line([(0, label_dimensions[1]-1-i),
                                 (label_dimensions[0]-1, label_dimensions[1]-1-i)],
                                fill="black")
                    result.line([(i, 0),
                                 (i, label_dimensions[1]-1)],
                                fill="black")
                    result.line([(label_dimensions[0]-1-i, 0),
                                 (label_dimensions[0]-1-i, label_dimensions[1]-1-i)],
                                fill="black")
                if label_type == 0 or label_type == 1:
                    pass
                elif label_type == 2:
                    for i in range(separator_line_thickness):
                        result.line([(0, separator_line_thickness + component_barcode.get_image().size[1] + i),
                                     (label_dimensions[0]-1, separator_line_thickness + component_barcode.get_image().size[1] + i)],
                                    fill="black")
                elif label_type == 3:
                    for i in range(separator_line_thickness):
                        result.line([(separator_line_thickness + component_barcode.get_image().size[0] + i, 0),
                                     (separator_line_thickness + component_barcode.get_image().size[0] + i, label_dimensions[1]-1)],
                                    fill="black")
                return label_image
            
            result = Image.new("RGB", label_dimensions, "white")
            if label_type == 0:
                result.paste(component_barcode.get_image(),
                             (separator_line_thickness, separator_line_thickness))
            elif label_type == 1:
                result.paste(component_barcode.get_image(),
                             (separator_line_thickness, separator_line_thickness))
                result.paste(component_text.get_image(),
                             (separator_line_thickness + round(label_dimensions[0]/2 - component_text.get_image().size[0]/2),
                              round((label_dimensions[1]/2 - component_text.get_image().size[1]/2))),
                             mask=component_text.get_image())
            elif label_type == 2:
                result.paste(component_barcode.get_image(),
                             (separator_line_thickness, separator_line_thickness))
                result.paste(component_text.get_image(),
                             (separator_line_thickness + round(label_dimensions[0]/2 - component_text.get_image().size[0]/2),
                              2*separator_line_thickness + component_barcode.get_image().size[1] + round((label_dimensions[1] - separator_line_thickness - component_barcode.get_image().size[1])/2 - component_text.get_image().size[1]/2)),
                             mask=component_text.get_image())
            elif label_type == 3:
                result.paste(component_barcode.get_image(),
                             (separator_line_thickness, separator_line_thickness))
                result.paste(component_text.get_image(),
                             (2*separator_line_thickness + component_barcode.get_image().size[0],
                              round(label_dimensions[1]/2 - component_text.get_image().size[1]/2)),
                             mask=component_text.get_image())
            result = draw_separator_lines(result, component_barcode, component_text, separator_line_thickness, label_type)
            return result
        
        def draw_corner_trim_lines(label_image, line_width, barcode_padding_thickness):
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
            return label_image
        
        self.size_barcode_module = get_barcode_module_size(size_barcode_module, label_type, size_font, self.text_on_label)
        self.size_font = get_font_size(size_font, label_type, self.text_on_label, self.size_barcode_module)
        
        if label_type == 1:
            self.component_text = LabelComponentText(self.text_on_label, self.size_font, color="gray")
        else:    
            self.component_text = LabelComponentText(self.text_on_label, self.size_font)
        self.component_barcode = LabelComponentBarcodeCode128(self.text_on_label, self.size_barcode_module, height=self.component_text.get_image().size[1])
        
        self.component_text.add_white_border(4*self.size_barcode_module)
        self.component_barcode.add_padding(4*self.size_barcode_module)
        
        self.label_dimensions = calculate_label_dimensions(self.component_barcode, self.component_text, separator_line_thickness, label_type)
        self.label_image = assemble_components(self.label_dimensions, self.component_barcode, self.component_text, separator_line_thickness, label_type)
        self.label_image = draw_corner_trim_lines(self.label_image, separator_line_thickness, 2*self.size_barcode_module)

    def get_image(self):
        return self.label_image
    
    def get_module_size(self):
        return self.size_barcode_module
    
    def get_font_size(self):
        return self.size_font
    
    def get_border_thickness(self):
        return self.separator_line_thickness
    
    def save_image_to_file(self, file_path):
        self.label_image.save(file_path, "PNG", dpi=self.dpi)
