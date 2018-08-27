'''
@author: Klaus
'''

import string
from io import BytesIO
from pystrich.code128 import Code128Encoder
from PIL import Image

class LabelComponentBarcodeCode128:
    def __init__(self, text, module_size, height=1, quiet_zone_size_factor=10):
        def _generate_barcode(string_to_encode, module_size):
            """Return a PIL image object of the barcode.
            """
            if isinstance(module_size, int):
                encoder = Code128Encoder(string_to_encode)
                buffer = BytesIO()
                buffer.write(encoder.get_imagedata(module_size))
                image = Image.open(buffer)
                return image
            else:
                return None
    
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
        
        def _add_quiet_zones(barcode_image, module_size, size_factor):
            if isinstance(module_size * size_factor, int) and module_size * size_factor > 0:
                quiet_zone_size = size_factor * module_size
                image = Image.new("RGB",
                                  (barcode_image.size[0] + 2*quiet_zone_size*module_size,
                                   barcode_image.size[1]),
                                  "white")
                image.paste(barcode_image, (quiet_zone_size*module_size, 0))
                return image
            else:
                return barcode_image

        self.text_encoded = "".join([c for c in text if c in string.ascii_letters + string.digits])
        self.module_size = module_size
        self.barcode_height = round(height)
        self.barcode_image = _add_quiet_zones(_resize_barcode(_trim_barcode(_generate_barcode(self.text_encoded, module_size), module_size), round(height)), module_size, quiet_zone_size_factor)

    def get_image(self):
        """
        """
        return self.barcode_image
    
    def add_padding(self, padding_size):
        padded = Image.new("RGB",
                           (self.barcode_image.size[0] + 2*padding_size,
                            self.barcode_image.size[1] + 2*padding_size),
                           "white")
        padded.paste(self.barcode_image, (padding_size, padding_size))
        self.barcode_image = padded
        return

    def save_barcode_to_file(self, file_path, dpi=(600, 600)):
        self.barcode_image.save(file_path, "PNG", dpi=dpi)
        return
