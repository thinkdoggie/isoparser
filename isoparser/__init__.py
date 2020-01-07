from __future__ import absolute_import

import six

from . import iso, source


def parse(iso_file, cache_content=False, min_fetch=16):
    """
    Returns an :class:`ISO` object for the given filesystem path, URL or file-like object.

    cache_content:
      Whether to store sectors backing file content in the sector cache. If true, this will
      cause memory usage to grow to the size of the ISO as more file content get accessed.
      Even if false (default), an individual Record object will cache its own file content
      for the lifetime of the Record, once accessed.

    min_fetch:
      The smallest number of sectors to fetch in a single operation, to speed up sequential
      accesses, e.g. for directory traversal.  Defaults to 16 sectors, or 32 KiB.
    """
    if isinstance(iso_file, six.string_types):
        if iso_file.startswith("http://") or iso_file.startswith("https://"):
            url = iso_file
            src = source.HTTPSource(url, cache_content=cache_content, min_fetch=min_fetch)
        else:
            path = iso_file
            fp = open(path, 'rb')
            src = source.FileSource(fp, cache_content=cache_content, min_fetch=min_fetch)
    else:
        fp = iso_file
        src = source.FileSource(fp, cache_content=cache_content, min_fetch=min_fetch)

    return iso.ISO(src)
