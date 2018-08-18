'''
@author: Klaus
'''

import os, subprocess
from io import StringIO, BytesIO
from PIL import Image, ImageDraw, ImageFont
from .barcode_label import BarcodeLabel

class Barcode:

    def __init__( self, label_specs, module_size, id_variable, constants_module ):
        self.constants     = constants_module
        self.id_variable   = id_variable
        self.data_prefix   = label_specs[ "prefix" ]
        self.barcode_image = Image
        self.module_size   = module_size
        self.__set_barcode_image()
        self.__trim_margins()

    def get_image( self ):
        return self.barcode_image

    def get_module_size( self ):
        return self.module_size

    def get_id_variable( self ):
        return self.id_variable

    def __trim_margins( self ):
        self.barcode_image = self.barcode_image.crop( ( self.constants.BARCODE_MARGIN,
                                                       self.constants.BARCODE_MARGIN,
                                                       self.barcode_image.size[ 0 ]-1,
                                                       self.barcode_image.size[ 1 ]-1 ) )

    def __set_barcode_image( self ):
        barcode_data = self.data_prefix + str( self.id_variable )
        arg1 = "--module=" + str( self.module_size )
        arg2 = "--margin=" + str( self.constants.BARCODE_MARGIN )
        arg3 = "--resolution=" + str( self.constants.DPI )
        arg4 = "--symbol-size=s"
        arg5 = "--encoding=t"
        #======================================================================
        # TODO:    tricky things going on here - study it in detail
        # https://stackoverflow.com/questions/15975714/create-image-object-from-image-stdout-output-of-external-program-in-python
        # p1 = subprocess.Popen(["echo", barcode_data], stdout=subprocess.PIPE)
        # p2 = subprocess.Popen(["dmtxwrite", arg1, arg2, arg3, arg4],
        # stdin=p1.stdout, stdout=subprocess.PIPE)
        # raw = p2.stdout.read()
        # buff = StringIO.StringIO()
        # buff.write(raw)
        # buff.seek(0)
        # self.barcode_image = Image.open(buff)
        #======================================================================
        p1 = subprocess.Popen( [ "echo", barcode_data ], stdout=subprocess.PIPE )
        p2 = subprocess.Popen( [ "dmtxwrite", arg1, arg2, arg3, arg4, arg5 ], stdin=p1.stdout, stdout=subprocess.PIPE )
        raw = p2.stdout.read()
        buff = BytesIO()
        buff.write( raw )
        buff.seek( 0 )
        self.barcode_image = Image.open( buff )
        self.barcode_image = self.barcode_image.convert( "RGB" )

    def save_to_file( self ):
        '''
        Save barcode to a png file.
        '''
        src_dir = os.getcwd()
        os.chdir( '..' )
        out_dir = os.path.join( os.getcwd(), "files", "output", "DMTX_" )
        self.barcode_image.save( out_dir + str( self.id_variable ) + ".png",
                                "PNG",
                                dpi=( self.constants.DPI, self.constants.DPI ) )
        os.chdir( src_dir )
