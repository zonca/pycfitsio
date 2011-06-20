import numpy as np
from ctypes import *

BINARY_TBL = c_int(2)
TLONG = c_int(41)
TDOUBLE = c_int(82)
_cfitsio = CDLL("libcfitsio.so")
ptr = c_voidp()
length = c_long()
status = c_int()
_cfitsio.ffopen(byref(ptr), "data.fits",False,byref(status))
_cfitsio.ffmnhd(ptr, BINARY_TBL, "DATA", 0, byref(status))
_cfitsio.ffgky(ptr, TLONG, "NAXIS2", byref(length) , False, byref(status))
anynul = c_int()
colnum = 1
data = np.zeros(10, order='C',dtype=np.double)
#datatype = c_double * 10
#data = datatype()
doublenull = c_double()
_cfitsio.ffgcv(ptr, TDOUBLE, c_int(1), c_longlong(1), c_longlong(1), c_longlong(10), byref(doublenull), data.ctypes.data_as(POINTER(c_double)), byref(anynul), status=byref(status))
#_cfitsio.ffgcv(ptr, TDOUBLE, c_int(1), c_int(1), c_int(1), c_int(5), byref(doublenull), data, byref(anynul), byref(status))
print(length)
print(data[4])
print(status)
