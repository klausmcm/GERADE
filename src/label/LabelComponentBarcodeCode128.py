'''
@author: Klaus
'''

from io import BytesIO
from pystrich.code128 import Code128Encoder
from PIL import Image

class LabelComponentBarcodeCode128:
    def __init__(self, text, module_size):
        self.text_on_label = text
        self.module_size = module_size
        self.barcode_image = self._generate_barcode(text, module_size)
        pass

    def _generate_barcode(self, string_to_encode, module_size):
        """Return a PIL image object of the barcode.
        """
        encoder = Code128Encoder(string_to_encode)
        buffer = BytesIO()
        buffer.write(encoder.get_imagedata(module_size))
        image = Image.open(buffer)
        return image

    def trim_barcode(self):
        """5x module size top
          10x module size left/right
        """
        barcode_width = self.barcode_image.size[0]
        cropped_image = self.barcode_image.crop((10*self.module_size,
                                                 5*self.module_size,
                                                 barcode_width-10*self.module_size,
                                                 5*self.module_size+10*self.module_size))
        return cropped_image

    def get_image(self):
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
