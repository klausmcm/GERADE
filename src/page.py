'''
@author: Klaus
'''

from PIL import Image

class Page():
    def __init__(self, file_path_template, dpi=(600, 600)):
        self.dpi = dpi
        self.template = Image.open(file_path_template)
        self.output = Image.new("RGB", self.template.size, "white")
        self.last_used_coordinates = (0, 0)

    def find_coordinates_for_next_available_spot(self, label):
        """
        """
        #TODO: use the start coordinates to make finding an available spot faster
        def has_enough_space(label, template, coordinates):
            template_pixels = template.load()
            template_size = template.size
            label_size = label.get_image().size
            if coordinates[0] + label_size[0] > template_size[0] or coordinates[1] + label_size[1] > template_size[1]:
                return False
            else:
                for y_label in range(label_size[1]):
                    for x_label in range(label_size[0]):
                        if template_pixels[x_label + coordinates[0], y_label + coordinates[1]] == (0, 0, 0):
                            return False
            return True
        
        for y in range(self.template.size[1]):
            for x in range(self.template.size[0]):
                if has_enough_space(label, self.template, (x + self.last_used_coordinates[0], y)):
                    return (x, y)
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
        
        def update_template(template, label, label_coordinates, overlap):
            """
            """
            image_label = label.get_image()
            pixels_template = template.load()
            label_coordinates = get_adjusted_coordinates(label, label_coordinates, overlap)
            for y in range(image_label.size[1]):
                for x in range(image_label.size[0]):
                    pixels_template[x + label_coordinates[0], y + label_coordinates[1]] = (0, 0, 0)
            return template
        
        def update_output(output, label, label_coordinates, overlap):
            """
            """
            output.paste(label.get_image(), get_adjusted_coordinates(label, label_coordinates, overlap))
            return output 
        
        self.template = update_template(self.template, label, label_coordinates, overlap)
        self.output = update_output(self.output, label, label_coordinates, overlap)
        self.last_used_coordinates = get_adjusted_coordinates(label, label_coordinates, overlap)
        
        return
    
    def get_page_dimensions(self):
        return self.template.size
    
    def save_page_to_file(self, file_path):
        '''
        Write template image to an image file.
        '''
        self.output.save(file_path, dpi=self.dpi)
