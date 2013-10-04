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
from spz.forms import SignupForm, NotificationForm


@upheaders
@templated('signup.html')
def index():
    form = SignupForm()

    evaluated = []  # XXX: remove this

    if form.validate_on_submit():
        applicant = form.get_applicant()
        course = form.get_course()

        if course.is_english() and not course.is_allowed(applicant):
            flash(u'Sie haben nicht die vorausgesetzten Englischtest Ergebnisse um diesen Kurs zu wählen', 'danger')
            return dict(form=form)

        # TODO:
        #if course.full():
            #waiting
        #else:
            #attends
        status = models.StateOfAtt.query.first()


        if applicant.has_to_pay():
            evaluated.append(">>> has to pay")

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
@templated('internal/all_courses.html')
def all_courses():
    return dict(courses=models.Course.query.order_by(models.Course.id.asc()).all())


@upheaders
@auth_required
@templated('internal/course_attendances.html')
def course_attendances(id):
    course = models.Course.query.get_or_404(id)
    attendances = db.session.query(models.Applicant, models.Attendance).filter(models.Applicant.id==models.Attendance.applicant_id).filter(models.Attendance.course_id==id).all()
    return dict(c=course, a=attendances)


@upheaders
@auth_required
@templated('internal/lists.html')
def lists():
    return dict(languages=models.Language.query.all())


@upheaders
@auth_required
@templated('internal/applicant.html')
def applicant(id):
    return dict(applicant = models.Applicant.query.get_or_404(id))


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


# vim: set tabstop=4 shiftwidth=4 expandtab:
