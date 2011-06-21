from __init__ import *
import os
import unittest

hdu_content = OrderedDict()
hdu_content['signal'] = np.arange(1000)
hdu_content['flag'] = np.ones(1000, dtype=np.uint8)


class TestPyCfitsIoRead(unittest.TestCase):

    def setUp(self):
        self.filename = "../test/data.fits"
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
        self.assertEqual(f[0].column_names, hdu_content.keys())

    def test_read_col(self):
        f = open(self.filename)
        h = f[0]
        for i, (name, array) in enumerate(hdu_content.iteritems()):
            np.testing.assert_array_almost_equal(h.read_column(i), array)
            np.testing.assert_array_almost_equal(h.read_column(name), array)

    def test_all_cols(self):
        f = open(self.filename)
        all = f[0].read_all()
        self.assertTrue(isinstance(all, OrderedDict))
        self.assertEqual(all.keys(), hdu_content.keys())
        for name, array in hdu_content.iteritems():
            np.testing.assert_array_almost_equal(all[name], array)

class TestPyCfitsIoWrite(unittest.TestCase):

    def setUp(self):
        self.filename = "../test/newdata.fits"
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
        all = f[0].read_all()
        self.assertTrue(isinstance(all, OrderedDict))
        self.assertEqual(all.keys(), hdu_content.keys())
        self.assertEqual(f[0].name, "NEWDATA")
        for name, array in hdu_content.iteritems():
            np.testing.assert_array_almost_equal(all[name], array)

if __name__ == '__main__':
    unittest.main()
