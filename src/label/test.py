# import itertools
# import string
# 
# perms = itertools.permutations(string.digits*2, 8)
# 
# count = 0
# print(len(perms))

from src.label.LabelFullDataMatrix import LabelFullDataMatrix

l = LabelFullDataMatrix("a0a0\na0a0\n0000\n0000", 2, 2, barcode_module_size=-1, text_font_size=50)
l.save_to_image_file("/media/sf_shared/test.png")
