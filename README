============================================
pycfitsio: Python ctypes wrapper for cfitsio
============================================

Features
========

* read binary tables using hdu and column names into simple dictionaries of arrays
* write FITS files incrementally 1 HDU at a time

Requirements
============
pycfitsio requires the dynamic library cfitsio, in linux it usually packaged as libcfitsio-dev

Install
=======

    pip install pycfitsio #stable version

    # for development version clone from github and run
    python setup.py install

Examples
=======

Reading
_______

    f = pycfitsio.open("debug/data.fits")

    hdulist = f.HDUs

    print(hdulist)
    OrderedDict([('DATA', HDU: DATA)])

    hdu = f['DATA']

    column_array = f['DATA'].read_column('signal')

    #read columns as array with custom dtype
    all_columns = f['DATA'].read_all()
    print(all_columns)
    array([(0.0, 1), (1.0, 1), (2.0, 1), (3.0, 1), (4.0, 1), (5.0, 1),
       (6.0, 1), (7.0, 1), (8.0, 1), (9.0, 1), (10.0, 1), (11.0, 1),
       (12.0, 1), (13.0, 1), (14.0, 1), (15.0, 1), (16.0, 1), (17.0, 1),

       (992.0, 1), (993.0, 1), (994.0, 1), (995.0, 1), (996.0, 1),
       (997.0, 1), (998.0, 1), (999.0, 1)], 
       dtype=[('signal', '<f8'), ('flag', ' u1')])

    #read columns as OrderedDict of arrays
    all_columns = f['DATA'].read_all(asodict=True)
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
