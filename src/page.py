'''
@author: Klaus
'''

import os
import math
from PIL import Image, ImageDraw
from pint import UnitRegistry

import constants


class Page():

    # TODO    want to be able to place a single barcode onto
    #            the template (by specifying the barcodes data and
    #            position on the template)
    #            ex.
    #                template.place_single_barcode(Barcode(124), 3)
    #                -> placing barcode 124 at position 3

    def __init__(self, file_path_template):
        pass

#     def __init__( self, paper_specs, tape_specs ):
#         '''
#         Constructor
#         paper_type is currently set to "default" representing the currently
#         only available measurements.
#         tape_width (mm) is reflecting current available tape.
#         
#         :param paper_type:
#             Currently only "default" creates a usable template. No other
#             paper types are set up.
#         :param tape_width:
#             Given in mm.
#         '''
#         self.tape_width_px     = int( round( tape_specs[ "width" ] ) )
#         self.page_width_px     = int( round( paper_specs[ "width" ] ) )
#         self.page_height_px    = int( round( paper_specs[ "height" ] ) )
#         self.margin_length_px  = int( round( paper_specs[ "margin" ] ) )
#         self.buffer_distance   = int( round( ( 2 * UnitRegistry().mm ).magnitude * constants.DPMM ) )
#         self.page_image        = Image.new( "RGB", ( self.page_width_px, self.page_height_px ), "white" )
#         self.label_coordinates = []

    def get_grid_dimensions( self ):
        # TODO
        return

    def get_grid_coordinates( self ):
        return self.label_coordinates

    def init_page( self, label ):
        self.__draw_margin()
        self.__generate_grid_coordinates( label.get_image() )
        return

    def has_page_room( self ):
        return len( self.label_coordinates ) > 0

    def paste_label_with_coordinates( self, label_image, coordinates ):
        self.page_image.paste( label, coordinates )
        return

    def paste_label_without_coordinates( self, label ):
        coordinates = self.label_coordinates.pop()
        self.page_image.paste( label.get_image(), coordinates )
        return

    def create_letter_page( self ):
        letter = Image.new( "RGB", ( round( constants.PAPER[ "letter" ][ "width" ] ), round( constants.PAPER[ "letter" ][ "height" ] ) ), "white" )
        letter.paste( self.page_image, ( round( ( letter.size[ 0 ]/2 ) - ( self.page_image.size[ 0 ]/2 ) ), 0 ) )
        self.page_image = letter

    def __draw_margin( self ):
        draw     = ImageDraw.Draw( self.page_image )
        left_x   = self.margin_length_px
        right_x  = self.page_width_px - self.margin_length_px - 1
        top_y    = self.margin_length_px
        bottom_y = self.page_height_px - self.margin_length_px - 1
        draw.line( [ ( left_x, top_y ), ( right_x, top_y ), ( right_x, bottom_y ), ( left_x, bottom_y ), ( left_x, top_y ) ], fill="black", width=1 )
        return

    def __generate_grid_coordinates( self, label_image ):
        initial_x = self.margin_length_px
        initial_y = self.margin_length_px
        last_x    = self.page_width_px - self.margin_length_px - label_image.size[ 0 ] - 1
        last_y    = self.page_height_px - self.margin_length_px - label_image.size[ 0 ] - 1
        column_spacing = int( round( ( self.tape_width_px + self.buffer_distance - label_image.size[ 0 ] ) / 2 ) ) + label_image.size[ 0 ]
        row_spacing    = label_image.size[ 0 ] - 1

        coordinates         = ( initial_x, initial_y, )
        label_coordinates   = []

        while ( coordinates[ 0 ] < last_x ):
            while ( coordinates[ 1 ] < last_y ):
                label_coordinates.append( ( coordinates[ 0 ], coordinates[ 1 ] ) )
                coordinates = ( coordinates[ 0 ], coordinates[ 1 ] + row_spacing )
            coordinates = ( coordinates[ 0 ] + column_spacing, initial_y )

        self.label_coordinates = label_coordinates

        return 

    def save_page_to_file( self, name ):
        '''
        Write template image to an image file.
        '''
        src_dir = os.getcwd()
        os.chdir( '..' )
        self.page_image.save( os.path.join( os.getcwd(), "files", "output",
                                              name + ".png" ), "PNG",
                             dpi=( constants.DPI, constants.DPI ) )
        os.chdir( src_dir )

