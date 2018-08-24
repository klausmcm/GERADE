'''
@author: Klaus
'''

import string
from io import BytesIO
from pystrich.code128 import Code128Encoder
from PIL import Image

class LabelComponentBarcodeCode128:
    def __init__(self, text, module_size, height=1):
        def _generate_barcode(string_to_encode, module_size):
            """Return a PIL image object of the barcode.
            """
            encoder = Code128Encoder(string_to_encode)
            buffer = BytesIO()
            buffer.write(encoder.get_imagedata(module_size))
            image = Image.open(buffer)
            return image
    
        def _trim_barcode(barcode_image, module_size):
            """5x module size top
              10x module size left/right
            """
            barcode_width = barcode_image.size[0]
            cropped_image = barcode_image.crop((10*module_size,
                                                5*module_size,
                                                barcode_width - 10*module_size,
                                                5*module_size + 10*module_size))
            return cropped_image
        
        def _resize_barcode(barcode_image, height):
            image = barcode_image.resize((barcode_image.size[0], height))
            return image
        
        def _add_quiet_zones(barcode_image, module_size):
            minimum_quiet_zone_factor = 10
            image = Image.new("RGB",
                              (barcode_image.size[0] + 2*minimum_quiet_zone_factor*module_size,
                               barcode_image.size[1]),
                              "white")
            image.paste(barcode_image, (minimum_quiet_zone_factor*module_size, 0))
            return image
        
        self.dpi = (600, 600)
        self.text_encoded = "".join([c for c in text if c in string.ascii_letters + string.digits])
        self.module_size = module_size
        self.barcode_height = round(height)
        self.barcode_image = _add_quiet_zones(_resize_barcode(_trim_barcode(_generate_barcode(self.text_encoded, module_size), module_size), round(height)), module_size)
        self.barcode_image_trimmed = _resize_barcode(_trim_barcode(_generate_barcode(self.text_encoded, module_size), module_size), round(height))

    def get_image(self):
        """
        """
        return self.barcode_image
    
    def get_image_trimmed_barcode(self):
        """
        """
        return self.barcode_image_trimmed
    
    def add_whitespace_padding(self, padding_size):
        padded = Image.new("RGB",
                           (self.barcode_image.size[0] + 2*padding_size,
                            self.barcode_image.size[1] + 2*padding_size),
                           "white")
        padded.paste(self.barcode_image, (padding_size, padding_size))
        self.barcode_image = padded
        return

    def save_barcode_to_file(self, file_path):
        self.barcode_image.save(file_path, "PNG", dpi=self.dpi)
        return
