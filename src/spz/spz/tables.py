# -*- coding: utf-8 -*-

"""Table export utility.

   Used to format course lists for download.
"""

import csv
import io

from flask import make_response, url_for, redirect, flash


def export_course_list(courses, format):
    if format == 'csv': return csv_export(courses)
    else:
        flash('Ungültiges Export-Format: {0}'.format(format), 'error')
        return redirect(url_for('lists'))


def csv_export(courses):
    buf = io.StringIO()
    out = csv.writer(buf, delimiter=";", dialect=csv.excel)

    # XXX: header -- not standardized
    out.writerow(['Kurs', 'Kursplatz', 'Bewerbernummer', 'Vorname', 'Nachname', 'Mail',
                  'Matrikelnummer', 'Telefon', 'Studienabschluss', 'Semester', 'Bewerberkreis'])

    def maybe(x):
        return x if x else ''

    for course in courses:
        active_no_debt = [attendance.applicant for attendance in course.attendances
                          if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]

        idx = 1
        for applicant in active_no_debt:
            out.writerow(['{0}'.format(course.full_name()),
                          '{0}'.format(idx),
                          '{0}'.format(applicant.id),
                          applicant.first_name,
                          applicant.last_name,
                          applicant.mail,
                          maybe(applicant.tag),
                          maybe(applicant.phone),
                          applicant.degree.name if applicant.degree else '',
                          '{0}'.format(maybe(applicant.semester)),
                          applicant.origin.name if applicant.origin else ''])
            idx += 1

    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = 'attachment; filename="Kursliste.csv"'
    resp.mimetype = 'text/csv'

    return resp
