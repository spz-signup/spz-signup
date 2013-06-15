# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

from flask import request, redirect, url_for, flash

from spz import app
from spz.decorators import templated
from spz.forms import SignupForm


@app.route('/', methods=['GET', 'POST'])
@templated('signup.html')
def index():
    form = SignupForm(request.form)

    if form.validate_on_submit():
        # applicant = Applicant(first_name = form.first_name.data, ..)
        flash(u'Saved', 'success')
        return redirect(url_for('index'))

    return dict(form=form)


# vim: set tabstop=4 shiftwidth=4 expandtab:
