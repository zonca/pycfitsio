import numpy as np
from ctypes import *

TSTRING = c_int(16)
TLOGICAL   = c_int( 14)
TBYTE      = c_int( 11)
TSTRING    = c_int( 16)
TUSHORT    = c_int( 20)
TSHORT     = c_int( 21)
TUINT      = c_int( 30)
TINT       = c_int( 31)
TULONG     = c_int( 40)
TLONG      = c_int( 41)
TFLOAT     = c_int( 42)
TLONGLONG  = c_int( 81)
TDOUBLE    = c_int( 82)
TCOMPLEX   = c_int( 83)
TDBLCOMPLEX= c_int(163)


BINARY_TBL = c_int(2)


TFORM_NP = {'L': 'i1', 'B': 'u1', 'I': 'i2', 'J': 'i4', 'K': 'i8', 'E': 'f4',
              'D': 'f8', 'C': 'c8', 'M': 'c16', 'A': 'a'}

TFORM_FITS = {
    'L':TLOGICAL,
    'B':TBYTE,
    'I':TSHORT,
    'J':TLONG,
    'K':TLONGLONG,
    'E':TFLOAT,
    'D':TDOUBLE,
    'C':TCOMPLEX,
    'M':TDBLCOMPLEX,
    'A':TSTRING
}

TFORM_CTYPES = {
    'L':c_bool, 
    'B':c_uint8, 
    'I':c_int16, 
    'J':c_int32, 
    'K':c_int64, 
    'E':c_float, 
    'D':c_double, 
    'A':c_char,
    'C':None,
    'M':None
}
