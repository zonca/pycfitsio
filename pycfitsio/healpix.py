from __init__ import *

HEALPIX_KEYS = ['NSIDE', 'ORDERING', 'BAD_DATA', 'COORDSYS']

def read_map(filename, columns=None, header_keys=HEALPIX_KEYS):
    """Read healpix map and return IQU or I array and header dictionary
    
    columns: None reads all the columns, otherwise a list of integers zero-based column numbers
            or a list of column names"""

    f = open(filename)
    first_hdu = f[0]

    if columns is None:
        data = first_hdu.read_all()


