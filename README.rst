============================================
pycfitsio: Python ctypes wrapper for cfitsio
============================================

Features
========

* read binary tables using hdu and column names into simple dictionaries of arrays
* write FITS files incrementally 1 HDU at a time

Examples
=======

Reading
_______

    f = pycfitsio.open("test/data.fits")

    hdulist = f.HDUs

    print(hdulist)
    OrderedDict([('DATA', HDU: DATA)])

    hdu = f['DATA']

    column_array = f['DATA'].read_column('signal')

    all_columns = f['DATA'].read_all()
    print(all_columns)
    OrderedDict([('signal', array([   0., 1. ....])), 'flag', array([1, 1, ....])])

Writing    
_______

    from collections import OrderedDict
    f = pycfitsio.create('file.fits')
    f.write_HDU_dict('OBT', OrderedDict(
          OBT=np.arange(100)
          ))
    f.write_HDU_dict('LFI27M', OrderedDict(
          LFI27M=np.arange(100, dtype=np.double)
          ))
    f.write_HDU_dict('PID', OrderedDict(
          PID=np.arange(1000, dtype=np.uint8)
          ))
    f.close()
