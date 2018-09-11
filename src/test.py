'''
Created on 2018-09-11

@author: klaus
'''


from LabelFullDataMatrix import LabelFullDataMatrix

l = LabelFullDataMatrix("a1a2a3a412341234", 2, 2)
# l.set_label_by_barcode_module_size(5)
# l.set_label_by_font_size(20)
cm=int(5*round((1/2.54)*(600/1)))
l.set_label_by_dimensions((-1, cm))
l.save_image_to_file("/media/sf_shared/test.png")
print(l.get_module_size(), l.get_font_size())
print("complete")
