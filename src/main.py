'''
@author: Klaus
'''
# from page import Page
from label.barcode import LabelComponentBarcode
from label.label import Label
from label.barcode_label import LabelComponentText
from page import Page
from pint import UnitRegistry
import label.id as id
import constants
import analysis

if __name__ == "__main__":
    module_size = analysis.get_module_size( constants.SMALL_LABEL_SPECS )
    for k in range( 3 ):
        barcode       = LabelComponentBarcode( constants.SMALL_LABEL_SPECS, module_size, "aaaa", constants )
        barcode_label = LabelComponentText( constants.SMALL_LABEL_SPECS, "aaaa", constants )
        label         = Label( constants.SMALL_LABEL_SPECS, barcode, barcode_label )
        page          = Page( constants.PAPER[ "sticker" ], constants.TAPE_SPECS )
        page.init_page( label )

        for i in range( len( page.get_grid_coordinates() ) ):
            id_var        = id.get_next_available_id()[ "id_variable" ]
            barcode       = LabelComponentBarcode( constants.SMALL_LABEL_SPECS, module_size, id_var, constants )
            barcode_label = LabelComponentText( constants.SMALL_LABEL_SPECS, id_var, constants )
            label         = Label( constants.SMALL_LABEL_SPECS, barcode, barcode_label )
            page.paste_label_without_coordinates( label )
            id.deactivate_entry( id_var )
        page.create_letter_page()
        page.save_page_to_file( id_var )

