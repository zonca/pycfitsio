import numpy as np

import healpy

from io import read

def read_map(filename, HDU=0, field=0, nest=False):
    """Read Healpix map
    all columns of the specified HDU are read into a compound numpy MASKED array
    if nest is not None, the map is converted if need to NEST or RING ordering.
    this function requires healpy"""
    m, h = read(filename, HDU=HDU)
    m = m[m.dtype.names[0]]
    nside = healpy.npix2nside(m.size)
    if not nest is None:
        if h.get('ORDERING', False):
            if h['ORDERING'] == 'NESTED' and not nest:
                idx = healpy.ring2nest(nside,np.arange(m.size,dtype=np.int32))
                m = m[idx]
            elif h['ORDERING'] == 'RING' and nest:
                idx = healpy.nest2ring(nside,np.arange(m.size,dtype=np.int32))
                m = m[idx]
    return healpy.ma(m)
