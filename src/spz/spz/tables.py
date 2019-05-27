# -*- coding: utf-8 -*-

"""Table export utility.

   Used to format course lists for download.
"""

import csv
import io
from tempfile import NamedTemporaryFile
from openpyxl import Workbook

from flask import make_response, url_for, redirect, flash


def export_course_list(courses, format):
    if format == 'csv':
        return export(CSVWriter(), courses)
    elif format == 'xlsx':
        return export(ExcelWriter(), courses)
    else:
        flash('Ungueltiges Export-Format: {0}'.format(format), 'error')
        return redirect(url_for('lists'))


class CSVWriter:

    mimetype = 'text/csv'

    def __init__(self):
        self.buf = io.StringIO()
        self.out = csv.writer(self.buf, delimiter=";", dialect=csv.excel)
        self.mimetype = 'text/csv'
        self.filename = 'Kursliste.csv'
        self.header_written = False

    def write_heading(self, values):
        if not self.header_written:
            self.write_row(values)
            self.header_written = True

    def write_row(self, values):
        string_values = [str(v) if v else '' for v in values]
        self.out.writerow(string_values)

    def new_section(self, name):
        pass

    def get_data(self):
        return self.buf.getvalue()


class ExcelWriter:

    def __init__(self):
        self.workbook = Workbook(write_only=True)
        self.mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        self.filename = 'Kursliste.xlsx'

    def write_heading(self, values):
        self.write_row(values)

    def write_row(self, values):
        self.workbook._sheets[-1].append(values)

    def new_section(self, name):
        self.workbook.create_sheet(name)

    def get_data(self):
        with NamedTemporaryFile() as file:
            self.workbook.save(file.name)
            file.seek(0)
            stream = file.read()
        return stream


def export(writer, courses):
    # XXX: header -- not standardized
    header = ['Kurs', 'Kursplatz', 'Bewerbernummer', 'Vorname', 'Nachname', 'Mail',
              'Matrikelnummer', 'Telefon', 'Studienabschluss', 'Semester', 'Bewerberkreis']

    for course in courses:
        writer.new_section(course.full_name())
        writer.write_heading(header)

        active_no_debt = [attendance.applicant for attendance in course.attendances
                          if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]

        idx = 1
        for applicant in active_no_debt:
            writer.write_row([course.full_name(),
                              idx,
                              applicant.id,
                              applicant.first_name,
                              applicant.last_name,
                              applicant.mail,
                              applicant.tag,
                              applicant.phone,
                              applicant.degree.name if applicant.degree else None,
                              applicant.semester,
                              applicant.origin.name if applicant.origin else None])
            idx += 1

    resp = make_response(writer.get_data())
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}"'.format(writer.filename)
    resp.mimetype = writer.mimetype

    return resp
