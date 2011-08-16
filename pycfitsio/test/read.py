import unittest
from pycfitsio import *
import numpy as np

hdu_content = np.empty(1000, dtype=np.dtype([
                                    ('signal', np.double),
                                    ('flag', np.uint8)
                                    ]))
hdu_content['signal'] = np.arange(1000)
hdu_content['flag'] = np.ones(1000)

class TestPyCfitsIoRead(unittest.TestCase):

    def setUp(self):
        self.filename = "../debug/data.fits"
        self.hdus = 1
        self.hduname = "DATA"
        self.len = 1000

    def test_open_file(self):
        with open(self.filename) as f:
            self.assertEqual(self.filename, f.filename)
            self.assertTrue(isinstance(f, File))

    def test_read_hdus(self):
        with open(self.filename) as f:
            hdus = f.HDUs
            self.assertEqual(len(hdus), 1)
            self.assertEqual(hdus.values()[0].name, self.hduname)
            self.assertEqual(f[0].name, self.hduname)
            self.assertEqual(hdus[self.hduname].name, self.hduname)

    def test_move(self):
        with open(self.filename) as f:
            f.move(f[0].name)
            self.assertEqual(f.current_HDU, self.hduname)

    def test_colnames(self):
        with open(self.filename) as f:
            self.assertEqual(f[0].column_names, hdu_content.dtype.names)


    def test_read_col(self):
        with open(self.filename) as f:
            h = f[0]
            for i, name in enumerate(hdu_content.dtype.names):
                np.testing.assert_array_almost_equal(h.read_column(i), hdu_content[name])
                np.testing.assert_array_almost_equal(h.read_column(name), hdu_content[name])

    def test_all_cols(self):
        with open(self.filename) as f:
            data = f[0].read_all()
            self.assertTrue(isinstance(data, np.ndarray))
            self.assertEqual(data.dtype.names, hdu_content.dtype.names)
            for name in hdu_content.dtype.names:
                np.testing.assert_array_almost_equal(data[name], hdu_content[name])

    def test_read(self):
        data, header = read(self.filename)
        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(data.dtype.names, hdu_content.dtype.names)
        for name in hdu_content.dtype.names:
            np.testing.assert_array_almost_equal(data[name], hdu_content[name])
