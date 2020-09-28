# -*- coding: utf-8 -*-

"""Logging module, writes annoted logs to the database."""

from datetime import datetime

from sqlalchemy import event

from spz import db, models

from flask_babel import gettext as _


def log(msg, language=None, timestamp=None):
    """Create new log entry.

    When timestamp is `None`, then current time is used.
    """

    # fill in timestamp
    if timestamp is None:
        timestamp = datetime.utcnow()

    entry = models.LogEntry(timestamp, msg, language)
    db.session.add(entry)


@event.listens_for(models.Attendance.waiting, 'set')
def evt_set_attendance_waiting(target, value, oldvalue, _initiator):
    if value is False and oldvalue is True:
        course = target.course
        lang = course.language
        msg = _(
            '%(fname)s (%(mail)s) wurde in %(cname)s gebucht.',
            fname=target.applicant.full_name,
            mail=target.applicant.mail,
            cname=course.full_name
        )
        log(msg, language=lang)


@event.listens_for(models.Course.has_waiting_list, 'set')
def evt_set_course_wlstatus(target, value, oldvalue, _initiator):
    if value is not oldvalue:
        lang = target.language
        if value:
            msg = _(
                '%(cname)s hat nun eine Warteliste.',
                cname=target.full_name
            )
        else:
            msg = _(
                '%(cname)s ist nun Wartelisten-frei.',
                cname=target.full_name
            )
        log(msg, language=lang)


# XXX: extend event handling, e.g. for sending mails to applicants
