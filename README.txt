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

    >>> f = pycfitsio.open("debug/data.fits")

    >>> hdulist = f.HDUs

    >>> print(hdulist)
    OrderedDict([('DATA', HDU: DATA)])

    >>> hdu = f['DATA']

    >>> column_array = f['DATA'].read_column('signal')

    >>> all_columns = f['DATA'].read_all() 
    >>> print(all_columns)
    OrderedDict([('signal', array([   0., 1. ....])), 'flag', array([1, 1, ....])])

Writing    
_______

    >>> from collections import OrderedDict
    >>> f = pycfitsio.create('file.fits')

3 options to write HDUs:

#. list of (name, array) tuples

    >>> f.write_HDU('HDUNAME', 
            [('firstcolname', np.arange(10)), ('seccolname', np.arange(10)**2)]
          )

#. OrderedDict keys = name values = array    

    >>> data = OrderedDict()
    >>> data['firstcolname'] = np.arange(10)
    >>> data['seccolname'] = np.arange(10)**2
    >>> f.write_HDU('HDUNAME', data)

#. Compound numpy array

    >>> data = np.ones(10, dtype = [('firstcolname', np.long), ('seccolname', np.double)])
    >>> f.write_HDU('HDUNAME', data)

    >>> f.close()
