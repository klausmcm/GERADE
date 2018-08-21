'''
@author: Klaus
'''

import string
from io import BytesIO
from pystrich.datamatrix import DataMatrixEncoder
from PIL import Image

class LabelComponentBarcodeDataMatrix:
    def __init__(self, text, module_size):
        self.text = "".join([c for c in text if c in string.ascii_letters + string.digits])
        self.module_size = module_size
        self.barcode_image = self._get_barcode_image(text, module_size)

    def _get_barcode_image(self, string_to_encode, module_size):
        """Return a PIL image object of the barcode.
        """
        encoder = DataMatrixEncoder(string_to_encode)
        buffer = BytesIO()
        buffer.write(encoder.get_imagedata(module_size))
        image = Image.open(buffer)
        return image
    
    def get_cropped_barcode(self):
        """2x module size top/bottom/left/right
        """
        barcode_side_length = self.barcode_image.size[0]
        cropped_image = self.barcode_image.crop((2*self.module_size, 
                                                 2*self.module_size,
                                                 barcode_side_length-2*self.module_size, 
                                                 barcode_side_length-2*self.module_size))
        return cropped_image

    def add_surrounding_whitespace(self):
        """
        """
        barcode_with_whitespace = Image.new("RGB", 
                                            (self.barcode_image.size[0] + 2*2*self.module_size, self.barcode_image.size[1] + 2*2*self.module_size), 
                                            "white")
        barcode_with_whitespace.paste(self.barcode_image, (2*self.module_size, 2*self.module_size))
        return barcode_with_whitespace

    def save_barcode_to_file(self, file_path):
        self.barcode_image.save(file_path, "PNG", dpi=(600, 600))
        return
