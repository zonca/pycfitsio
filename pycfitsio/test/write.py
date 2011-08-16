from pycfitsio import *
import unittest
import numpy as np
from read import hdu_content
import os

def create_file(filename, data):
    f = create(filename)
    f.write_HDU("NEWDATA", data)
    f.close()

class TestPyCfitsIoWrite(unittest.TestCase):

    def setUp(self):
        self.filename = "testwrite.fits"
        try:
            os.remove(self.filename)
        except:
            pass

    def test_create(self):
        create_file(self.filename, hdu_content)
        self.assertTrue(os.path.exists(self.filename))

    def test_write(self):
        create_file(self.filename, hdu_content)
        with open(self.filename)  as f:
            data = f[0].read_all()
            self.assertTrue(isinstance(data, np.ndarray))
            self.assertEqual(f[0].name, "NEWDATA")
            for name in hdu_content.dtype.names:
                np.testing.assert_array_almost_equal(data[name.upper()], hdu_content[name])

    def tearDown(self):
        try:
            os.remove(self.filename)
        except:
            pass
