import unittest
from read import *
from write import *

class TestError(unittest.TestCase):

    def test_error(self):
        
        self.assertRaises(CfitsioError, open, 'unexisting_file.fits')
        self.assertRaisesRegexp(CfitsioError, 'could not open',
                        open, 'unexisting_file.fits')

if __name__ == '__main__':
    unittest.main()
