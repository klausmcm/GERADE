# import itertools
# import string
# 
# perms = itertools.permutations(string.digits*2, 8)
# 
# count = 0
# print(len(perms))

import os
from src.label.LabelFullDataMatrix import LabelFullDataMatrix

def format_int(i):
    s = "%08d" % (i,)
    s = "\n".join([s[:4], s[4:]])
    return s

# for i in range(1000):
#     string = "\n".join(["a0a0", "a0a0", format_int(i)])
string="abc"
l = LabelFullDataMatrix(string, 2, 2, barcode_module_size=-1, text_font_size=50)
l.save_to_image_file(os.path.join("/media/sf_shared/", "".join(["test", ".png"])))
