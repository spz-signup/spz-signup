# -*- coding: utf-8 -*-

"""Implements mail generators."""

from datetime import datetime

from flask import render_template

from flask_mail import Message

from spz import app, models

from pytz import timezone
import pytz


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
                subject_status = 'Verlosungspool'
                template = 'mails/poolmail.html'
            else:
                subject_status = 'Warteliste'
                template = 'mails/waitinglistmail.html'
        else:
            # :) applicant is signed up for the course
            # let's differ according to the reason (normal procedure or manual restock)
            if restock:
                subject_status = 'Platz durch Nachrückverfahren'
                template = 'mails/restockmail.html'
            else:
                subject_status = 'Erfolgreiche Anmeldung'
                template = 'mails/registeredmail.html'
    else:
        # no registration exists => assuming she got kicked out
        subject_status = 'Platzverlust'
        template = 'mails/kickoutmail.html'
    # assigning timezone
    if attendance:
        signoff = attendance.signoff_window.replace(tzinfo=pytz.utc).astimezone(tz=timezone('Europe/Berlin'))
    else:
        signoff = False
    return Message(
        sender=app.config['PRIMARY_MAIL'],
        reply_to=course.language.reply_to,
        recipients=[applicant.mail],
        subject='[Sprachenzentrum] Kurs {0} - {1}'.format(course.full_name(), subject_status),
        body=render_template(
            template,
            applicant=applicant,
            course=course,
            has_to_pay=attendance.has_to_pay if attendance else False,
            date=time,
            signoff_window=signoff
        ),
        charset='utf-8'
    )
