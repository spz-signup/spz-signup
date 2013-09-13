# -*- coding: utf-8 -*-

"""Sign up management handling.

   .. note::
      Views have to be registered at the end of this module because of circular dependencies.

   .. warning::
      Some code analyzers may flag view imports as unused, because they are only imported for their side effects.
"""

from flask import Flask, session, g
from flask.ext.assets import Environment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.cache import Cache

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

# Cache setup
cache = Cache(app, config=app.config['CACHE_CONFIG'])


# Register all views here
from spz import views, errorhandlers, auth


# Authentication
@app.before_request
def get_current_user():
    mail = session.get('email', None)
    acl = app.config['ACCESS_CONTROL']

    if mail in acl['unrestricted']:
        g.access = 'unrestricted'
    elif mail in acl['restricted']:
        g.access = 'restricted'
    else:
        g.access = None

    g.user = mail


routes = [('/', views.index, ['GET', 'POST']),
          ('/licenses', views.licenses, ['GET']),

          ('/internal', views.internal, ['GET']),
          ('/internal/statistics', views.statistics, ['GET']),
          ('/internal/datainput', views.datainput, ['GET', 'POST']),
          ('/internal/datainput/matrikelnummer', views.matrikelnummer, ['GET', 'POST']),
          ('/internal/datainput/zulassungen', views.zulassungen, ['GET', 'POST']),
          ('/internal/notifications', views.notifications, ['GET', 'POST']),

          ('/internal/lists', views.lists, ['GET']),
          ('/internal/language/<int:id>', views.language, ['GET']),
          ('/internal/course/<int:id>', views.course, ['GET']),
          ('/internal/applicant/<int:id>', views.applicant, ['GET']),

          ('/_auth/login', auth.login_handler, ['GET', 'POST']),
          ('/_auth/logout', auth.logout_handler, ['POST'])]

for rule, view_func, methods in routes:
    app.add_url_rule(rule, view_func=view_func, methods=methods)


handlers = [(404, errorhandlers.page_not_found),
            (403, errorhandlers.page_forbidden),
            (410, errorhandlers.page_gone),
            (500, errorhandlers.not_found)]

for errno, handler in handlers:
    app.register_error_handler(errno, handler)


# vim: set tabstop=4 shiftwidth=4 expandtab:
