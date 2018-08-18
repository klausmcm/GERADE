import os, sys
from PIL import Image, ImageDraw, ImageFont

class BarcodeLabel:

    def __init__( self, specs, id_variable, constants_module ):
        self.constants           = constants_module
        self.barcode_label_image = self.__generate_text_label( specs[ "recommended_font_size" ], specs[ "prefix" ], id_variable )

    def get_image( self ):
        return self.barcode_label_image

    def __generate_text_label( self, font_size, prefix, id_variable ):
        label_string = prefix + "•" + id_variable
        label_font   = ImageFont.truetype( self.constants.LABEL_FONT_PATH, font_size )
        img_size     = ImageDraw.Draw( Image.new( "RGB", ( 0, 0 ), "white" ) ).textsize( label_string, font=label_font )
        img          = Image.new( "RGB", img_size, "white" )
        draw         = ImageDraw.Draw( img )
        draw.text( ( 0, 0 ), label_string, fill="black", font=label_font )

        return img

