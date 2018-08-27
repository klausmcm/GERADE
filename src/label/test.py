# import itertools
# import string
# 
# perms = itertools.permutations(string.digits*2, 8)
# 
# count = 0
# print(len(perms))





import os
from src.label.LabelFullDataMatrix import LabelFullDataMatrix
from src.label.LabelFullCode128 import LabelFullCode128

font_size = 32
 
def format_int(i):
    s = "%08d" % (i,)
    s = "\n".join([s[:4], s[4:]])
    return s
 
for i in range(1):
    string = "\n".join(["a0a0", "a0a0", format_int(i)])
    file_path_result = "".join(string.split("\n"))
      
    l = LabelFullDataMatrix(string,
                            separator_line_thickness=1,
                            label_type=1,
                            barcode_module_size=-1,
                            text_font_size=font_size).save_to_image_file(os.path.join("/media/sf_shared/", "".join([file_path_result + "_2", ".png"])))
      
    l = LabelFullDataMatrix(string,
                            separator_line_thickness=1,
                            label_type=1,
                            barcode_module_size=-1,
                            text_font_size=font_size).save_to_image_file(os.path.join("/media/sf_shared/", "".join([file_path_result + "_3", ".png"])))
    
l = LabelFullCode128("a0a0a0a012345678",
                     separator_line_thickness=1,
                     label_type=1,
                     barcode_module_size=-1,
                     text_font_size=font_size).save_image_to_file("/media/sf_shared/test1.png")
l = LabelFullCode128("a0a0a0a012345678",
                     separator_line_thickness=1,
                     label_type=2,
                     barcode_module_size=-1,
                     text_font_size=font_size).save_image_to_file("/media/sf_shared/test2.png")
l = LabelFullCode128("a0a0a0a012345678",
                     separator_line_thickness=1,
                     label_type=3,
                     barcode_module_size=-1,
                     text_font_size=font_size).save_image_to_file("/media/sf_shared/test3.png")

 
print("complete")
