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


# Set up logging before anything else, in order to catch early errors
if not app.debug:
    from logging import FileHandler
    file_handler = FileHandler(app.config['LOGFILE'])
    app.logger.addHandler(file_handler)


# Database handling
db = SQLAlchemy(app)

# Mail sending
mail = Mail(app)

# Cache setup
cache = Cache(app, config=app.config['CACHE_CONFIG'])


# Register all views here
from spz import views, errorhandlers, auth, pdf


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

          ('/internal/import', views.importer, ['GET']),
          ('/internal/import/registrations', views.registrations, ['GET', 'POST']),
          ('/internal/import/approvals', views.approvals, ['GET', 'POST']),

          ('/internal/export', views.exporter, ['GET']),
          ('/internal/export_course/<int:course_id>', views.export_course, ['GET']),
          ('/internal/print_course/<int:course_id>', pdf.print_course, ['GET']),
          ('/internal/export_language/<int:language_id>', views.export_language, ['GET']),
          ('/internal/print_language/<int:language_id>', pdf.print_language, ['GET']),

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
          ('/internal/status/<int:applicant_id>/<int:course_id>', views.status, ['GET', 'POST']),
          ('/internal/print_bill/<int:applicant_id>/<int:course_id>', pdf.print_bill, ['GET']),

          ('/internal/restock', views.restock, ['GET', 'POST']),

          ('/internal/statistics', views.statistics, ['GET']),
          ('/internal/statistics/free_courses', views.free_courses, ['GET']),

          ('/internal/duplicates', views.duplicates, ['GET']),

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
