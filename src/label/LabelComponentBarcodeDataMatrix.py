'''
@author: Klaus
'''

import string
from io import BytesIO
from pystrich.datamatrix import DataMatrixEncoder
from PIL import Image

class LabelComponentBarcodeDataMatrix:
    def __init__(self, text, module_size, quiet_zone_thickness=-1):
        """
        text                 -
        module_size          -
        quiet_zone_thickness - The thickness of the border in number of modules.
        """
        
        def _generate_barcode(string_to_encode, module_size):
            """Return a PIL image object of the barcode.
            """
            #TODO: document
            if isinstance(module_size, int) and module_size > 0:
                encoder = DataMatrixEncoder(string_to_encode)
                buffer = BytesIO()
                buffer.write(encoder.get_imagedata(module_size))
                image = Image.open(buffer)
                return image
            else:
                return None
        
        def _trim_barcode(barcode_image):
            """2x module size top/bottom/left/right
            """
            #TODO: document
            barcode_side_length = barcode_image.size[0]
            cropped_image = barcode_image.crop((2*self.module_size, 
                                                2*self.module_size,
                                                barcode_side_length-2*self.module_size, 
                                                barcode_side_length-2*self.module_size))
            return cropped_image
    
        def _add_quiet_zone(barcode_image):
            """
            """
            #TODO: document
            barcode_with_whitespace = Image.new("RGB",
                                                (barcode_image.size[0] + 2*self.quiet_zone_thickness,
                                                 barcode_image.size[1] + 2*self.quiet_zone_thickness),
                                                "white")
            barcode_with_whitespace.paste(barcode_image,
                                          (self.quiet_zone_thickness,
                                           self.quiet_zone_thickness))
            return barcode_with_whitespace
        
        self.quiet_zone_thickness = 2*module_size if quiet_zone_thickness == -1 else quiet_zone_thickness
        self.text_encoded = "".join([c for c in text if c in string.ascii_letters + string.digits])
        self.module_size = module_size
        self.barcode_image = _add_quiet_zone(_trim_barcode(_generate_barcode(self.text_encoded, module_size)))
        
    def get_image(self):
        """
        """
        return self.barcode_image
    
    def get_border_thickness(self):
        """
        """
        return self.quiet_zone_thickness

    def save_barcode_to_file(self, file_path, dpi=(600, 600)):
        """
        """
        self.barcode_image.save(file_path, "PNG", dpi=dpi)
        return
