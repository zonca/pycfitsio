from pycfitsio import *
import unittest
import numpy as np
from read import hdu_content
import os

class TestPyCfitsIoWrite(unittest.TestCase):

    def setUp(self):
        self.filename = "../debug/newdata.fits"
        try:
            os.remove(self.filename)
        except:
            pass

    def test_create(self):
        f = create(self.filename)
        f.write_HDU("NEWDATA", hdu_content)
        f.close()
        self.assertTrue(isinstance(f, File))
        self.assertTrue(os.path.exists(self.filename))

    def test_write(self):
        fw = create(self.filename)
        fw.write_HDU("NEWDATA", hdu_content)
        fw.close()
        f = open(self.filename)
        data = f[0].read_all()
        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(f[0].name, "NEWDATA")
        for name in data.dtype.names:
            np.testing.assert_array_almost_equal(data[name], hdu_content[name])

    def test_repeat_tform(self):
        array = open('../debug/tform.fits')[0].read_column('data')
        np.testing.assert_array_almost_equal(array, np.arange(10000))

    def tearDown(self):
        try:
            os.remove(self.filename)
        except:
            pass
