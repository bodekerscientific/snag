import os

from setuptools import setup, find_packages


PACKAGE_NAME = "snag"
AUTHOR = "Jared Lewis"
AUTHOR_EMAIL = "jared@bodekerscientific.com"
DESCRIPTION = "Single column model Namelist Auto Generator"


version = None
exec(open('snag/version.py').read())


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=PACKAGE_NAME,
    version=version,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    long_description=read('README.rst'),
    url='https://github.com/bodekerscientific/snag',  # use the URL to the github repo
    download_url='https://github.com/bodekerscientific/snag/archive/{}.tar.gz'.format(version),
    install_requires=[
        'pyyaml',
        'six',
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
    entry_points={
        'console_scripts':
            ['snag = snag.cli:main']
    },
)
