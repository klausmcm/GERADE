import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class LabelComponentText:
    def __init__(self, text, font_size, file_path_true_type_font=""):
        """
        """
        def _get_text_as_image(text, font_size):
            """
            """
            if font_size <= 0:
                return Image.new("RGB", (0, 0), "white")
            else:
                if file_path_true_type_font != "":
                    label_font = ImageFont.truetype(file_path_true_type_font, font_size)
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
        self.text_encoded = text
        self.font_size = font_size
        self.text_image = _get_text_as_image(text, font_size)
        
    def get_image(self):
        return self.text_image
    
    def add_white_border(self, border_thickness):
        image = Image.new("RGB",
                          (self.text_image.size[0] + 2*border_thickness,
                           self.text_image.size[1] + 2*border_thickness),
                          "white")
        image.paste(self.text_image, (border_thickness, border_thickness))
        self.text_image = image
        return
