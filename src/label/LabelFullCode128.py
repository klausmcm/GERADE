import math
import string
from src.label.LabelComponentText import LabelComponentText
from src.label.LabelComponentBarcodeCode128 import LabelComponentBarcodeCode128
from PIL import Image
from PIL import ImageDraw
 
class LabelFullCode128:
    def __init__(self, text, separator_line_thickness, label_type, barcode_module_size=-1, text_font_size=-1):
        """
        types
        0 - Plain code 128 barcode - no text
        1 - Code 128 barcode with text on the barcode - barcode has +1/= height as the text and is >=x2 the width of the text
        2 - Code 128 barcode with text at the bottom - barcode has +1/= height as the text and is >=x2 the width of the text
        3 - Code 128 barcode with text on the side (thin but long) - barcode width and height is equal to the text width and height
        """
        #FIXME: generated label has a quiet space area of 12x module size instead of 10x module size
        def _get_text_on_label(text, label_type):
            result = ""
            if label_type == 0:
                result = ""
            elif label_type == 1 or label_type == 2 or label_type == 3:
                result = "-".join([text[:4], text[4:8], text[8:12], text[12:]])
            else:
                result = ""
            return result
        
        def _get_font_size(label_type, text_on_label, barcode_module_size):
            font_size = 1
            barcode_image = LabelComponentBarcodeCode128(text_on_label, barcode_module_size).get_image_trimmed_barcode()
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

        def _get_barcode_module_size(label_type, font_size, text_on_label):
            module_size = 1
            text_image = LabelComponentText(text_on_label, font_size).get_image()
            if label_type == 1 or label_type == 2:
                while True:
                    barcode_image = LabelComponentBarcodeCode128(text_on_label, module_size).get_image_trimmed_barcode()
                    if barcode_image.size[0] > 2*text_image.size[0]:
                        break
                    else:
                        module_size += 1
            elif label_type == 0 or label_type == 3:
                while True:
                    barcode_image = LabelComponentBarcodeCode128(text_on_label, module_size).get_image_trimmed_barcode()
                    if barcode_image.size[0] > text_image.size[0]:
                        break
                    else:
                        module_size += 1
            return module_size
        
        def _calculate_label_dimensions(component_barcode, component_text, separator_line_thickness, label_type):
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
        
        def _assemble_components(label_dimensions, component_barcode, component_text, separator_line_thickness, label_type):
            def _draw_separator_lines(label_image, component_barcode, component_text, separator_line_thickness, label_type):
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
            elif label_type == 2:
                result.paste(component_barcode.get_image(),
                             (separator_line_thickness, separator_line_thickness))
                result.paste(component_text.get_image(),
                             (separator_line_thickness + round(label_dimensions[0]/2 - component_text.get_image().size[0]/2),
                              2*separator_line_thickness + component_barcode.get_image().size[1]))
            elif label_type == 3:
                result.paste(component_barcode.get_image(),
                             (separator_line_thickness, separator_line_thickness))
                result.paste(component_text.get_image(),
                             (2*separator_line_thickness + component_barcode.get_image().size[0],
                              separator_line_thickness))
            result = _draw_separator_lines(result, component_barcode, component_text, separator_line_thickness, label_type)
            return result
        
        def _draw_corner_trim_lines(label_image, line_width, barcode_padding_thickness):
            """
            """
            #FIXME:
            offset = round((math.sqrt(2*math.pow(barcode_padding_thickness, 2)) - barcode_padding_thickness) / math.cos(math.radians(45)))
            draw = ImageDraw.Draw(label_image)
            for i in range(line_width):
                draw.line([(0, offset-i),
                           (offset-i, 0)],
                          fill="black")
                draw.line([(label_image.size[0]-offset+i, 0),
                           (label_image.size[0], offset-i)],
                          fill="black")
                draw.line([(label_image.size[0]-1, label_image.size[1]-offset-i),
                           (label_image.size[0]-offset-i, label_image.size[1]-1)],
                          fill="black")
                draw.line([(offset-i, label_image.size[1]),
                           (0, label_image.size[1]-offset+i)],
                          fill="black")
            return label_image
        
        self.text_encoded = "".join([c for c in text if c in string.ascii_letters + string.digits])
        self.text_on_label = _get_text_on_label(text, label_type)
        self.font_size = text_font_size
        self.barcode_module_size = barcode_module_size
        self.line_thickness = separator_line_thickness
        
        if barcode_module_size != -1 and text_font_size != -1:
            pass
        elif barcode_module_size == -1:
            self.barcode_module_size = _get_barcode_module_size(label_type, text_font_size, self.text_on_label)
        elif text_font_size == -1:
            self.font_size = _get_font_size(label_type, text, barcode_module_size)
        else:
            pass
        
        self.component_text = LabelComponentText(self.text_on_label, self.font_size)
        self.component_barcode = LabelComponentBarcodeCode128(self.text_encoded, self.barcode_module_size, height=self.component_text.get_image().size[1])
        
        self.component_text.add_white_border(2*barcode_module_size)
        self.component_barcode.add_whitespace_padding(2*barcode_module_size)
        
        self.label_dimensions = _calculate_label_dimensions(self.component_barcode, self.component_text, separator_line_thickness, label_type)
        self.label_image = _assemble_components(self.label_dimensions, self.component_barcode, self.component_text, separator_line_thickness, label_type)
        self.label_image = _draw_corner_trim_lines(self.label_image, separator_line_thickness, 2*barcode_module_size)
 
    def get_image(self):
        return self.label_image
    
    def save_image_to_file(self, file_path, dpi=(600, 600)):
        self.label_image.save(file_path, "PNG", dpi=dpi)
