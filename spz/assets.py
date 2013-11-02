# -*- coding: utf-8 -*-

"""Register assets for optimizations.

   We optimize and merge assets into bundles, in order to reduce the client's connections
   from number of assets down to number of bundles.

   Register static files for those asset bundles here.

   We support the two most common and mature filters only:
        - rjsmin (for .js files)
        - rcssmin (for .css files)

   .. note::
      Paths are relative to the static directory.

   .. warning::
      * Synchronize this listing with static directory changes.
      * License get's stripped too, provide external file.
"""

from flask.ext.assets import Bundle, register_filter
from webassets.loaders import PythonLoader as PythonAssetsLoader

from spz.util.RCSSMin import RCSSMin


register_filter(RCSSMin)


# Javascript bundles:

all_js = Bundle('js/jquery-1.10.2.min.js',
                'js/mailcheck.1.0.2.min.js',
                'js/mailcheck-domains.js',
                'js/garlic-1.2.2.min.js',
                'js/parsley-1.1.16-de.js',
                'js/parsley-1.1.16.min.js',
                'js/moment.2.0.0.min.js',
                'js/bootstrap.min.js',
                'js/bootstrap-sortable.js',
                'js/intro.min.js',
                filters='rjsmin', output='js/packed.js')

# Internet Explorer specific Javascript workarounds
ie_js = Bundle('js/html5shiv.js',
               'js/respond.min.js',
               filters='rjsmin', output='js/packed_ie.js')


# Tooling bundles
tools_js = Bundle('js/persona.js',
                  filters='rjsmin', output='js/packed_tools.js')


# Stylesheet bundles:

all_css = Bundle('css/bootstrap.min.css',
                 'css/bootstrap-sortable.css',
                 'css/sidebar.css',
                 'css/scrollbars.css',
                 'css/introjs.min.css',
                 filters='rcssmin', output='css/packed.css')


# Hide concrete loading method inside this module
def get_bundles():
    """Returns all registered bundles.

       .. note:: Returns only bundles from the assets module, you shouldn't register them anywhere else
    """
    loader = PythonAssetsLoader(__name__)

    return loader.load_bundles()


# vim: set tabstop=4 shiftwidth=4 expandtab:
