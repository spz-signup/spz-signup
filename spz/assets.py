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

all_js = Bundle('js/jquery-1.11.1.min.js',
                'js/mailcheck.1.1.0.min.js',
                'js/mailcheck-domains.js',
                'js/garlic-1.2.2.min.js',
                'js/parsley-de.js',
                'js/parsley.min.js',
                'js/moment.min.js',
                'js/bootstrap.min.js',
                'js/select2.min.js',
                filters='rjsmin', output='js/packed.js')

# Internet Explorer specific Javascript workarounds
ie_js = Bundle('js/html5shiv.js',
               'js/respond.min.js',
               filters='rjsmin', output='js/packed_ie.js')


# Tooling bundles
tools_js = Bundle('js/persona.js',
                  'js/bootstrap-sortable.js',
                  filters='rjsmin', output='js/packed_tools.js')


# Stylesheet bundles:

all_css = Bundle('css/bootstrap.min.css',
                 'css/select2.min.css',
                 'css/simple-sidebar.css',
                 'css/scrollbars.css',
                 'css/spz.css',
                 filters='rcssmin', output='css/packed.css')

tools_css = Bundle('css/bootstrap-sortable.css',
                   filters='rcssmin', output='css/packed_tools.css')


# Hide concrete loading method inside this module
def get_bundles():
    """Returns all registered bundles.

       .. note:: Returns only bundles from the assets module, you shouldn't register them anywhere else
    """
    loader = PythonAssetsLoader(__name__)

    return loader.load_bundles()
