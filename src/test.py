from src.label.LabelFullDataMatrix import LabelFullDataMatrix
from src.Page import Page

def format_int(i):
    s = "%08d" % (i,)
    s = "\n".join([s[:4], s[4:]])
    return s
 
paper = Page("/media/sf_shared/workspace/barcode/files/template_letter.png")

for i in range(500):
    label = LabelFullDataMatrix("".join(["a0a0", "a0a0", format_int(i)]), 2, 3, -1, 50) 
    coordinates = paper.find_coordinates_for_next_available_spot(label)
    print(coordinates)
    if coordinates == (-1, -1):
        break
    paper.add_label(label, coordinates)
paper.save_page_to_file("/media/sf_shared/page.png")
    
print("complete")


# template = Image.open("/media/sf_shared/workspace/barcode/files/template_letter.png")
# pix = template.load()
# for y in range(template.size[1]):
#     for x in range(template.size[0]):
#         if pix[x, y] != (255, 255, 255):
#             pix[x, y] = (128, 200, 50)
# template.save("/media/sf_shared/test.png")