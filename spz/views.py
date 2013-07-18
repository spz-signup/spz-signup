# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

from flask import redirect, url_for, flash
from flask.ext.mail import Message

from spz import models, mail
from spz.decorators import templated
from spz.headers import upheaders
from spz.forms import SignupForm


def nullmailer():
    msg = Message("hello", recipients=["alice@example.com"])
    mail.send(msg)

    return u'mail sent'


@upheaders
@templated('signup.html')
def index():
    form = SignupForm()

    if form.validate_on_submit():
        # applicant = Applicant(first_name = form.first_name.data, ..)
        flash(u'Erfolgreich eingetragen', 'success')
        return redirect(url_for('index'))

    return dict(form=form)


@upheaders
@templated('course.html')
def course(id):
    return dict(course=models.Course.query.get_or_404(id))


@upheaders
@templated('language.html')
def language(id):
    return dict(language=models.Language.query.get_or_404(id))


@upheaders
@templated('applicant.html')
def applicant(id):
    return dict(applicant=models.Applicant.query.get_or_404(id))


# vim: set tabstop=4 shiftwidth=4 expandtab:
