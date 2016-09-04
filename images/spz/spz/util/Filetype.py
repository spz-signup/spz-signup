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
    data = fp.read(1024)
    mime = magic.from_buffer(data, mime=True)
    fp.seek(pos, os.SEEK_SET)
    return mime


def size_from_filepointer(fp):
    """Detect size from filepointer.

    File position gets restored after the detection procedure."""
    pos = fp.tell()
    fp.seek(0, os.SEEK_END)
    size = fp.tell()
    fp.seek(pos, os.SEEK_SET)
    return size
