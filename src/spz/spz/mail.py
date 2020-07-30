# -*- coding: utf-8 -*-

"""Implements mail generators."""

from datetime import datetime
from pytz import timezone, utc

from flask import render_template
from flask_mail import Message
from flask_babel import gettext as _

from spz import app, models


def generate_status_mail(applicant, course, time=None, restock=False):
    """Generate mail to notify applicants about their new attendance status."""
    time = time or datetime.utcnow()
    attendance = models.Attendance.query \
        .filter(models.Attendance.applicant_id == applicant.id, models.Attendance.course_id == course.id) \
        .first()

    if attendance:
        # applicant is (somehow) registered for this course
        if attendance.waiting:
            # applicant is waiting, let's figure out if we are in RND or FCFS phase
            if course.language.is_open_for_signup_rnd(time):
                subject_status = _('Verlosungspool')
                template = 'mails/poolmail.html'
            else:
                subject_status = _('Warteliste')
                template = 'mails/waitinglistmail.html'
        else:
            # :) applicant is signed up for the course
            # let's differ according to the reason (normal procedure or manual restock)
            if restock:
                subject_status = _('Platz durch Nachrückverfahren')
                template = 'mails/restockmail.html'
            else:
                subject_status = _('Erfolgreiche Anmeldung')
                template = 'mails/registeredmail.html'
    else:
        # no registration exists => assuming she got kicked out
        subject_status = _('Platzverlust')
        template = 'mails/kickoutmail.html'
    # assigning timezone
    if attendance:
        signoff = attendance.signoff_window.replace(tzinfo=utc).astimezone(tz=timezone('Europe/Berlin'))
    else:
        signoff = False
    return Message(
        sender=app.config['PRIMARY_MAIL'],
        reply_to=course.language.reply_to,
        recipients=[applicant.mail],
        subject=_(
            '[Sprachenzentrum] Kurs %(course)s - %(status)s',
            course=course.full_name,
            status=subject_status),
        body=render_template(
            template,
            applicant=applicant,
            course=course,
            has_to_pay=not attendance.is_free if attendance else False,
            date=time,
            signoff_window=signoff
        ),
        charset='utf-8'
    )
