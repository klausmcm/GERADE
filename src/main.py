'''
@author: Klaus
'''

from label.LabelFullDataMatrix import LabelFullDataMatrix
from label.LabelFullCode128 import LabelFullCode128
from Page import Page



if __name__ == "__main__":
    def format_int(i):
        s = "%08d" % (i,)
        s = "\n".join([s[:4], s[4:]])
        return s
    
    coordinates = (0, 0)
    paper = Page("/media/sf_shared/workspace/barcode/files/template_letter.png")
    barcode_module_size = -1
    
    for i in range(500):
        #TODO: test with the case where the line thickness is at least 20 -> need to review calculation of trim lines
        label = LabelFullDataMatrix("".join(["a0a0", "a0a0", format_int(i)]), 2, 3, barcode_module_size=-1, text_font_size=80)
        label.save_image_to_file("/media/sf_shared/test" + str(i) + ".png")
        if barcode_module_size == -1:
            barcode_module_size = label.get_module_size() 
        coordinates = paper.find_coordinates_for_next_available_spot(label)
        print(coordinates)
        if coordinates == (-1, -1):
            break
        paper.add_label(label, coordinates, overlap=True)
    paper.save_page_to_file("/media/sf_shared/page.png")
    
    print("complete")
