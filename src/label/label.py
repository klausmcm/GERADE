import math
from PIL import Image, ImageDraw

class Label:
    def __init__(self, specs, barcode_object, barcode_label_object):
        self.specs = specs
        self.barcode = barcode_object
        self.barcode_label = barcode_label_object

        self.label_dimensions = self.__calculate_label_dimensions()
        self.label_image = Image.new("RGB", self.label_dimensions, "white")
        self.__draw_corner_trim_lines()
        self.__assemble_components()
        self.__draw_bounding_box()

    def save_to_file( self ):
        self.label_image.save( "_".join( [ self.specs[ "prefix" ], str( self.barcode.get_id_variable() ) ] ) + ".png" )

    def get_image( self ):
        return self.label_image

    def __calculate_label_dimensions( self ):
        label_length = max( [ self.barcode_label.get_image().size[ 0 ], self.barcode.get_image().size[ 0 ] + self.barcode_label.get_image().size[ 1 ] + self.barcode.get_module_size() ] ) + 2 * self.specs[ "margin" ]
        return ( round( label_length ), round( label_length ) )

    def __draw_corner_trim_lines( self ):
        line_width = 2
        to_trim              = math.sqrt( 2 * math.pow( self.specs[ "margin" ], 2 ) ) - self.specs[ "margin" ]
        diagonal_trim_length = 2 * to_trim * math.tan( math.radians( 45 ) )
        label_trim_length    = math.sqrt( math.pow( diagonal_trim_length, 2 )/2 )
        draw                 = ImageDraw.Draw( self.label_image )

        draw.line( [ ( label_trim_length, 0 ), ( 0, label_trim_length ) ], fill="black", width=line_width )
        draw.line( [ ( self.label_image.size[ 0 ] - label_trim_length, 0 ), 
                    ( self.label_image.size[ 0 ], label_trim_length ) ], fill="black", width=line_width )
        draw.line( [ ( self.label_image.size[ 0 ], self.label_image.size[ 0 ] - label_trim_length ), 
                    ( self.label_image.size[ 0 ] - label_trim_length, self.label_image.size[ 0 ] ) ], 
                  fill="black", width=line_width )
        draw.line( [ ( 0, self.label_image.size[ 0 ] - label_trim_length ), 
                    ( label_trim_length, self.label_image.size[ 0 ] ) ], fill="black", width=line_width )

        return

    def __assemble_components( self ):
        top_y = round( ( self.label_image.size[ 1 ] - ( self.barcode.get_image().size[ 1 ] + self.barcode_label.get_image().size[ 1 ] + self.barcode.get_module_size() ) ) / 2 )
        barcode_label_coordinates = ( round( ( self.label_image.size[ 0 ] - self.barcode_label.get_image().size[ 0 ] ) / 2 ), top_y )
        barcode_coordinates = ( round( ( self.label_image.size[ 0 ] - self.barcode.get_image().size[ 0 ] ) / 2 ), 
                               round( top_y + 
                                     self.barcode_label.get_image().size[ 1 ] + 
                                     self.barcode.get_module_size() ) )
        self.label_image.paste( self.barcode.get_image(), barcode_coordinates )
        self.label_image.paste( self.barcode_label.get_image(), barcode_label_coordinates )

        return

    def __draw_bounding_box( self ):
        template = Image.new( "RGB", ( self.label_image.size[ 0 ] + 2, self.label_image.size[ 1 ] + 2 ), "black" )
        template.paste( self.label_image, ( 1, 1 ) )
        self.label_image = template
        return


