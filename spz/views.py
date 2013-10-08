# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

import socket
import csv

from flask import request, redirect, render_template, url_for, flash
from flask.ext.mail import Message
from sqlalchemy.orm.exc import FlushError


from spz import app, models, mail, db
from spz.decorators import templated, auth_required
from spz.headers import upheaders
from spz.forms import SignupForm, NotificationForm, ApplicantForm


@upheaders
@templated('signup.html')
def index():
    form = SignupForm()

    evaluated = []  # XXX: remove this later

    if form.validate_on_submit():
        applicant = form.get_applicant()
        course = form.get_course()

        if course.is_english() and not course.is_allowed(applicant):
            flash(u'Sie haben nicht die vorausgesetzten Englischtest-Ergebnisse um diesen Kurs zu wählen', 'danger')
            return dict(form=form)

        evaluated.append(course.is_full())

        if course.is_full():
            evaluated.append(">>> waiting")
            status = models.StateOfAtt.query.filter_by(id=1).first()
        else:
            evaluated.append(">>> attends")
            status = models.StateOfAtt.query.filter_by(id=2).first()

        if applicant.has_to_pay():
            status = models.StateOfAtt.query.filter_by(id=4).first()
            evaluated.append(">>> has to pay")

        evaluated.append(status.name)

        # Run the final insert isolated in a transaction, with rollback semantics
        try:
            # TODO: check if already in this course
            applicant.add_course_attendance(course, status, form.get_graduation())
            db.session.add(applicant)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(u'Ihre Kurswahl konnte nicht registriert werden: {0}'.format(e), 'danger')
            return dict(form=form)

        # TODO: send mail now

        return render_template('confirm.html', evaluated=evaluated)

    return dict(form=form)


@upheaders
@templated('licenses.html')
def licenses():
    return None


@upheaders
@templated('internal/overview.html')
def internal():
    return None


@upheaders
@auth_required
@templated('internal/statistics.html')
def statistics():
    return None


@upheaders
@auth_required
@templated('internal/datainput.html')
def datainput():
    return None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@upheaders
@auth_required
@templated('internal/datainput/matrikelnummer.html')
def matrikelnummer():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            lst = {models.Registration(line.rstrip('\r\n')) for line in fp}
            gel = models.Registration.query.delete()
            db.session.add_all(lst)
            db.session.commit()
            flash(u'Dateiname war OK %s Zeilen gelöscht %s Zeilen gelesen' % (gel, len(lst)), 'success')

            return redirect(url_for('internal'))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        return redirect(url_for('matrikelnummer'))
    return None


@upheaders
@auth_required
@templated('internal/datainput/status.html')
def status():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            try: 
                lst = (models.StateOfAtt(line.rstrip('\r\n')) for line in fp)
                gel = models.StateOfAtt.query.delete()
                db.session.add_all(lst)
                db.session.commit()
                anz = models.StateOfAtt.query.count()
                flash(u' %s Zeilen gelöscht %s Zeilen aus %s gelesen' % (gel, anz, fp.filename), 'success')
            except (IndexError, csv.Error) as e:
                flash(u'Status konnten nicht eingelesen werden (\';\' als Trenner verwenden): {0}'.format(e), 'danger')                

            return redirect(url_for('internal'))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        return redirect(url_for('zulassungen'))
    return None


@upheaders
@auth_required
@templated('internal/datainput/zulassungen.html')
def zulassungen():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            filecontent = csv.reader(fp, delimiter=';')
            try: 
                lst = [models.Approval(line[0], line[1]) for line in filecontent]
                gel = models.Approval.query.delete()
                db.session.add_all(lst)
                db.session.commit()
#                anz = models.Approval.query.count()
                flash(u' %s Zeilen gelöscht %s Zeilen aus %s gelesen' % (gel, len(lst), fp.filename), 'success')
            except (IndexError, csv.Error) as e:
                flash(u'Zulassungen konnten nicht eingelesen werden (\';\' als Trenner verwenden): {0}'.format(e), 'danger')                

            return redirect(url_for('internal'))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        return redirect(url_for('zulassungen'))
    return None


@upheaders
@auth_required
@templated('internal/notifications.html')
def notifications():
    form = NotificationForm()

    if form.validate_on_submit():
        try:
            # TODO(daniel): extract recipients from courses; sender from config
            msg = Message(subject=form.mail_subject.data, body=form.mail_body.data, recipients=None, sender=None)
            mail.send(msg)
            flash(u'Mail erfolgreich verschickt', 'success')
            return redirect(url_for('internal'))

        except (AssertionError, socket.error) as e:
            flash(u'Mail wurde nicht verschickt: {0}'.format(e), 'danger')

    return dict(form=form)


@upheaders
@auth_required
@templated('internal/lists.html')
def lists():
    return dict(languages=models.Language.query.order_by(models.Language.name).all())


@upheaders
@auth_required
@templated('internal/language.html')
def language(id):
    return dict(language=models.Language.query.get_or_404(id))


@upheaders
@auth_required
@templated('internal/course.html')
def course(id):
    return dict(course=models.Course.query.get_or_404(id))


@upheaders
@auth_required
@templated('internal/applicant.html')
def applicant(id):

    applicant = models.Applicant.query.get_or_404(id)
    form = ApplicantForm()

    if form.validate_on_submit():

        try:
            applicant.first_name = form.first_name.data
            applicant.last_name = form.last_name.data
            applicant.phone = form.phone.data
            applicant.mail = form.mail.data
            applicant.tag = form.tag.data
##            applicant.origin = form.origin.data
            db.session.commit()
            flash(u'Der Bewerber wurde aktualisiert', 'success')
        except Exception as e:
            db.session.rollback()
            flash(u'Der Bewerber konnte nicht aktualisiert werden: {0}'.format(e), 'danger')
            return dict(form=form)

    form.populate(applicant)
    return dict(form=form)


@upheaders
@auth_required
@templated('internal/course.html')
def course(id):
    return dict(course=models.Course.query.get_or_404(id))


# vim: set tabstop=4 shiftwidth=4 expandtab:
