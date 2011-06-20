import numpy as np
import exceptions
from collections import OrderedDict
from ctypes import *

_cfitsio = CDLL("libcfitsio.so")

TSTRING = 16

class CfitsioError(exceptions.Exception):
#TODO verbose error messages
    pass

def open(filename):
    """Opens fits file and returns a File object"""
    f = File(filename)
    f.open()
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

    def open(self):
        run_check_status(_cfitsio.ffopen,byref(self.ptr), self.filename, False)

    def write(self):
        raise exceptions.NotImplementedError()

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
            name = c_char_p(" "*50)
            run_check_status(_cfitsio.ffgky, self.ptr, TSTRING, "EXTNAME", name , False)
            hdu_name = name.value
            hdu_name.strip()
            self._HDUs[hdu_name] = HDU(hdu_name)

class HDU(object):

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return "HDU: %s" % self.name

    def read_column(self, name):
        return np.zeros(10)

    def read_all(self):
        return {'first':np.zeros(10), 'sec':np.zeros(20)}

if __name__ == '__main__':
    f = open("test/data.fits")
    print(f.HDUs)
    #data = f["DATA"].read_column('signal')
    #data = f[1].read_column(0)
    #all_data = f["DATA"].read_all()
