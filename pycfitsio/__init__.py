import numpy as np
import exceptions
from collections import OrderedDict

from ctypes import *
from constants import *

_cfitsio = CDLL("libcfitsio.so")

class CfitsioError(exceptions.Exception):
#TODO verbose error messages
    pass

def open(filename):
    """Opens fits file and returns a File object"""
    f = File(filename)
    f.open()
    return f

def create(filename):
    """Create a new fits file and returns a File object"""
    f = File(filename)
    f.create()
    return f

def check_status(status):
    if status.value != 0:
        raise CfitsioError("CFITSIO error with code %d" % status.value)

def run_check_status(function, *args):
    status = c_long()
    args = list(args)
    args.append(byref(status))
    function(*args)
    check_status(status)

class File(object):

    def __init__(self, filename):
        self.ptr = c_voidp()
        self.filename = filename
        self.current_HDU = None

    def __repr__(self):
        return "Fits FILE: %s" % self.filename

    def get_header_key(self, name):
        value = c_long()
        run_check_status(_cfitsio.ffgky, self.ptr, TLONG, name, byref(value), False)
        return value.value

    def get_header_keyword(self, name):
        value = (c_char*50)()
        run_check_status(_cfitsio.ffgky, self.ptr, TSTRING, name, byref(value) , False)
        return value.value.strip()

    def open(self):
        run_check_status(_cfitsio.ffopen, byref(self.ptr), self.filename, False)

    def create(self):
        run_check_status(_cfitsio.ffinit, byref(self.ptr), '!'+self.filename)

    def close(self):
        run_check_status(_cfitsio.ffclos, self.ptr)

    @property
    def HDUs(self):
        try:
            return self._HDUs
        except exceptions.AttributeError:
            self.read_HDUs()
            return self.HDUs

    def __getitem__(self, key):
        """Returns HDU by name or index"""
        if isinstance(key, int):
            return self.HDUs.values()[key]
        else:
            return self.HDUs[key]

    def read_HDUs(self):
        self._HDUs = OrderedDict()
        hdunum = c_int()
        run_check_status(_cfitsio.ffthdu, self.ptr, byref(hdunum))
        hdutype = c_int()
        for i in range(2, hdunum.value+1):
            run_check_status(_cfitsio.ffmahd, self.ptr, c_int(i), byref(hdutype))
            hdu_name = self.get_header_keyword("EXTNAME")
            hdu_name.strip()
            self._HDUs[hdu_name] = HDU(hdu_name, file=self)

    def move(self, name):
        if self.current_HDU != name:
            run_check_status(_cfitsio.ffmnhd, self.ptr, BINARY_TBL, name, False)
            self.current_HDU = name

    def write_HDU(self, name, data):
        """Data must be an OrderedDict of arrays"""
        keywords_t = c_char_p * len(data)
        ttype = keywords_t(*map(c_char_p, data.keys()))
        tform = keywords_t(*[NP_TFORM[col.dtype.str[1:]] for col in data.values()])
        run_check_status(_cfitsio.ffcrtb, self.ptr, BINARY_TBL, c_longlong(0), c_int(len(data)), byref(ttype), byref(tform), 0, c_char_p(name))
        for i, (colname, colarray) in enumerate(data.iteritems()):
            coltform = NP_TFORM[colarray.dtype.str[1:]]
            run_check_status(_cfitsio.ffpcl, self.ptr, TFORM_FITS[coltform], c_int(i+1), c_longlong(1), c_longlong(1), c_longlong(len(colarray)), colarray.ctypes.data_as(POINTER(TFORM_CTYPES[coltform])))

class HDU(object):

    def __init__(self, name='', file=None):
        self.name = name
        self.file = file

    def __repr__(self):
        return "HDU: %s" % self.name

    def read_column(self, num):
        self.file.move(self.name)
        if isinstance(num, str):
            num = self.column_names.index(num)
        length = self.file.get_header_key("NAXIS2")
        fits_datatype = self.file.get_header_keyword("TFORM%d" % (num+1))[-1]

        array = np.empty(length, dtype=TFORM_NP[fits_datatype])
        run_check_status(_cfitsio.ffgcv, self.file.ptr, TFORM_FITS[fits_datatype], c_int(num+1), c_longlong(1), c_longlong(1), c_longlong(length), False, array.ctypes.data_as(POINTER(TFORM_CTYPES[fits_datatype])), False)
        return array

    @property
    def column_names(self):
        try:
            return self._column_names
        except exceptions.AttributeError:
            self.read_column_names()
            return self.column_names

    def read_column_names(self):
        self.file.move(self.name)
        num_columns = self.file.get_header_key("TFIELDS")
        self._column_names = [self.file.get_header_keyword("TTYPE%d" % (i+1)) for i in range(num_columns)]

    def read_all(self):
        all = OrderedDict()
        for i, name in enumerate(self.column_names):
            all[name] = self.read_column(i)
        return all



if __name__ == '__main__':
    f = open("../test/data.fits")
    print(f.HDUs)
    print(f['DATA'])
    self=f[0]
    #data = f["DATA"].read_column('signal')
    a = f[0].read_all()
    self = create('../test/newdata.fits')
    self.write_HDU('newdata',a)
    self.close()
    #all_data = f["DATA"].read_all()
    
