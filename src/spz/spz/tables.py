# -*- coding: utf-8 -*-

"""Table export utility.

   Used to format course lists for download.
"""

import csv
import io
from tempfile import NamedTemporaryFile
from openpyxl import Workbook

from flask import make_response, send_file, url_for, redirect, flash


def export_course_list(courses, format):
    if format == 'csv':
        return csv_export(courses)
    elif format == 'xlsx':
        return excel_export(courses)
    else:
        flash('Ungueltiges Export-Format: {0}'.format(format), 'error')
        return redirect(url_for('lists'))


class CSVWriter:

    mimetype = 'text/csv'

    def __init__(self):
        self.buf = io.StringIO()
        self.out = csv.writer(self.buf, delimiter=";", dialect=csv.excel)

    def write_heading(self, values):
        self.write_row(values)

    def write_row(self, values):
        self.out.writerow(values)
    
    def get_data(self):
        return self.buf.getvalue()


def csv_export(courses):
    writer = CSVWriter()

    # XXX: header -- not standardized
    writer.write_heading(['Kurs', 'Kursplatz', 'Bewerbernummer', 'Vorname', 'Nachname', 'Mail',
                  'Matrikelnummer', 'Telefon', 'Studienabschluss', 'Semester', 'Bewerberkreis'])

    def maybe(x):
        return x if x else ''

    for course in courses:
        active_no_debt = [attendance.applicant for attendance in course.attendances
                          if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]

        idx = 1
        for applicant in active_no_debt:
            writer.write_row(['{0}'.format(course.full_name()),
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

    resp = make_response(writer.get_data())
    resp.headers['Content-Disposition'] = 'attachment; filename="Kursliste.csv"'
    resp.mimetype = writer.mimetype

    return resp


def excel_export(courses):
    wb = Workbook()
    wb.active.title = "Kursliste"
    with NamedTemporaryFile() as file:
        wb.save(file.name)
        file.seek(0)
        stream = file.read()
        resp = make_response(stream)
        resp.headers['Content-Disposition'] = 'attachment; filename="Kursliste.xlsx"'
        resp.mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return resp
