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
    long_description=read('README.md'),
    url='https://github.com/bodekerscientific/snag',  # use the URL to the github repo
    download_url='https://github.com/bodekerscientific/snag/archive/{}.tar.gz'.format(VERSION),
)
