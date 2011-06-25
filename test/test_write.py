from pycfitsio import *

_cfitsio = CDLL("libcfitsio.so")

data = OrderedDict()
data['signal'] = np.arange(1000000) 
data['flag'] = np.ones(1000000, dtype=np.uint8)
data['signal'] = np.append(data['signal'], [12, 343,343])
data['flag'] = np.append(data['flag'], [12, 343,343]).astype(np.uint8)

self = create('big.fits')
self.write_HDU("NEWDATA", data)

#name = "NEWDATA"
#
#keywords_t = c_char_p * len(data)
#ttype = keywords_t(*map(c_char_p, data.keys()))
#tformlen = len(data.values()[0])
#tformlen = ''
#tform = keywords_t(*[str(tformlen)+NP_TFORM[col.dtype.str[1:]] for col in data.values()])
#run_check_status(_cfitsio.ffcrtb, self.ptr, BINARY_TBL, c_longlong(0), c_int(len(data)), byref(ttype), byref(tform), byref(NULL), c_char_p(name))
#
#buffer_size = c_long(1)
#run_check_status(_cfitsio.ffgrsz, self.ptr, byref(buffer_size))
#
#data_length = len(data.values()[0])
#for k in range(0,len(data.values()[0]),buffer_size.value):
#    print(k)
#    if (k+buffer_size.value)>data_length:
#        buffer_size = c_long(data_length - k)
#    for i, (colname, colarray) in enumerate(data.iteritems()):
#        coltform = NP_TFORM[colarray.dtype.str[1:]]
#        run_check_status(_cfitsio.ffpcl, self.ptr, TFORM_FITS[coltform], c_int(i+1), c_longlong(1+k), c_longlong(1), c_longlong(buffer_size.value), colarray[k:].ctypes.data_as(POINTER(TFORM_CTYPES[coltform])))
#
#for i, (colname, colarray) in enumerate(data.iteritems()):
#    coltform = NP_TFORM[colarray.dtype.str[1:]]
#    run_check_status(_cfitsio.ffpcl, self.ptr, TFORM_FITS[coltform], c_int(i+1), c_longlong(1), c_longlong(1), c_longlong(len(colarray)), colarray.ctypes.data_as(POINTER(TFORM_CTYPES[coltform])))
self.close()
