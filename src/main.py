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
    font_size = -1
    
    for i in range(500):
        #TODO: test with the case where the line thickness is at least 20 -> need to review calculation of trim lines
        label = LabelFullDataMatrix("".join(["a0a0", "a0a0", format_int(i)]), 2, 3)
        if barcode_module_size != -1 and font_size != -1:
            label.set_label(barcode_module_size, font_size)
        else:
            label.set_label_by_dimensions((500, 500))
            barcode_module_size = label.get_module_size()
            font_size = label.get_font_size()
#         label.save_image_to_file("/media/sf_shared/test" + str(i) + ".png")
        coordinates = paper.find_coordinates_for_next_available_spot(label)
        print(coordinates)
        if coordinates == (-1, -1):
            break
        paper.add_label(label, coordinates, overlap=True)
    paper.save_page_to_file("/media/klaus/ssh/pi-bedroom-remote/downloads/page.png")
    
    print("complete")
