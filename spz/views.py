# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

import socket
import csv
import re

from sqlalchemy import func

from flask import request, redirect, render_template, url_for, flash, g
from flask.ext.mail import Message

from spz import app, models, mail, db
from spz.decorators import templated, auth_required
from spz.forms import SignupForm, NotificationForm, ApplicantForm, StatusForm, PaymentForm


@templated('signup.html')
def index():
    form = SignupForm()

    if form.validate_on_submit():
        applicant = form.get_applicant()
        course = form.get_course()

        if course.is_overbooked():
            flash(u'Der gewünschte Kurs inklusive Warteliste ist bereits ausgebucht', 'danger')
            return dict(form=form)

        if not course.is_allowed(applicant):
            flash(u'Sie haben nicht die vorausgesetzten Sprachtest-Ergebnisse um diesen Kurs zu wählen', 'danger')
            return dict(form=form)

        if applicant.in_course(course):
            flash(u'Sie nehmen bereits am Kurs teil', 'danger')
            return dict(form=form)

        # Run the final insert isolated in a transaction, with rollback semantics
        try:
            applicant.add_course_attendance(course, form.get_graduation(),
                                            waiting=course.is_full(),
                                            has_to_pay=applicant.has_to_pay())

            db.session.add(applicant)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(u'Ihre Kurswahl konnte nicht registriert werden: {0}'.format(e), 'danger')
            return dict(form=form)

        # Send confirmation mail now
        try:
            msg = Message(sender=app.config['PRIMARY_MAIL'], recipients=[applicant.mail],
                          subject=u'[Sprachenzentrum] Kurs {0} {1}'.format(course.language.name, course.level),
                          body=u'Bewerbernummer: A{0}C{1}'.format(applicant.id, course.id))
            mail.send(msg)
            flash(u'Eine Bestätigungsmail wurde an {0} verschickt'.format(applicant.mail), 'success')
        except (AssertionError, socket.error) as e:
            flash(u'Eine Bestätigungsmail konnte nicht verschickt werden: {0}'.format(e), 'danger')

        # Finally redirect the user to an confirmation page, too
        return render_template('confirm.html', applicant=applicant, course=course)

    return dict(form=form)


@templated('licenses.html')
def licenses():
    return None


@templated('internal/overview.html')
def internal():
    return None


@auth_required
@templated('internal/statistics.html')
def statistics():
    return None


@auth_required
@templated('internal/datainput.html')
def datainput():
    return None


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

            return redirect(url_for('datainput'))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        return redirect(url_for('matrikelnummer'))
    return None


@auth_required
@templated('internal/datainput/zulassungen.html')
def zulassungen():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            filecontent = csv.reader(fp, delimiter=';')
            try: 
                gel = 0
                if request.form.getlist("delete_old"):
                    gel = models.Approval.query.delete()
                lst = [models.Approval(line[0], line[1]) for line in filecontent]
                db.session.add_all(lst)
                db.session.commit()
                anz = models.Approval.query.count()
                flash(u' %s Zeilen gelöscht %s Zeilen aus %s gelesen, insgesamt %s Einträge' % (gel, len(lst), fp.filename, anz), 'success')
            except (IndexError, csv.Error) as e:
                flash(u'Zulassungen konnten nicht eingelesen werden (\';\' als Trenner verwenden): {0}'.format(e), 'danger')                
                return redirect(url_for('zulassungen'))

            return redirect(url_for('datainput'))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        return redirect(url_for('zulassungen'))
    return None


@auth_required
@templated('internal/datainput/priority.html')
def priority():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            filecontent = csv.reader(fp, delimiter=';')
            flash(u'Not ready yet!', 'warning')
            # try: 
                # for line in filecontent:
                    # app = models.Applicant(line[3], line[4], line[5], line[1], line[2], line[6], line[9], line[8], line[7]) 
                    # applicant = db.session.add(app)
                    # attendance = db.session.add(applicant, status, course)
                # db.session.commit()
                # anz = models.Approval.query.count()
                # flash(u' %s Zeilen aus %s gelesen, insgesamt %s Einträge' % (len(lst), fp.filename, anz), 'success')
            # except (IndexError, csv.Error) as e:
                # flash(u'Zulassungen konnten nicht eingelesen werden (\';\' als Trenner verwenden): {0}'.format(e), 'danger')                
                # return redirect(url_for('priority'))

            return redirect(url_for('datainput'))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        return redirect(url_for('priority'))
    return None


@auth_required
@templated('internal/notifications.html')
def notifications():
    form = NotificationForm()

    if form.validate_on_submit():
        try:
            # Do not leak mail addresses -- bcc, because the message is unique anyway
            bcc = form.get_bcc() + form.get_recipients()

            msg = Message(sender=g.user, recipients=[g.user], subject=form.mail_subject.data, body=form.mail_body.data,
                          cc=form.get_cc(), bcc=bcc, reply_to=form.get_reply_to())
            mail.send(msg)

            flash(u'Mail erfolgreich verschickt', 'success')
            return redirect(url_for('internal'))

        except (AssertionError, socket.error) as e:
            flash(u'Mail wurde nicht verschickt: {0}'.format(e), 'danger')

    return dict(form=form)


@auth_required
@templated('internal/lists.html')
def lists():
    # list of tuple (lang, aggregated number of courses, aggregated number of seats)
    lang_misc = db.session.query(models.Language, func.count(models.Language.courses), func.sum(models.Course.limit)) \
                          .join(models.Course, models.Language.courses) \
                          .group_by(models.Language) \
                          .order_by(models.Language.name) \
                          .all()

    return dict(lang_misc=lang_misc)


@auth_required
@templated('internal/language.html')
def language(id):
    return dict(language=models.Language.query.get_or_404(id))


@auth_required
@templated('internal/course.html')
def course(id):
    return dict(course=models.Course.query.get_or_404(id))


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
            applicant.origin = models.Origin.query.get(form.origin.data) 
            db.session.commit()
            flash(u'Der Bewerber wurde aktualisiert', 'success')
        except Exception as e:
            db.session.rollback()
            flash(u'Der Bewerber konnte nicht aktualisiert werden: {0}'.format(e), 'danger')
            return dict(form=form)

    form.populate(applicant)
    return dict(form=form)


@auth_required
@templated('internal/applicants/search_applicant.html')
def search_applicant():
    return dict(applicants=models.Applicant.query.order_by(models.Applicant.last_name).all())


@auth_required
@templated('internal/applicants/applicant_attendances.html')
def applicant_attendances(id):
    return dict(applicant=models.Applicant.query.get_or_404(id))


@auth_required
@templated('internal/payments.html')
def payments():
    form = PaymentForm()

    if form.validate_on_submit():
        code = form.confirmation_code.data
        match = re.search(r'^A(?P<a_id>\d{1,})C(?P<c_id>\d{1,})$', code)

        if match:
            a_id, c_id = match.group('a_id', 'c_id')
            return redirect(url_for('status', applicant_id=a_id, course_id=c_id))

        flash(u'Belegungsnummer ungültig', 'danger')
    
    return dict(form=form)


@auth_required
@templated('internal/status.html')
def status(applicant_id, course_id):
    attendance = models.Attendance.query.get_or_404((applicant_id, course_id))
    form = StatusForm()
    
    if form.validate_on_submit():
        try:
            attendance.waiting =    form.waiting.data
            attendance.has_to_pay = form.has_to_pay.data
            attendance.discounted = form.discounted.data
            attendance.paidbycash = form.paidbycash.data
            attendance.amountpaid = form.amountpaid.data 
            db.session.commit()
            flash(u'Der Status wurde aktualisiert', 'success')
        except Exception as e:
            db.session.rollback()
            flash(u'Der Status konnte nicht aktualisiert werden: {0}'.format(e), 'danger')
            return dict(form=form, attendance=attendance)
            
    form.populate(attendance)
    return dict(form=form, attendance=attendance)


# vim: set tabstop=4 shiftwidth=4 expandtab:
