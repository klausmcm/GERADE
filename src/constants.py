from pint import UnitRegistry
import os

#=========================================================================
# conversion of 600 dpi to dots/mm (ie. pixels/mm)
# 600 dpi used because of printer's capability
#=========================================================================

LABEL_FONT_PATH = ( os.path.join( os.getcwd(), "files", "DejaVuSansMono.ttf" ) )
BARCODE_MARGIN  = 1

DPI  = 600
DPMM = DPI / ( 1 * UnitRegistry().inch ).to( UnitRegistry().mm ).magnitude

# LARGE_BARCODE_SPECS = { "prefix":"6a49b879" , "module_size":20 , "side_length":360 , "max_string_length":17 }
SMALL_LABEL_SPECS = { "prefix":"d9g3", "max_string_length":8  }

# LARGE_BARCODE_SPECS[ "margin" ] = 2 * 600 * ( 1 * UnitRegistry().mm ).to( UnitRegistry().inch ).magnitude
SMALL_LABEL_SPECS[ "margin" ] = 2 * DPMM
# LARGE_BARCODE_SPECS[ "barcode_label_margin" ] = LARGE_BARCODE_SPECS[ "module_size" ]
SMALL_LABEL_SPECS[ "recommended_font_size" ] = 40

PAPER = { "A4":{ "width":210 * DPMM, "height":297 * DPMM, "margin":10 * DPMM }, 
         "letter":{ "width":8.5 * DPI, "height": 11 * DPI, "margin":10 * DPMM }, 
         "sticker":{ "width":104 * DPMM, "height":156 * DPMM, "margin":5 * DPMM } }

TAPE_SPECS = { "width":19 * DPMM }

