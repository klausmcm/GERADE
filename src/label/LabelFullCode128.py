# import math
# import numpy
# from src.label.LabelComponentText import LabelComponentText
# from src.label.LabelComponentBarcodeCode128 import LabelComponentBarcodeCode128
# from src.label.LabelComponentBarcodeDataMatrix import LabelComponentBarcodeDataMatrix
# from PIL import Image
# from PIL import ImageDraw
# 
# class LabelDataMatrix:
#     def __init__(self, text, separator_line_thickness, label_type, barcode_module_size=-1, text_font_size=-1):
#         """
#         types
#         0 - Plain data matrix barcode                        1 - Plain code 128 barcode
#         1 - Data matrix barcode with text on the barcode     3 - Code 128 barcode with text on the barcode
#         2 - Data matrix barcode with text on the side        5 - Code 128 barcode with text at the bottom
#         6 -                                                  7 - Code 128 barcode with text on the side (thin but long) 
#         """
#         if barcode_module_size != -1 and text_font_size != -1:
#             pass
#         elif barcode_module_size == -1:
#             font_size = self._get_font_size()
#         elif text_font_size == -1:
#             pass
#         else:
#             pass
#         
#         self.barcode = None
#         self.text = text
#         self.label_type = label_type
#         self.line_thickness = separator_line_thickness
# 
#         self.label_dimensions = self.__calculate_label_dimensions()
#         self.label_image = Image.new("RGB", self.label_dimensions, "white")
#         self.__draw_corner_trim_lines()
#         self.__assemble_components()
#         self.__draw_bounding_box()
# 
#     def get_image(self):
#         return self.label_image
#     
#     def _get_barcode_module_size_code128(self):
#         return
#     
#     def _get_barcode_module_size_datamatrix(self):
#         return
#     
#     def _get_font_size(self):
#         font_size = -1
#         if self.label_type == 0:
#             font_size = 0
#         elif self.label_type == 2:
#             while True:
#                 text_image = LabelComponentText(self.text, font_size).get_image()
#                 if (text_image.size[0] <= self.barcode.add_surrounding_whitespace(self.barcode.get_cropped_barcode()).size[0] and
#                     text_image.size[1] <= self.barcode.add_surrounding_whitespace(self.barcode.get_cropped_barcode()).size[1]):
#                     font_size += 1
#                 else:
#                     break
#         elif self.label_type == 4:
#             while True:
#                 text_image = LabelComponentText(self.text, font_size).get_image()
#                 if text_image.size[1] <= self.barcode.add_surrounding_whitespace(self.get_cropped_barcode()).size[1]:
#                     font_size += 1
#                 else:
#                     break
#         return font_size
# 
#     def __calculate_label_dimensions(self):
#         """
#         """
#         barcode_datamatrix = self.barcode.add_surrounding_whitespace(self.barcode.get_cropped_barcode_datamatrix())
#         barcode_code128 = self.barcode.add_surrounding_whitespace(self.barcode.get_cropped_barcode_code128())
#         if self.label_type == 0:
#             return tuple(numpy.add(barcode_datamatrix.size, (2*self.line_thickness, 2*self.line_thickness)))
#         elif self.label_type == 1:
#             pass
#         elif self.label_type == 2:
#             width = max([barcode_datamatrix.size[0], self.text.size[0]])
#             height = max([barcode_datamatrix.size[1], self.text.size[1]])
#             return tuple(numpy.add((width, height), (2*self.line_thickness, 2*self.line_thickness)))
#         elif self.label_type == 3:
#             pass
#         elif self.label_type == 4:
#             width_barcode = barcode_datamatrix.size[0]
#             width_text = self.text.get_image().size[0]
#             height_barcode = barcode_datamatrix.size[1]
#             height_text = self.text.get_image().size[1]
#             
#         elif self.label_type == 5:
#             pass
#         elif self.label_type == 6:
#             pass
#         elif self.label_type == 7:
#             pass
#         
#         
#         label_length = max([self.text.get_image().size[0], 
#                             self.barcode.get_image().size[0] + self.text.get_image().size[1] + self.barcode.get_module_size()]) + 2 * self.specs["margin"]
#         return (round(label_length), 
#                 round(label_length))
# 
#     def __draw_corner_trim_lines(self):
#         line_width = 2
#         to_trim = math.sqrt(2 * math.pow( self.specs["margin"], 2)) - self.specs["margin"]
#         diagonal_trim_length = 2 * to_trim * math.tan(math.radians(45))
#         label_trim_length = math.sqrt(math.pow(diagonal_trim_length, 2)/2)
#         draw = ImageDraw.Draw(self.label_image)
# 
#         draw.line([(label_trim_length, 0), 
#                    (0, label_trim_length )], 
#                   fill="black", 
#                   width=line_width)
#         draw.line([(self.label_image.size[0] - label_trim_length, 0),
#                    (self.label_image.size[0], label_trim_length)],
#                   fill="black",
#                   width=line_width)
#         draw.line([(self.label_image.size[0], self.label_image.size[0] - label_trim_length),
#                    (self.label_image.size[0] - label_trim_length, self.label_image.size[0])],
#                   fill="black",
#                   width=line_width)
#         draw.line([(0, self.label_image.size[0] - label_trim_length), 
#                    (label_trim_length, self.label_image.size[0])], 
#                   fill="black", 
#                   width=line_width )
# 
#         return
# 
#     def __assemble_components(self):
#         top_y = round((self.label_image.size[1] - 
#                        (self.barcode.get_image().size[1] + 
#                         self.text.get_image().size[1] + 
#                         self.barcode.get_module_size())) / 2)
#         barcode_label_coordinates = (round((self.label_image.size[0] - self.text.get_image().size[0]) / 2), top_y)
#         barcode_coordinates = (round((self.label_image.size[0] - self.barcode.get_image().size[0]) / 2), 
#                                round(top_y + 
#                                      self.text.get_image().size[1] + 
#                                      self.barcode.get_module_size()))
#         self.label_image.paste(self.barcode.get_image(), barcode_coordinates)
#         self.label_image.paste(self.text.get_image(), barcode_label_coordinates)
# 
#         return
# 
#     def __draw_bounding_box(self):
#         template = Image.new("RGB", 
#                              (self.label_image.size[0] + 2, self.label_image.size[1] + 2), 
#                              "black")
#         template.paste(self.label_image, (1, 1))
#         self.label_image = template
#         return
# 

