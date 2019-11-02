# -*- coding: utf-8 -*-

"""Export module for course lists.

   Formatters are loaded dynamically by their file name.
"""

from flask import make_response

from .excel import ExcelCourseWriter
from .csv import CSVCourseWriter


formatters = {
    'excel': ExcelCourseWriter,
    'csv': CSVCourseWriter
}


def export_course_list(courses, format, filename='Kursliste'):
    formatter = format.init_formatter()
    formatter.process(courses)

    resp = make_response(formatter.get_data())
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}.{1}"'.format(filename, format.extension)
    resp.mimetype = formatter.mimetype

    return resp
