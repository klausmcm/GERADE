import unittest
import Image
import ImageDraw
from barcode import LabelComponentBarcode
from template import Template


class TestBarcode(unittest.TestCase):

    def test_set_barcode_coordinates(self):
        barcode = LabelComponentBarcode(1)
        x_coordinates = [119, 556, 993, 1430, 1867]
        for i in range(1, 6):
            barcode.set_barcode_coordinates(i)
            self.assertEqual(barcode.get_coordinates(), 
                             (x_coordinates[i - 1], 119))
        for i in range(6, 11):
            barcode.set_barcode_coordinates(i)
            self.assertEqual(barcode.get_coordinates(), 
                             (x_coordinates[i - 6], 520))
        for i in range(11, 16):
            barcode.set_barcode_coordinates(i)
            self.assertEqual(barcode.get_coordinates(), 
                             (x_coordinates[i - 11], 921))
        for i in range(16, 21):
            barcode.set_barcode_coordinates(i)
            self.assertEqual(barcode.get_coordinates(), 
                             (x_coordinates[i - 16], 1322))
        for i in range(21, 26):
            barcode.set_barcode_coordinates(i)
            self.assertEqual(barcode.get_coordinates(), 
                             (x_coordinates[i - 21], 1723))
        for i in range(26, 31):
            barcode.set_barcode_coordinates(i)
            self.assertEqual(barcode.get_coordinates(), 
                             (x_coordinates[i - 26], 2124))
        for i in range(31, 36):
            barcode.set_barcode_coordinates(i)
            self.assertEqual(barcode.get_coordinates(), 
                             (x_coordinates[i - 31], 2525))
        for i in range(36, 41):
            barcode.set_barcode_coordinates(i)
            self.assertEqual(barcode.get_coordinates(), 
                             (x_coordinates[i - 36], 2926))

class TestTemplate(unittest.TestCase):
    
    def test_set_template_margins(self):
        template = Template()
        
#=========================================================================
# if __name__ == '__main__':
#     unittest.main()
#=========================================================================
