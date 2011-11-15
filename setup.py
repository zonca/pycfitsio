from distutils.core import setup

setup(
    name = "pycfitsio",
    version = "0.3.0",

    packages=['pycfitsio', 'pycfitsio.test'],

    author = "Andrea Zonca",
    author_email = "code@andreazonca.com",
    description = "Simple FITS files I/O package",
    license='GPL3',
    keywords = "fits, astrophysics, pyfits",
    url = "http://github.com/zonca/pycfitsio",
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Physics',
          ],
    long_description=open('README.txt').read(),

)
