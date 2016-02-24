# -*- coding: utf-8 -*-

"""Custom error handlers.

   Registers error handlers for the most common errors.
"""

from flask import flash, redirect, render_template, url_for


def render_error(errorcode, errormessage):
    """Renders the error handler template and explicitely sets the HTTP status code.

       :param errorcode: The HTTP error code.
       :param errormessage: The error message to render.
    """
    return render_template('errorhandler.html', errorcode=errorcode, errormessage=errormessage), errorcode


def page_not_found(e):
    return render_error(404, 'Seite nicht gefunden')


def page_forbidden(e):
    return render_error(403, 'Keine Berechtigung')


def page_gone(e):
    return render_error(410, 'Seite wurde entfernt')


def not_found(e):
    return render_error(500, 'Interner Fehler')


def unauthorized(e):
    flash('Bitte einloggen!', 'warning')
    return redirect(url_for('login'))

def bad_request(e):
    return render_error(400, 'Fehlerhafte Anfrage (evt. Verdacht auf CSRF)')
