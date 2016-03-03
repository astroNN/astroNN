from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os

# Third-party
from six.moves.urllib.request import urlretrieve, urlopen
from six.moves.urllib.error import URLError

__all__ = ['fetch_notMNIST', 'fetch_GalaxyZoo']

def fetch_data(data_url, cache_path=None, download_if_missing=True):
    """
    Fetch data and return local filename

    Parameters
    ----------
    cache_path : str (optional)
        Specify a path to cache the datasets. If not specified, this
        will cache the downloaded data to the current working directory.
    download_if_missing : bool (optional)
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.
    data_url : str (optional)
        Path to the remote data file.

    Returns
    -------
    filename : str
        The path to the local HDF5 data file.
    """

    if cache_path is None:
        cache_path = os.getcwd()
    else:
        cache_path = os.path.expanduser(os.path.abspath(cache_path))

    cache_file = os.path.join(cache_path, os.path.basename(data_url))

    try:
        # how many bytes are we expecting
        url = urlopen(data_url)
        meta = url.info()
        expected_bytes = int(meta['Content-Length'])
    except URLError as e:
        if os.path.exists(cache_file):
            print("Data file exists but unable to verify against remote file.")
            return cache_file
        else:
            print("Local file not found and unable to connect to remote file! Do "
                  "you have an internet connection?")
            raise e

    if (os.path.exists(cache_file) and os.stat(cache_file).st_size != expected_bytes) \
        or not os.path.exists(cache_file) or not os.path.isfile(cache_file):
        urlretrieve(data_url, cache_file)

        received_bytes = os.stat(cache_file).st_size
        if received_bytes != expected_bytes:
            raise IOError("Download error: size expected = {} bytes, size received = {} bytes"
                          .format(expected_bytes, received_bytes))

        print("Data downloaded and verified.")

    else:
        print("Data file already exists and is verified.")

    return cache_file

def fetch_notMNIST(data_url=None, cache_path=None, download_if_missing=True):
    """
    Fetch and load the notMNIST HDF5 data. This data file is
    about ~1.7GB, so if you don't have a local copy and you choose
    to download (the default option) this could take a while.

    Parameters
    ----------
    data_url : str (optional)
        Path to the remote data file.
    cache_path : str (optional)
        Specify a path to cache the datasets. If not specified, this
        will cache the downloaded data to the current working directory.
    download_if_missing : bool (optional)
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    Returns
    -------
    filename : str
        The path to the local HDF5 data file.
    """

    if data_url is None:
        data_url = "https://s3.amazonaws.com/astronn/notMNIST.h5"

    return fetch_data(data_url=data_url, cache_path=cache_path,
                      download_if_missing=download_if_missing)

def fetch_GalaxyZoo(data_url=None, cache_path=None, download_if_missing=True):
    """
    Fetch and load the Galaxy Zoo HDF5 data. This data file is
    about ~3GB, so if you don't have a local copy and you choose
    to download (the default option) this could take a while.

    Parameters
    ----------
    data_url : str (optional)
        Path to the remote data file.
    cache_path : str (optional)
        Specify a path to cache the datasets. If not specified, this
        will cache the downloaded data to the current working directory.
    download_if_missing : bool (optional)
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    Returns
    -------
    filename : str
        The path to the local HDF5 data file.
    """

    if data_url is None:
        data_url = "https://s3.amazonaws.com/astronn/galaxyzoo_gri.h5"

    return fetch_data(data_url=data_url, cache_path=cache_path,
                      download_if_missing=download_if_missing)
