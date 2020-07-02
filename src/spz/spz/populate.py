# -*- coding: utf-8 -*-

"""Holds popuplation logic."""

import socket
from datetime import datetime

from redis import ConnectionError

from sqlalchemy import orm

from spz import db, models, tasks

from spz.mail import generate_status_mail

from spz.util.WeightedRandomGenerator import WeightedRandomGenerator


def eager_load_waiting():
    """Eager load all waiting attendances ordered by `registered`."""
    # eager loading, see (search for 'subqueryload'):
    # http://docs.sqlalchemy.org/en/rel_0_9/orm/loading_relationships.html
    return models.Attendance.query \
        .options(orm.subqueryload(models.Attendance.applicant).subqueryload(models.Applicant.attendances)) \
        .filter_by(waiting=True) \
        .order_by(models.Attendance.registered) \
        .all()


def send_mails(attendances):
    """Send mails to handled (successful or not) attendances."""
    try:
        for attendance, informed_before_now in attendances:
            # consider this a restock if we already send out a "no, sorry" mail
            restock = informed_before_now

            tasks.send_slow.delay(
                generate_status_mail(attendance.applicant, attendance.course, restock=restock),
            )

    except (AssertionError, socket.error, ConnectionError) as e:
        raise e


def populate_generic(time, attendance_filter, idx_prepare, idx_select):
    """Generic populate implementation.

    :param time: current UTC time
    :param attendance_filter: function that accepts one `Attendance` arguments and must return True if
                              attendance should be considered for this populate procedure.
    :param idx_prepare: function that gets a list of all possible attendances and can prepare the
                        `idx_select` function (see below).
    :param idx_select: function that gets a list of all remaining but possible attendances and must
                       return the index of the attendance that should be tried.


    First this method selects all attendances (called candidiates) which:
    - are not waiting
    - where the course is not in manual assignment period anymore
    - where `attendance_filter` return True

    Afterwards, it calls `idx_prepare`. Finally, it loops until no candidiates remain and in every round it:
    1. calls `idx_select` to select a candidiate.
    2. checks if the candidiate is not signed up for a parallel course
    3. checks if the specified course is not full
    4. if all conditions hold, it signs up the candidate.

    Finally, it prepares emails for all candidates that:
    - successfully entered a course
    - got rejected for the first time
    """
    # only non-manual-mode courses
    to_assign = [
        att
        for att
        in eager_load_waiting()
        if attendance_filter(att) and not att.course.language.is_in_manual_mode(time)
    ]

    # keep track of which attendances we set to active/waiting
    handled_attendances = []

    idx_prepare(to_assign)

    while to_assign:
        attendance = to_assign.pop(idx_select(to_assign))

        if attendance.applicant.active_in_parallel_course(attendance.course):
            # XXX: how can this happen? should we send a message to someone?
            attendance.informed_about_rejection = True
            continue

        # keep default waiting status
        if attendance.course.is_full:
            if not attendance.informed_about_rejection:
                handled_attendances.append((attendance, attendance.informed_about_rejection))
                attendance.informed_about_rejection = True
            continue

        attendance.discount = attendance.applicant.current_discount()
        attendance.set_waiting_status(False)
        handled_attendances.append((attendance, attendance.informed_about_rejection))
        attendance.informed_about_rejection = True

    try:
        db.session.commit()
        # XXX: send stats somewhere
    except Exception as e:
        db.session.rollback()
        raise e

    # Send mails (async) only if the commit was successfull -- be conservative here
    send_mails(handled_attendances)


def populate_rnd(time):
    """Run RND populate procedure.

       :param time: current UTC time
    """

    # Interval filtering in Python instead of SQL because it's not portable (across SQLite, Postgres, ..)
    # implementable in standard SQL
    # See: https://groups.google.com/forum/#!msg/sqlalchemy/AneqcriykeI/j4sayzZP1qQJ

    weights = []

    def attendance_filter(att):
        return (att.course.language.signup_begin) < att.registered < (att.course.language.signup_rnd_window_end)

    def idx_prepare(to_assign):
        # (attendance, weight) tuples from query would be possible, too;
        # eager loading already takes care of not issuing tons of sql queries here
        # XXX: re-decide if we should consider all attendances, or only some
        nonlocal weights
        weights = [
            1.0 / max(
                1.0,
                len([
                    att
                    for att
                    in attendance.applicant.attendances
                ])
            )
            for attendance
            in to_assign
        ]

    def idx_select(to_assign):
        assert len(to_assign) == len(weights)

        # weighted random selection
        gen = WeightedRandomGenerator(weights)
        idx = next(gen)

        del weights[idx]
        return idx

    populate_generic(time, attendance_filter, idx_prepare, idx_select)


def populate_fcfs(time):
    """Run FCFS populate procedure.

       :param time: current UTC time

    To ensure fairness, courses are shuffled before fill-up.
    """

    def attendance_filter(att):
        return True

    def idx_prepare(to_assign):
        pass

    def idx_select(to_assign):
        return 0

    populate_generic(time, attendance_filter, idx_prepare, idx_select)


def update_waiting_list_status():
    """Update waiting list status of all courses."""
    courses = models.Course.query.all()
    for c in courses:
        c.has_waiting_list = c.is_full
    db.session.commit()


def populate_global():
    """Run global populate procedure as discussed with management."""
    time = datetime.utcnow()
    populate_rnd(time)
    populate_fcfs(time)
    update_waiting_list_status()
