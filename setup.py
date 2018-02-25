import os

from setuptools import setup, find_packages

from snag import __version__

PACKAGE_NAME = "snag"
VERSION = __version__
AUTHOR = "Jared Lewis"
AUTHOR_EMAIL = "jared@bodekerscientific.com"
DESCRIPTION = "Single column model Namelist Auto Generator"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    long_description=read('README.rst'),
    url='https://github.com/bodekerscientific/snag',  # use the URL to the github repo
    download_url='https://github.com/bodekerscientific/snag/archive/{}.tar.gz'.format(VERSION),
    install_requires=[
        'pyyaml',
        'six',
        'f90nml>=0.23',
        'netCDF4',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',

        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science'
    ],
    keywords='namelist scm climate generator',
)
