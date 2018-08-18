from label.barcode import Barcode
from label.barcode_label import  BarcodeLabel
import constants
import sqlite3

def get_module_size( label_specs ):
    chosen_module_size        = float( "inf" )
    smallest_ratio_difference = float( "inf" )
    current_ratio             = float( "inf" )
    variable_id_length        = label_specs[ "max_string_length" ] - len( label_specs[ "prefix" ] )
    variable_id_sample        = "".join( [ "a" for i in range( variable_id_length ) ] )

    for i in range( 100 ):
        module_size = i+1
        b_img = Barcode( label_specs, module_size, variable_id_sample, constants ).get_image()
        l_img = BarcodeLabel( label_specs, variable_id_sample, constants ).get_image()
        height = b_img.size[ 1 ] + l_img.size[ 1 ] + module_size
        width  = l_img.size[ 0 ]
        ratio_diff  = abs( ( height / width ) - 1 )
        if ratio_diff < smallest_ratio_difference:
            smallest_ratio_difference = ratio_diff
            chosen_module_size = module_size
        elif ratio_diff > smallest_ratio_difference:
            return chosen_module_size
    return

