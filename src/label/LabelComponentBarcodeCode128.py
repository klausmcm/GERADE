'''
@author: Klaus
'''

from io import BytesIO
from pystrich.code128 import Code128Encoder
from PIL import Image

class LabelComponentBarcodeCode128:
    def __init__(self, text, module_size, whitespace_padding_size, height):
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
        
        def _add_whitespace_padding(barcode_image, padding_size, module_size):
            whitespace_padding_pixels = max([padding_size*module_size, 10])
            padded = Image.new("RGB",
                               (barcode_image.size[0] + 2*whitespace_padding_pixels,
                                barcode_image.size[1] + 2*whitespace_padding_pixels),
                               "white")
            padded.paste(barcode_image, (whitespace_padding_pixels, whitespace_padding_pixels))
            return padded
        
        self.dpi = (600, 600)
        self.text_on_label = text
        self.module_size = module_size
        self.whitespace_padding_size = whitespace_padding_size
        self.barcode_height = round(height)
        self.barcode_image = _add_whitespace_padding(_resize_barcode(_trim_barcode(_generate_barcode(text, module_size), module_size), round(height)), whitespace_padding_size, module_size)

    def get_image(self):
        """
        """
        return self.barcode_image

    def save_barcode_to_file(self, file_path):
        self.barcode_image.save(file_path, "PNG", dpi=self.dpi)
        return
