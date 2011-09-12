from io import File, open, read, create, CfitsioError  
try: #read_map available only if healpy is installed
    from healpix import read_map
except:
    pass
