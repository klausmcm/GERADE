import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class LabelComponentText:
    def __init__(self, text, font_size):
        self.text = text
        self.font_size = font_size
        self.text_image = self._get_text_as_image(text, font_size)
        
    def get_image(self):
        return self.text_image

    def _get_text_as_image(self, text, font_size):
        """
        """
        if font_size <= 0:
            return Image.new("RGB", (0, 0), "white")
        else:
            label_font = ImageFont.truetype("/media/sf_shared/workspace/barcode/files/DejaVuSansMono.ttf", 
                                            font_size)
            image_width = ImageDraw.Draw(Image.new("RGB", (0, 0), "white")).textsize(text, font=label_font)[0]
            image_height = ImageDraw.Draw(Image.new("RGB", (0, 0), "white")).textsize(string.ascii_letters + string.digits, font=label_font)[1]
            
            lines = text.split("\n")
            
            img = Image.new("RGB",
                            (image_width, len(lines)*image_height),
                            "white")
            for i in range(len(lines)):
                image_line = Image.new("RGB",
                                       (image_width, image_height),
                                       "white")
                draw = ImageDraw.Draw(image_line)
                draw.text((0, 0),
                          lines[i],
                          fill="black",
                          font=label_font)
                img.paste(image_line, (0, i*image_height))
            return img
