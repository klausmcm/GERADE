import math
from src.label.LabelComponentText import LabelComponentText
from src.label.LabelComponentBarcodeDataMatrix import LabelComponentBarcodeDataMatrix
from PIL import Image
from PIL import ImageDraw



class LabelFullDataMatrix:
    def __init__(self, text, separator_line_thickness, label_type, barcode_module_size=-1, text_font_size=-1):
        # TODO: implement
        """
        types
        0 - Plain data matrix barcode
        1 - Data matrix barcode with text on the barcode
        2 - Data matrix barcode with text on the right side
        3 - Data matrix barcode for use with cable ties on cables
        """
        self.component_barcode = None
        self.component_text = None
        self.barcode_module_size = barcode_module_size
        self.text_font_size = text_font_size
        self.text = text
        self.label_type = label_type
        
        if barcode_module_size != -1 and text_font_size != -1:
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text, self.barcode_module_size)
            self.component_text = LabelComponentText(self.text, self.text_font_size)
            self.component_text.add_white_border(self.component_barcode.get_border_thickness())
        elif barcode_module_size == -1:
            self.component_text = LabelComponentText(self.text, self.text_font_size)
            self.barcode_module_size = self._get_barcode_module_size()
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text, self.barcode_module_size)
            self.component_text.add_white_border(self.component_barcode.get_border_thickness())
        elif text_font_size == -1:
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text, self.barcode_module_size)
            self.text_font_size = self._get_font_size()
            self.component_text = LabelComponentText(self.text, self.text_font_size)
            self.component_text.add_white_border(self.component_barcode.get_border_thickness())
        else:
            pass
        
        self.separator_line_thickness = separator_line_thickness
        self.label_dimensions = (-1, -1)
        self.label_image = None
        
        self.label_dimensions = self._calculate_label_dimensions()
        
        self._assemble_components()
        self._draw_bounding_lines()
#         self._draw_corner_trim_lines()

#         self.label_image = Image.new("RGB", self.label_dimensions, "white")
        

    def get_image(self):
        return self.label_image
    
    def _get_barcode_module_size(self):
        """
        """
        #TODO: document
        module_size = 1
        while True:
            barcode_image = LabelComponentBarcodeDataMatrix(self.text, module_size, 0).get_image()
            if (barcode_image.size[0] >= self.component_text.get_image().size[0] and
                barcode_image.size[1] >= self.component_text.get_image().size[1]):
                break
            else:
                module_size += 1
        return module_size
    
    def _get_font_size(self):
        """
        """
        #TODO: document
        barcode_image = LabelComponentBarcodeDataMatrix(self.text, self.barcode_module_size, 0).get_image()
        font_size = -1
        while True:
            text_image = LabelComponentText(self.text, font_size).get_image()
            if (text_image.size[0] <= barcode_image.size[0] and
                text_image.size[1] <= barcode_image.size[1]):
                font_size += 1
            else:
                break
        return max([1, font_size-1])

    def _calculate_label_dimensions(self):
        """
        """
        # TODO: document
        barcode_image = self.component_barcode.get_image()
        if self.label_type == 0 or self.label_type == 1:
            width = barcode_image.size[0] + 2*self.separator_line_thickness
            height = barcode_image.size[1] +2*self.separator_line_thickness
        elif self.label_type == 2:
            width = barcode_image.size[0] + self.component_text.get_image().size[0] + 3*self.separator_line_thickness
            height = barcode_image.size[1] + 2*self.separator_line_thickness
        elif self.label_type == 3:
            #TODO: implement
            width = -1
            height = -1
        return (round(width), round(height))

    def _draw_corner_trim_lines(self):
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

    def _assemble_components(self):
        """
        """
        template = Image.new("RGB",
                             self.label_dimensions,
                             "white")
        if self.label_type == 0:
            template.paste(self.component_barcode.get_image(),
                           (self.separator_line_thickness, self.separator_line_thickness))
        elif self.label_type == 1:
            #TODO: implement
            template.paste(self.component_barcode.get_image(),
                           (self.separator_line_thickness, self.separator_line_thickness))
        elif self.label_type == 2:
            template.paste(self.component_barcode.get_image(),
                           (self.separator_line_thickness, self.separator_line_thickness))
            template.paste(self.component_text.get_image(),
                           (self.component_barcode.get_image().size[0] + 2*self.separator_line_thickness,
                            round(template.size[1]/2-self.component_text.get_image().size[1]/2)))
        elif self.label_type == 3:
            pass
        self.label_image = template
        return
    

        return

    def _draw_bounding_lines(self):
        # TODO: review
        draw = ImageDraw.Draw(self.label_image)
        for i in range(self.separator_line_thickness):
            draw.line([(0, i), 
                       (self.label_image.size[0]-1, i)], 
                      fill="black")
            draw.line([(0, self.label_image.size[1]-1-i), 
                       (self.label_image.size[0]-1, self.label_image.size[1]-1-i)], 
                      fill="black")
            draw.line([(i, 0), 
                       (i, self.label_image.size[1]-1)], 
                       fill="black")
            draw.line([(self.label_image.size[0]-1-i, 0),
                       (self.label_image.size[0]-1-i, self.label_image.size[1]-1)],
                      fill="black")
        if self.label_type == 2:
            for i in range(self.separator_line_thickness):
                draw.line([(self.separator_line_thickness + self.component_barcode.get_image().size[0] +i, 0), 
                           (self.separator_line_thickness + self.component_barcode.get_image().size[0] +i, self.label_image.size[1]-1)], 
                          fill="black")
        elif self.label_type == 3:
            pass
        else:
            pass
        
        return
    
    def save_to_image_file(self, file_path):
        self.label_image.save(file_path, "PNG")
        return


