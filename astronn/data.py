from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os

# Third-party
from six.moves.urllib.request import urlretrieve, urlopen

def fetch_notMNIST(cache_path=None, download_if_missing=True, data_url=None):
    """
    Fetch and load the notMNIST HDF5 data. This data file is
    about ~1.7GB, so if you don't have a local copy and you choose
    to download (the default option) this could take a while.

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

    if data_url is None:
        data_url = "https://s3.amazonaws.com/astronn/notMNIST.h5"

    cache_file = os.path.join(cache_path, os.path.basename(data_url))

    # how many bytes are we expecting
    url = urlopen(data_url)
    meta = url.info()
    expected_bytes = int(meta['Content-Length'])

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
