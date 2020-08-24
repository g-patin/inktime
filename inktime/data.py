# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/01_data.ipynb (unless otherwise specified).

__all__ = ['fetch_star', 'fetch_blackwhite', 'GOODBOY', 'registry_file']

# Cell
import pkg_resources
import pooch
import numpy
import matplotlib.pyplot as plt


GOODBOY = pooch.create(
    # Use the default cache folder for the OS
    path=pooch.os_cache('inktime'),
    # The remote data is on Github
    base_url='https://github.com/fligt/inktime/raw/master/data/',
    version=None,
    # If this is a development version, get the data from the master branch
    version_dev=None,
    # We'll load it from a file below
    registry=None,
)

registry_file = pkg_resources.resource_stream('inktime', 'registry.txt')
GOODBOY.load_registry(registry_file)

def fetch_star():
    '''Download demo data file *star.png* into cache once.

    Returns:
    --------

    im: numpy array'''

    fpath = GOODBOY.fetch('star.png')
    im = plt.imread(fpath)

    return im

def fetch_blackwhite():
    '''Download demo data file *blackwhite.png* into cache once.

    Returns:
    --------

    im: numpy array'''

    fpath = GOODBOY.fetch('blackwhite.png')
    im = plt.imread(fpath)

    return im