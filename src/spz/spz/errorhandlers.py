# -*- coding: utf-8 -*-

"""Custom error handlers.

   Registers error handlers for the most common errors.
"""

from flask import flash, redirect, render_template, url_for
from flask_babel import gettext as _


def render_error(errorcode, errormessage):
    """Renders the error handler template and explicitely sets the HTTP status code.

       :param errorcode: The HTTP error code.
       :param errormessage: The error message to render.
    """
    return render_template('errorhandler.html', errorcode=errorcode, errormessage=errormessage), errorcode


def page_not_found(e):
    return render_error(404, _('Seite nicht gefunden'))


def page_forbidden(e):
    return render_error(403, _('Keine Berechtigung'))


def page_gone(e):
    return render_error(410, _('Seite wurde entfernt'))


def not_found(e):
    return render_error(500, _('Interner Fehler'))


def unauthorized(e):
    flash(_('Bitte einloggen!'), 'warning')
    return redirect(url_for('login'))


def bad_request(e):
    return render_error(400, _('Fehlerhafte Anfrage (evt. Verdacht auf CSRF)'))
