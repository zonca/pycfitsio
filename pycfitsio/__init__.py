import warnings

from file import File, open, read, create, write, CfitsioError  
try:
    from healpix import read_map, read_mask
except:
    warnings.warn('Cannot import read_map and read_mask if healpy is not installed')
    pass
