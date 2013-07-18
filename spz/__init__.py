# -*- coding: utf-8 -*-

"""Sign up management handling.

   .. note::
      Views have to be registered at the end of this module because of circular dependencies.

   .. warning::
      Some code analyzers may flag view imports as unused, because they are only imported for their side effects.
"""

from flask import Flask
from flask.ext.assets import Environment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

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

# Database handling
db = SQLAlchemy(app)

# Mail sending
mail = Mail(app)


# Register all views here
from spz import views, errorhandlers, auth

app.before_request = auth.get_current_user


routes = [('/', views.index, ['GET', 'POST']),
          ('/language/<int:id>', views.language, ['GET']),
          ('/course/<int:id>', views.course, ['GET']),
          ('/applicant/<int:id>', views.applicant, ['GET']),
          ('/nullmailer', views.nullmailer, ['GET']),
          ('/_auth/login', auth.login_handler, ['GET', 'POST']),
          ('/_auth/logout', auth.logout_handler, ['POST'])]

for rule, view_func, methods in routes:
    app.add_url_rule(rule, view_func=view_func, methods=methods)


handlers = [(404, errorhandlers.page_not_found),
            (403, errorhandlers.page_forbidden),
            (410, errorhandlers.page_gone),
            (500, errorhandlers.not_found)]

for errno, handler in handlers:
    app.error_handlers[errno] = handler


# vim: set tabstop=4 shiftwidth=4 expandtab:
