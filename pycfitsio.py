import numpy as np
import exceptions
from ctypes import *

_cfitsio = CDLL("libcfitsio.so")

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

class HDU(object):

    def __init__(self, name='', file=None):
        self.name = name
        self.file = file

    def read_column(self, name):
        return np.zeros(10)

    def read_all(self, name):
        return {'first':np.zeros(10), 'sec':np.zeros(20)}

if __name__ == '__main__':
    f = open("test/data.fits")
