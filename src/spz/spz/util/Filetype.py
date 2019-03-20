# -*- coding: utf-8 -*-

"""Utilities to detect a file type.
"""

import magic
import os


def mime_from_filepointer(fp):
    """Detect mime from filepointer.

    File position gets restored after the detection procedure."""
    pos = fp.tell()
    fp.seek(0)
    try:
        data = fp.read(1024)
        mime = magic.from_buffer(data, mime=True)
        fp.seek(pos, os.SEEK_SET)
        return mime
    except UnicodeDecodeError:
        # that might happen when you open a file as text but it contains binary data
        # in this case, we assume that this was not the file-type you wanted and try
        # to follow RFC 2046 as close as possible
        fp.seek(pos, os.SEEK_SET)
        return 'application/octet-stream'


def size_from_filepointer(fp):
    """Detect size from filepointer.

    File position gets restored after the detection procedure."""
    if not fp:
        return 0
    pos = fp.tell()
    fp.seek(0, os.SEEK_END)
    size = fp.tell()
    fp.seek(pos, os.SEEK_SET)
    return size
