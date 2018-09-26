'''
@author: Klaus
'''

from label.LabelFullDataMatrix import LabelFullDataMatrix
from label.LabelFullCode128 import LabelFullCode128
from Page import Page

cm = (1/2.54) * 600

if __name__ == "__main__":
    def format_int(i):
        s = "%08d" % (i,)
        s = "\n".join([s[:4], s[4:]])
        return s
    
    coordinates = (0, 0)
    paper = Page("/home/klaus/template.png", "/home/klaus/result.png")
    barcode_module_size = -1
    font_size = -1
    next_num = 370
    #redo = []
    
    for i in range(10**8):
        #TODO: test with the case where the line thickness is at least 20 -> need to review calculation of trim lines
        
        label = LabelFullCode128("".join(["a0a0", "a0a0", format_int(i + next_num)]), 2, 3)
        #label.rotate_label()
        if barcode_module_size != -1 and font_size != -1:
            label.set_label(barcode_module_size, font_size)
        else:
            label.set_label_by_dimensions((-1, (1.6/4) * cm))
            barcode_module_size = label.get_module_size()
            font_size = label.get_font_size()
        coordinates = paper.find_coordinates_for_next_available_spot(label)
        print(coordinates)
        if coordinates == (-1, -1):
            break
        paper.add_label(label, coordinates, overlap=True)
    paper.clean_template()
    paper.save_page_to_file("/home/klaus/result.png")
    paper.save_template_to_file("/home/klaus/template.png")
    
    print("complete")
