import numpy as np
import pyfits

a=pyfits.new_table([pyfits.Column(name='signal',array=np.arange(1000),format='D'),pyfits.Column(name='flag',array=np.ones(1000,dtype=np.uint8),format='B')])
a.name='DATA'
a.writeto('data.fits',clobber=True)

