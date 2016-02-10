# -*- coding: utf-8 -*-

"""Sign up management handling.

   .. note::
      Views have to be registered at the end of this module because of circular dependencies.

   .. warning::
      Some code analyzers may flag view imports as unused, because they are only imported for their side effects.
"""

import os

from flask import Flask, session, g
from flask.ext.assets import Environment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.mail import Mail
from flask.ext.cache import Cache

from jinja2 import Markup

from spz import assets


class CustomFlask(Flask):
    """Internal customizations to the Flask class.

       This is mostly for Jinja2's whitespace and newline control, and improved template performance.
    """
    jinja_options = dict(Flask.jinja_options, trim_blocks=True, lstrip_blocks=True, auto_reload=False)

app = CustomFlask(__name__, instance_relative_config=True)


# set up login system
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

@login_manager.user_loader
def login_by_id(id):
    # local imports to avoid import before config
    from spz.models import User
    return User.query.filter(User.id == id).first()

@login_manager.token_loader
def login_by_token(tokenstring):
    # local imports to avoid import before config
    from spz.models import User
    return User.get_by_token(tokenstring)


# add `include_raw` Jinja helper
app.jinja_env.globals['include_raw'] = lambda filename : Markup(app.jinja_loader.get_source(app.jinja_env, filename)[0])


# Assets handling; keep the spz.assets module in sync with the static directory
assets_env = Environment(app)

bundles = assets.get_bundles()

for name, bundle in bundles.items():
    assets_env.register(name, bundle)


# Configuration loading
if 'SPZ_CFG_FILE' in os.environ:
    app.config.from_pyfile(os.environ['SPZ_CFG_FILE'])
else:
    app.config.from_pyfile('development.cfg')
    # app.config.from_pyfile('production.cfg')


# Set up logging before anything else, in order to catch early errors
if not app.debug:
    from logging import FileHandler
    file_handler = FileHandler(app.config['LOGFILE'])
    app.logger.addHandler(file_handler)


# modify app for uwsgi
if app.debug:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
elif args.profiling:
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app)

elif args.linting:
    from werkzeug.contrib.lint import LintMiddleware
    app.wsgi_app = LintMiddleware(app.wsgi_app)


# Database handling
db = SQLAlchemy(app)

# Mail sending
mail = Mail(app)

# Cache setup
cache = Cache(app, config=app.config['CACHE_CONFIG'])


# Register all views here
from spz import views, errorhandlers, pdf


# Permission handling
@app.before_request
def detect_permission_level():
    if not current_user.is_anonymous:
        mail = current_user.id
        acl = app.config['ACCESS_CONTROL']

        if mail in acl['unrestricted']:
            g.access = 'unrestricted'
        elif mail in acl['restricted']:
            g.access = 'restricted'
        else:
            g.access = None

        g.user = mail
    else:
        g.access = None
        g.user = None


routes = [('/', views.index, ['GET', 'POST']),
          ('/licenses', views.licenses, ['GET']),

          ('/internal/', views.internal, ['GET']),

          ('/internal/import/', views.importer, ['GET']),
          ('/internal/import/registrations', views.registrations, ['GET', 'POST']),
          ('/internal/import/approvals', views.approvals, ['GET', 'POST']),

          ('/internal/export_course/<int:course_id>', views.export_course, ['GET']),
          ('/internal/print_course/<int:course_id>', pdf.print_course, ['GET']),
          ('/internal/print_course_presence/<int:course_id>', pdf.print_course_presence, ['GET']),
          ('/internal/export_language/<int:language_id>', views.export_language, ['GET']),
          ('/internal/print_language/<int:language_id>', pdf.print_language, ['GET']),
          ('/internal/print_language_presence/<int:language_id>', pdf.print_language_presence, ['GET']),

          ('/internal/notifications', views.notifications, ['GET', 'POST']),

          ('/internal/lists', views.lists, ['GET']),
          ('/internal/applicant/<int:id>', views.applicant, ['GET', 'POST']),
          ('/internal/language/<int:id>', views.language, ['GET']),
          ('/internal/course/<int:id>', views.course, ['GET']),

          ('/internal/add_attendance/<int:applicant_id>/<int:course_id>', views.add_attendance, ['GET']),
          ('/internal/remove_attendance/<int:applicant_id>/<int:course_id>', views.remove_attendance, ['GET']),

          ('/internal/applicants/search_applicant', views.search_applicant, ['GET', 'POST']),
          ('/internal/applicants/applicant_attendances/<int:id>', views.applicant_attendances, ['GET']),

          ('/internal/payments', views.payments, ['GET', 'POST']),
          ('/internal/outstanding', views.outstanding, ['GET', 'POST']),
          ('/internal/status/<int:applicant_id>/<int:course_id>', views.status, ['GET', 'POST']),
          ('/internal/print_bill/<int:applicant_id>/<int:course_id>', pdf.print_bill, ['GET']),

          # First-come-first-serve selection
          ('/internal/restock_fcfs', views.restock_fcfs, ['GET', 'POST']),
          # Weighted random selection
          ('/internal/restock_rnd', views.restock_rnd, ['GET', 'POST']),

          ('/internal/unique', views.unique, ['GET', 'POST']),

          ('/internal/preterm', views.preterm, ['GET', 'POST']),

          ('/internal/statistics/', views.statistics, ['GET']),
          ('/internal/statistics/free_courses', views.free_courses, ['GET']),
          ('/internal/statistics/origins_breakdown', views.origins_breakdown, ['GET']),
          ('/internal/statistics/task_queue', views.task_queue, ['GET']),

          ('/internal/duplicates', views.duplicates, ['GET']),

          ('/internal/login', views.login, ['GET', 'POST']),
          ('/internal/logout', views.logout, ['GET', 'POST']),
]

for rule, view_func, methods in routes:
    app.add_url_rule(rule, view_func=view_func, methods=methods)


handlers = [
    (401, errorhandlers.unauthorized),
    (404, errorhandlers.page_not_found),
    (403, errorhandlers.page_forbidden),
    (410, errorhandlers.page_gone),
    (500, errorhandlers.not_found),
]

for errno, handler in handlers:
    app.register_error_handler(errno, handler)