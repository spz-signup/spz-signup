# -*- coding: utf-8 -*-

"""Export module for course lists.

   Formatters are loaded dynamically by their file name.
"""

from flask import make_response

from .excel import ExcelWriter
from .csv import CSVWriter


formatters = {
    'excel': ExcelWriter,
    'csv': CSVWriter
}


def export_course_list(courses, format, filename='Kursliste', sectionize=True):
    return export(format, courses, filename, sectionize)


def export(format, courses, filename, sectionize):
    writer = format.init_formatter()

    if not sectionize:
        writer.new_section(filename)
        writer.write_heading()
    for course in courses:
        if sectionize:
            writer.new_section(course.full_name())
            writer.write_heading()

        active_no_debt = sorted(attendance.applicant for attendance in course.get_paid_attendances())

        for applicant in active_no_debt:
            writer.write_element(applicant)

    resp = make_response(writer.get_data())
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}.{1}"'.format(filename, format.extension)
    resp.mimetype = format.mimetype

    return resp
