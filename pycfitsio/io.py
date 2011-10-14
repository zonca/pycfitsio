import numpy as np
import exceptions
try:
    from collections import OrderedDict
except exceptions.ImportError:
    from ordereddict import OrderedDict
from contextlib import closing
from ctypes import *

from decorator import cache

from constants import *
import ctypes.util

_cfitsio = CDLL(ctypes.util.find_library("cfitsio"))
if not _cfitsio._name: #temporary fix for planck
    _cfitsio = CDLL('/project/projectdirs/planck/user/zonca/software/lib/lib/libcfitsio.so')

class CfitsioError(exceptions.Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "CFITSIO error with code %d: %s" % (self.value, 
                ERRORMESSAGES.get(self.value, "Error code unknown"))

def open(filename, context_manager=True):
    """Opens fits file and returns a File object encapsulated in a context manager,
    so it should be called as:
    with open(filename) as f:
        print(f.HDUs)
    the file will be automatically closed at the exit from with"""
    f = File(str(filename))
    f.open()
    if context_manager:
        return closing(f)
    else:
        return f

def read(filename, HDU=0, return_header=False):
    """Quick function for reading one HDU and header

    HDU is name or index of HDU, default 0
    Returns the data array and a header dictionary"""

    with open(filename) as f:
        if return_header:
            return f[HDU].read_all(), f[HDU].header
        else:
            return f[HDU].read_all()


def create(filename):
    """Create a new fits file and returns a File object"""
    f = File(filename)
    f.create()
    return f

def check_status(status):
    if status.value != 0:
        raise CfitsioError(status.value)

def run_check_status(function, *args):
    status = c_int()
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

    def open(self):
        run_check_status(_cfitsio.ffopen, byref(self.ptr), self.filename, False)

    def create(self):
        run_check_status(_cfitsio.ffinit, byref(self.ptr), '!'+self.filename)

    def close(self):
        run_check_status(_cfitsio.ffclos, self.ptr)

    def __getitem__(self, key):
        """Returns HDU by name or index"""
        if isinstance(key, int):
            return self.HDUs.values()[key]
        else:
            return self.HDUs[key]

    @cache
    def HDUs(self):
        _HDUs = OrderedDict()
        hdunum = c_int()
        run_check_status(_cfitsio.ffthdu, self.ptr, byref(hdunum))
        hdutype = c_int()
        for i in range(2, hdunum.value+1):
            run_check_status(_cfitsio.ffmahd, self.ptr, c_int(i), byref(hdutype))
            hdu = HDU(i-2, file=self)
            _HDUs[hdu.name] = hdu
        return _HDUs

    def move(self, name):
        if self.current_HDU != name:
            if isinstance(name, int):
                hdutype = c_int(0)
                run_check_status(_cfitsio.ffmahd, self.ptr, c_int(name+2), byref(hdutype))
            elif name.startswith('HDU'):
                self.move(int(name[-1]))
            else:
                run_check_status(_cfitsio.ffmnhd, self.ptr, BINARY_TBL, name, False)
            self.current_HDU = name

    def read_all(self):
        """Read data from all extensions and generate a list of compound arrays"""
        return OrderedDict(
        (name, h.read_all()) for name, h in self.HDUs.iteritems()
        )

    def write_HDU(self, name, data):
        """There are 3 options for data storage:
           * list of (name, array) tuples
           * OrderedDict with key=name and value = array
           * coumpound array with named fields
           =NOTE= write_HDU makes the array contiguous, so this might involve copying all the data
        """
        if isinstance(data, list):
            data = OrderedDict(data)
        elif isinstance(data, np.ndarray):
            data = OrderedDict((name, data[name]) for name in data.dtype.names)
        for k, v in data.iteritems():
            data[k] = np.ascontiguousarray(v)
        keywords_t = c_char_p * len(data)
        ttype = keywords_t(*map(c_char_p, data.keys()))
        data_length = len(data.values()[0])
        tform = keywords_t(*[NP_TFORM[col.dtype.str[1:]] for col in data.values()])
        run_check_status(_cfitsio.ffcrtb, self.ptr, BINARY_TBL, c_longlong(0), c_int(len(data)), byref(ttype), byref(tform), None, c_char_p(name))
    
        buffer_size = c_long(1)
        run_check_status(_cfitsio.ffgrsz, self.ptr, byref(buffer_size))
    
        #print("Buffer size ");print(buffer_size)
        for k in range(0,len(data.values()[0]),buffer_size.value):
            if (k+buffer_size.value) > data_length:
                buffer_size = c_long(data_length - k)
            for i, (colname, colarray) in enumerate(data.iteritems()):
                np_dtype = colarray.dtype.str[1:]
                coltform = NP_TFORM[np_dtype]
                run_check_status(_cfitsio.ffpcl, self.ptr, TFORM_FITS[coltform], c_int(i+1), c_longlong(1+k), c_longlong(1), c_longlong(buffer_size.value), colarray[k:].ctypes.data_as(POINTER(TFORM_CTYPES[np_dtype])))

class HDU(object):

    def __init__(self, num=0, file=None):
        self.num = num
        self.file = file
        try:
            self.name = self.get_header_keyword("EXTNAME").strip()
        except CfitsioError:
            self.name = "HDU%d" % num

    #TODO implement self.file.move as a decorator
    #def move(self):
    #    def newf():
    #        self.file.move(self.name)

    def __repr__(self):
        return "HDU: %s" % self.name

    def get_header_key(self, name):
        self.file.move(self.num)
        value = c_long()
        run_check_status(_cfitsio.ffgky, self.file.ptr, TLONG, name, byref(value), False)
        return value.value

    def get_header_keyword(self, name):
        self.file.move(self.num)
        value = (c_char*150)()
        run_check_status(_cfitsio.ffgky, self.file.ptr, TSTRING, name, byref(value) , False)
        return value.value.strip()

    def read_column(self, num):
        self.file.move(self.num)
        if isinstance(num, str):
            num = self.column_names.index(num.upper())
        array = np.empty(self.length, dtype=self.dtype[num])
        run_check_status(_cfitsio.ffgcv, self.file.ptr, TFORM_FITS[self.fits_datatypes[num]], c_int(num+1), c_longlong(1), c_longlong(1), c_longlong(self.length), None, array.ctypes.data_as(POINTER(TFORM_CTYPES[self.dtype[num].str[1:]])), None)
        return array

    @property
    def column_names(self):
        return self.dtype.names

    @cache
    def length(self):
        self.file.move(self.name)
        length = self.get_header_key("NAXIS2")
        #check repeat
        tform = self.get_header_keyword("TFORM1")
        if len(tform) > 1:
            length *= long(tform[:-1])
        return length

    @cache
    def fits_datatypes(self):
        self.file.move(self.num)
        return [self.get_header_keyword("TFORM%d" % (num+1))[-1] for num in range(self.num_columns)]

    @cache
    def num_columns(self):
        self.file.move(self.num)
        return self.get_header_key("TFIELDS")

    @cache
    def header(self):
        self.file.move(self.num)
        keysexist, numkeys = c_int(0), c_int(0)
        run_check_status(_cfitsio.ffghsp, self.file.ptr, byref(keysexist), byref(numkeys))
        header = {}
        for i in range(1, keysexist.value+1):
            name = (c_char*150)()
            value = (c_char*150)()
            comment = (c_char*150)()
            run_check_status(_cfitsio.ffgkyn, self.file.ptr, c_int(i), byref(name), byref(value), byref(comment))
            header[name.value] = value.value.replace("'","").strip()
        return header

    @cache
    def dtype(self):
        self.file.move(self.num)
        data_dtype = []
        for num, fits_datatype in enumerate(self.fits_datatypes):
            if fits_datatype == 'S':
                tform = self.get_header_keyword("TFORM%d" % (num+1))
                if len(tform) > 1:
                    length = tform[:-1]
                else:
                    length = '' 
                data_dtype.append((self.get_header_keyword("TTYPE%d" % (num+1)).upper(), length + TFORM_NP[fits_datatype]))
            else:
                data_dtype.append((self.get_header_keyword("TTYPE%d" % (num+1)).upper(), TFORM_NP[fits_datatype]))
        return np.dtype(data_dtype)

    def read_all(self):
        """Read columns into ordered dict"""
        data = OrderedDict()
        for i, name in enumerate(self.column_names):
            data[name] = self.read_column(i)
        return data

if __name__ == '__main__':
    pass
    ##f = open("../test/data.fits")
    ##print(f.HDUs)
    ##print(f['DATA'])
    ##self=f[0]
    ##data = f["DATA"].read_column('signal')
    ##a = f[0].read_all()
    ##self = create('../test/newdata.fits')
    ##self.write_HDU('newdata',a)
    ##self.close()
    ##print(f[0].header)
    #all_data = f["DATA"].read_all()

    filename = '101003_ext.fits'
    with open(filename) as f:
        hdu_names = f.HDUs.keys()
        all = f.read_all()

    self = create('out.fits')
    name = 'A'
    data = all[0]
    self.write_HDU(name, data)
    self.close()
