from io import *

def read_map(filename, columns=None):
    """Read healpix map and return IQU or I array and header dictionary
    
    columns: None reads all the columns, otherwise a list of integers zero-based column numbers
            or a list of column names
            
    Returns the data array and a header dictionary"""

    #TODO context manager
    f = open(filename)
    first_hdu = f[0]

    if columns is None:
        return first_hdu.read_all(), first_hdu.header

if __name__ == '__main__':
    d, h = read_map('../test/data.fits')
