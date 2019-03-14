# -*- coding: utf-8 -*-

"""Implements the RCSSMin stylesheet minifier filter for webassets.

   The assets package does not provide a filter for rcssmin.
   We probably could use cssmin, but it's not as up to date as rcssmin.
"""

from rcssmin import cssmin
from flask_assets import Filter


class RCSSMin(Filter):
    """Stylesheet minifier, using the RCSSmin library.

       .. note:: you have to register this filter explicitely before using it
    """

    name = 'rcssmin'

    def output(self, _in, out, **kw):
        out.write(cssmin(_in.read()))
