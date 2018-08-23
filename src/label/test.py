# import itertools
# import string
# 
# perms = itertools.permutations(string.digits*2, 8)
# 
# count = 0
# print(len(perms))

import os
from src.label.LabelFullDataMatrix import LabelFullDataMatrix
from src.label.LabelComponentBarcodeCode128 import LabelComponentBarcodeCode128

def format_int(i):
    s = "%08d" % (i,)
    s = "\n".join([s[:4], s[4:]])
    return s

# for i in range(1000):
#     string = "\n".join(["a0a0", "a0a0", format_int(i)])
#     file_path_result = "".join(string.split("\n"))
#     
#     l = LabelFullDataMatrix(string,
#                             separator_line_thickness=1,
#                             label_type=2,
#                             barcode_module_size=20,
#                             text_font_size=-1)
#     l.save_to_image_file(os.path.join("/media/sf_shared/", "".join([file_path_result + "_2", ".png"])))
#     
#     l = LabelFullDataMatrix(string,
#                             separator_line_thickness=1,
#                             label_type=3,
#                             barcode_module_size=20,
#                             text_font_size=-1)
#     l.save_to_image_file(os.path.join("/media/sf_shared/", "".join([file_path_result + "_3", ".png"])))

l = LabelComponentBarcodeCode128("a0a0a0a000000000", module_size=1, whitespace_padding_size=10, height=(1/2.54)*600)
l.save_barcode_to_file("/media/sf_shared/test.png")
