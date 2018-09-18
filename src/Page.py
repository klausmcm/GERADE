'''
@author: Klaus
'''

from PIL import Image

class Page():
    def __init__(self, file_path_template, dpi=(600, 600)):
        self.coordinates_black = {}
        self.coordinates_available = {}
        self.coordinates_accessed = {}
        
        def scan_template(template):
            template_pixels = template.load()
            for y in range(template.size[1]):
                for x in range(template.size[0]):
                    if template_pixels[x, y] == (0, 0, 0):
                        self.coordinates_black[(x, y)] = True
                    else:
                        self.coordinates_available[(x, y)] = True
            return
        
        self.dpi = dpi
        self.template = Image.open(file_path_template)
        self.output = Image.new("RGB", self.template.size, "white")
        scan_template(self.template)
        
        

    def find_coordinates_for_next_available_spot(self, label):
        """
        """
        def has_enough_space(label, template, coordinates):
            template_pixels = template.load()
            template_size = template.size
            label_size = label.get_image().size
            if (template_pixels[coordinates[0], coordinates[1]] == (0, 0, 0) or 
                coordinates[0] + label_size[0] > template_size[0] or 
                coordinates[1] + label_size[1] > template_size[1]):
                return False
            else:
                for y_label in range(label_size[1]):
                    for x_label in range(label_size[0]):
                        self.coordinates_accessed[(coordinates[0] + x_label, coordinates[1] + y_label)] = True
                        if template_pixels[coordinates[0] + x_label, coordinates[1] + y_label] == (0, 0, 0):
                            return False
                                
            return True
        
#         for y in range(self.template.size[1]):
#             for x in range(self.template.size[0]):
#                 if has_enough_space(label, self.template, (x, y)):
#                     return (x, y)

        for coordinates in self.coordinates_available:
            if not self.coordinates_accessed[coordinates] and has_enough_space(label, self.template, coordinates):
                return coordinates
        return (-1, -1)
    
    def add_label(self, label, label_coordinates, overlap=False):
        """
        """
        def get_adjusted_coordinates(label, coordinates, overlap):
            """
            """
            if overlap:
                label_coordinates = (coordinates[0] - label.get_border_thickness(), 
                                     coordinates[1] - label.get_border_thickness())
            else:
                label_coordinates = coordinates
            return label_coordinates
        
        def update_output(output, label, label_coordinates):
            """
            """
            output.paste(label.get_image(), label_coordinates)
            return output
        
        def update_template(template, label, label_coordinates):
            """
            """
            template_pixels = template.load()
            for y_label in range(label.get_image().size[1]):
                for x_label in range(label.get_image().size[0]):
                    template_pixels[label_coordinates[0] + x_label, label_coordinates[1] + y_label] = (0, 0, 0)
                    self.coordinates_available.pop(label_coordinates, None)
                    self.coordinates_black[label_coordinates] = True
            return template
        
        label_coordinates = get_adjusted_coordinates(label, label_coordinates, overlap)
        update_output(self.output, label, label_coordinates)
        update_template(self.template, label, label_coordinates)
        
        return
    
    def get_page_dimensions(self):
        return self.template.size
    
    def save_page_to_file(self, file_path):
        '''
        Write template image to an image file.
        '''
        self.output.save(file_path, dpi=self.dpi)
        
    def save_template_to_file(self, file_path):
        """
        """
        self.template.save(file_path, dpi=self.dpi)
