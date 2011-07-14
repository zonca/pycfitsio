from pycfitsio import *
import numpy as np
import os
import unittest

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
        f = open(self.filename)
        self.assertEqual(self.filename, f.filename)
        self.assertTrue(isinstance(f, File))

    def test_read_hdus(self):
        f = open(self.filename)
        hdus = f.HDUs
        self.assertEqual(len(hdus), 1)
        self.assertEqual(hdus.values()[0].name, self.hduname)
        self.assertEqual(f[0].name, self.hduname)
        self.assertEqual(hdus[self.hduname].name, self.hduname)

    def test_move(self):
        f = open(self.filename)
        f.move(f[0].name)
        self.assertEqual(f.current_HDU, self.hduname)

    def test_colnames(self):
        f = open(self.filename)
        self.assertEqual(f[0].column_names, hdu_content.dtype.names)


    def test_read_col(self):
        f = open(self.filename)
        h = f[0]
        for i, name in enumerate(hdu_content.dtype.names):
            np.testing.assert_array_almost_equal(h.read_column(i), hdu_content[name])
            np.testing.assert_array_almost_equal(h.read_column(name), hdu_content[name])

    def test_all_cols(self):
        f = open(self.filename)
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

if __name__ == '__main__':
    unittest.main()
