from pycfitsio import *
from collections import OrderedDict
import unittest
import numpy as np
from read import hdu_content
import os

def create_file(filename, data):
    with create(filename) as f:
        f.write_HDU("NEWDATA", data)

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
            self.assertIsInstance(data, OrderedDict)
            self.assertEqual(f[0].name, "NEWDATA")
            for name in hdu_content.dtype.names:
                np.testing.assert_array_almost_equal(data[name.upper()], hdu_content[name])

    def test_write_tuplist(self):
        tuplist = [(name, np.ascontiguousarray(hdu_content[name])) for name in hdu_content.dtype.names]
        create_file(self.filename, tuplist)
        with open(self.filename)  as f:
            data = f[0].read_all()
            self.assertIsInstance(data, OrderedDict)
            self.assertEqual(f[0].name, "NEWDATA")
            for name in hdu_content.dtype.names:
                np.testing.assert_array_almost_equal(data[name.upper()], hdu_content[name])

    def test_write_odict(self):
        tuplist = [(name, np.ascontiguousarray(hdu_content[name])) for name in hdu_content.dtype.names]
        odict = OrderedDict(tuplist)
        create_file(self.filename, odict)
        with open(self.filename)  as f:
            data = f[0].read_all()
            self.assertIsInstance(data, OrderedDict)
            self.assertEqual(f[0].name, "NEWDATA")
            for name in hdu_content.dtype.names:
                np.testing.assert_array_almost_equal(data[name.upper()], hdu_content[name])


    def tearDown(self):
        try:
            os.remove(self.filename)
        except:
            pass
