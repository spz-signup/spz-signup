# -*- coding: utf-8 -*-

"""Utilities to detect a file type.
"""

import magic


def mime_from_filepointer(fp):
    """Detect mime from filepointer.

    File position gets restored after the detection procedure."""
    pos = fp.tell()
    fp.seek(0)
    data = fp.read(1024)
    mime = magic.from_buffer(data, mime=True).decode('utf-8')
    fp.seek(pos)
    return mime
