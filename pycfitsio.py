import numpy as np
import exceptions
from ctypes import *

_cfitsio = CDLL("libcfitsio.so")

class CfitsioError(exceptions.Exception):
#TODO implement verbose error messages
    pass

def open(filename):
    """Opens fits file and returns a File object"""
    f = File(filename)
    f.open()
    return f

def check_status(function):
    def inner_func(*args, **kwargs):
        status = c_int()
        function(*args, **kwargs)
        report_error(status)
    return inner_func

def report_error(status):
    if status != 0:
        raise CfitsioError("CFITSIO error with code %d" % status)

class File(object):

    def __init__(self, filename):
        self.ptr = c_voidp()
        self.filename = filename

    def open(self):
        _cfitsio.ffopen(byref(self.ptr), filename,False,byref(self.status))

class HDU(object):

    def __init__(self, name='', file=None):
        self.name = name
        self.file = file

    def read_column(self, name):
        return np.zeros(10)

    def read_all(self, name):
        return {'first':np.zeros(10), 'sec':np.zeros(20)}
