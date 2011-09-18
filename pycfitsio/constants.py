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
              'D': 'f8', 'C': 'c8', 'M': 'c16', 'A': 'S'}

NP_TFORM = dict([[v,k] for k,v in TFORM_NP.items()])

TFORM_FITS = {
    'L':TLOGICAL,
    'B':TBYTE,
    'I':TSHORT,
    'J':TINT,
    'K':TLONG,
    'E':TFLOAT,
    'D':TDOUBLE,
    'C':TCOMPLEX,
    'M':TDBLCOMPLEX,
    'A':TSTRING
}

TFORM_CTYPES = {
    'u1':c_uint8, 
    'i2':c_int16, 
    'i4':c_int32, 
    'i8':c_int64, 
    'f4':c_float, 
    'f8':c_double, 
    'c8':None,
    'c16':None
}

ERRORMESSAGES = {
101  : "input and output files are the same ",
103  : "tried to open too many FITS files ",
104  : "could not open the named file ",
105  : "could not create the named file ",
106  : "error writing to FITS file ",
107  : "tried to move past end of file ",
108  : "error reading from FITS file ",
110  : "could not close the file ",
111  : "array dimensions exceed internal limit ",
112  : "Cannot write to readonly file ",
113  : "Could not allocate memory ",
114  : "invalid fitsfile pointer ",
115  : "NULL input pointer to routine ",
116  : "error seeking position in file ",
121  : "invalid URL prefix on file name ",
122  : "tried to register too many IO drivers ",
123 : "driver initialization failed ",
124 : "matching driver is not registered ",
125 : "failed to parse input file URL ",
126 : "failed to parse input file URL ",
201  : "header already contains keywords ",
202  : "keyword not found in header ",
203  : "keyword record number is out of bounds ",
204  : "keyword value field is blank ",
205  : "string is missing the closing quote ",
206  : "illegal indexed keyword name ",
207  : "illegal character in keyword name or card ",
208  : "required keywords out of order ",
209  : "keyword value is not a positive integer ",
210  : "couldn't find END keyword ",
211  : "illegal BITPIX keyword value",
212  : "illegal NAXIS keyword value ",
213  : "illegal NAXISn keyword value ",
214  : "illegal PCOUNT keyword value ",
215  : "illegal GCOUNT keyword value ",
216  : "illegal TFIELDS keyword value ",
217  : "negative table row size ",
218  : "negative number of rows in table ",
219  : "column with this name not found in table ",
220  : "illegal value of SIMPLE keyword  ",
221  : "Primary array doesn't start with SIMPLE ",
222  : "Second keyword not BITPIX ",
223  : "Third keyword not NAXIS ",
224  : "Couldn't find all the NAXISn keywords ",
225  : "HDU doesn't start with XTENSION keyword ",
226  : "the CHDU is not an ASCII table extension ",
227  : "the CHDU is not a binary table extension ",
228  : "couldn't find PCOUNT keyword ",
229  : "couldn't find GCOUNT keyword ",
230  : "couldn't find TFIELDS keyword ",
231  : "couldn't find TBCOLn keyword ",
232  : "couldn't find TFORMn keyword ",
233  : "the CHDU is not an IMAGE extension ",
234  : "TBCOLn keyword value < 0 or > rowlength ",
235  : "the CHDU is not a table ",
236  : "column is too wide to fit in table ",
237  : "more than 1 column name matches template ",
241  : "sum of column widths not = NAXIS1 ",
251  : "unrecognizable FITS extension type ",
252  : "unrecognizable FITS record ",
253  : "END keyword is not blank ",
254  : "Header fill area not blank ",
255  : "Data fill area not blank or zero ",
261  : "illegal TFORM format code ",
262  : "unrecognizable TFORM datatype code ",
263  : "illegal TDIMn keyword value ",
264  : "invalid BINTABLE heap address ",

301  : "HDU number < 1 or > MAXHDU ",
302  : "column number < 1 or > tfields ",
304  : "tried to move before beginning of file  ",
306  : "tried to read or write negative bytes ",
307  : "illegal starting row number in table ",
308  : "illegal starting element number in vector ",
309  : "this is not an ASCII string column ",
310  : "this is not a logical datatype column ",
311  : "ASCII table column has wrong format ",
312  : "Binary table column has wrong format ",
314  : "null value has not been defined ",
317  : "this is not a variable length column ",
320  : "illegal number of dimensions in array ",
321  : "first pixel number greater than last pixel ",
322  : "illegal BSCALE or TSCALn keyword = 0 ",
323  : "illegal axis length < 1 ",
401  : "bad int to formatted string conversion ",
402  : "bad float to formatted string conversion ",
403  : "cant interprete keyword value as integer ",
404  : "cant interprete keyword value as logical ",
405  : "cant interprete keyword value as float ",
406  : "cant interprete keyword value as double ",
407  : "bad formatted string to int conversion ",
408  : "bad formatted string to float conversion ",
409  : "bad formatted string to double conversion ",
410  : "bad keyword datatype code ",
411  : "bad number of decimal places specified ",
412  : "overflow during datatype conversion ",
412  : "error in imcompress routines ",
414  :  "error in imcompress routines ",
415:  "compressed tile doesn t exist ",
420  : "error in date or time conversion ",
431  : "syntax error in parser expression ",
432  : "expression did not evaluate to desired type ",
433  : "vector result too large to return in array ",
434  : "data parser failed not sent an out column ",
435  : "bad data encounter while parsing column ",
436  : "Output file not of proper type          ",
501  : "celestial angle too large for projection ",
502  : "bad celestial coordinate or pixel value ",
503  : "error in celestial coordinate calculation ",
504  : "unsupported type of celestial projection ",
505  : "celestial coordinate keywords not found ",
506  : "approximate WCS keywords were calculated ",
}

try:
    TFORM_CTYPES['i1'] = c_bool
except NameError:
    pass
