'''
@author: Klaus
'''

from PIL import Image
from PIL import ImageDraw



class Page():
    def __init__(self, file_path_template):
        self.template = Image.open(file_path_template)
        self.output = Image.new("RGB", self.template.size, "white")

    def find_coordinates_for_next_available_spot(self, label):
        """
        """
        label_size = label.get_image().size
        pixels_template = self.template.load()
        coordinates = (-1, -1)
        for y in range(self.template.size[1]):
            for x in range(self.template.size[0]):
                if pixels_template[x, y] == (255, 255, 255):
                    is_clear = True
                    for y_label in range(label_size[1]):
                        for x_label in range(label_size[0]):
                            if pixels_template[x+x_label, y+y_label] == (0, 0, 0):
                                is_clear = False
                                break
                        if not is_clear:
                            break
                    if is_clear:
                        return (x, y)
        return coordinates
    
    def add_label(self, label, label_coordinates):
        def update_template(template, label, label_coordinates):
            """
            """
            image_label = label.get_image()
            pixels_template = template.load()
            for y in range(image_label.size[1]):
                for x in range(image_label.size[0]):
                    pixels_template[x+label_coordinates[0], y+label_coordinates[1]] = (0, 0, 0)
            return template
        
        def update_output(output, label, label_coordinates):
            """
            """
            output.paste(label.get_image(), label_coordinates)
            return output
        
        self.template = update_template(self.template, label, label_coordinates)
        self.output = update_output(self.output, label, label_coordinates)
        
        return
    
    def get_page_dimensions(self):
        return self.template.size
    
    def save_page_to_file(self, file_path, dpi=(600, 600)):
        '''
        Write template image to an image file.
        '''
        self.output.save(file_path, dpi=dpi)
