from io import *
from io import _cfitsio
from numpy import *

self = create('out.fits')

N = 7
column_names = ['E','B','C','D','A','F','g','h'][:N]
keywords_t = c_char_p * len(column_names)
ttype = keywords_t(*map(c_char_p, column_names))
print(ttype._objects)
tform = keywords_t(*(['E']*N))
print(tform._objects)
ext_name = c_char_p('AA')
run_check_status(_cfitsio.ffcrtb, self.ptr, BINARY_TBL, c_longlong(0), c_int(N), byref(ttype), byref(tform), None, ext_name)
self.close()
