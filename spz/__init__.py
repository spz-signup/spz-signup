# -*- coding: utf-8 -*-

"""Sign up management handling.

   .. note::
      Views have to be registered at the end of this module because of circular dependencies.

   .. warning::
      Some code analyzers may flag view imports as unused, because they are only imported for their side effects.
"""

from flask import Flask
from flask.ext.assets import Environment

from spz import assets


class CustomFlask(Flask):
    """Internal customizations to the Flask class.

       This is mostly for Jinja2's whitespace and newline control, and improved template performance.
    """
    jinja_options = dict(Flask.jinja_options, trim_blocks=True, lstrip_blocks=True, auto_reload=False)

app = CustomFlask(__name__, instance_relative_config=True)


# Assets handling; keep the spz.assets module in sync with the static directory
assets_env = Environment(app)

bundles = assets.get_bundles()

for name, bundle in bundles.iteritems():
    assets_env.register(name, bundle)


# Configuration loading
app.config.from_pyfile('development.cfg')
#app.config.from_pyfile('production.cfg')


# Register all views here
from spz import views
from spz import errorhandlers


# vim: set tabstop=4 shiftwidth=4 expandtab:
