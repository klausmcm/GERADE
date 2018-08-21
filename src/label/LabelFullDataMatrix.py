import math
import numpy
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
        self.line_thickness = separator_line_thickness
        
        if barcode_module_size != -1 and text_font_size != -1:
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text, self.barcode_module_size)
            self.component_text = LabelComponentText(self.text, self.text_font_size)
        elif barcode_module_size == -1:
            self.component_text = LabelComponentText(self.text, self.text_font_size)
            self.barcode_module_size = self._get_barcode_module_size()
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text, self.barcode_module_size)
        elif text_font_size == -1:
            self.component_barcode = LabelComponentBarcodeDataMatrix(self.text, self.barcode_module_size)
            self.text_font_size = self._get_font_size()
            self.component_text = LabelComponentText(self.text, self.text_font_size)
        else:
            pass
        
        print(self.text_font_size)

#         self.label_dimensions = self.__calculate_label_dimensions()
#         self.label_image = Image.new("RGB", self.label_dimensions, "white")
#         self.__draw_corner_trim_lines()
#         self.__assemble_components()
#         self.__draw_bounding_box()

    def get_image(self):
        return self.label_image
    
    def _get_barcode_module_size(self):
        """
        """
        #TODO: document
        module_size = 0
        while True:
            barcode_image = LabelComponentBarcodeDataMatrix(self.text, module_size).get_cropped_barcode()
            if (barcode_image.size[0] >= self.component_text.get_image().size[0] and
                barcode_image.size[1] >= self.component_text.get_image().size[1]):
                break
            else:
                module_size += 1
        return module_size
    
    def _get_font_size(self):
        font_size = -1
        if self.label_type == 0:
            font_size = 0
        else:
            while True:
                text_image = LabelComponentText(self.text, font_size).get_image()
                if (text_image.size[0] <= self.component_barcode.get_cropped_barcode().size[0] and
                    text_image.size[1] <= self.component_barcode.get_cropped_barcode().size[1]):
                    font_size += 1
                else:
                    break
        return font_size

    def __calculate_label_dimensions(self):
        """
        """
        # TODO: document
        barcode_datamatrix = self.component_barcode.get_cropped_barcode().add_surrounding_whitespace()
        if self.label_type == 0:
            return tuple(numpy.add(barcode_datamatrix.size, (2*self.line_thickness, 2*self.line_thickness)))
        elif self.label_type == 1:
            pass
        elif self.label_type == 2:
            width = max([barcode_datamatrix.size[0], self.text.size[0]])
            height = max([barcode_datamatrix.size[1], self.text.size[1]])
            return tuple(numpy.add((width, height), (2*self.line_thickness, 2*self.line_thickness)))
        elif self.label_type == 3:
            pass
        elif self.label_type == 4:
            width_barcode = barcode_datamatrix.size[0]
            width_text = self.text.get_image().size[0]
            height_barcode = barcode_datamatrix.size[1]
            height_text = self.text.get_image().size[1]
            
        elif self.label_type == 5:
            pass
        elif self.label_type == 6:
            pass
        elif self.label_type == 7:
            pass
        
        
        label_length = max([self.text.get_image().size[0], 
                            self.barcode.get_image().size[0] + self.text.get_image().size[1] + self.barcode.get_module_size()]) + 2 * self.specs["margin"]
        return (round(label_length), 
                round(label_length))

    def __draw_corner_trim_lines(self):
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

    def __assemble_components(self):
        # TODO: review
        top_y = round((self.label_image.size[1] - 
                       (self.component_barcode.get_image().size[1] + 
                        self.text.get_image().size[1] + 
                        self.component_barcode.get_module_size())) / 2)
        barcode_label_coordinates = (round((self.label_image.size[0] - self.text.get_image().size[0]) / 2), top_y)
        barcode_coordinates = (round((self.label_image.size[0] - self.component_barcode.get_image().size[0]) / 2), 
                               round(top_y + 
                                     self.text.get_image().size[1] + 
                                     self.barcode.get_module_size()))
        self.label_image.paste(self.barcode.get_image(), barcode_coordinates)
        self.label_image.paste(self.text.get_image(), barcode_label_coordinates)

        return

    def __draw_bounding_box(self):
        # TODO: review
        template = Image.new("RGB", 
                             (self.label_image.size[0] + 2, self.label_image.size[1] + 2), 
                             "black")
        template.paste(self.label_image, (1, 1))
        self.label_image = template
        return


