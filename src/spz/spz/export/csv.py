# -*- coding: utf-8 -*-

"""Formatter that writes csv files.
"""

import csv
import io

from spz import app


def read_template(template_path):
    with app.open_resource('templates/' + template_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        template = {}
        template['keys'] = next(reader)
        template['values'] = [app.jinja_env.compile_expression(key) for key in next(reader)]
        return template


class CSVCourseWriter:

    def __init__(self, template_path):
        self.buf = io.StringIO()
        self.out = csv.writer(self.buf, delimiter=';')
        self.header_written = False
        self.template = read_template(template_path)

    def process(self, courses):
        self.write_row(self.template['keys'])  # write heading
        for course in courses:  # write data
            for applicant in course.course_list:
                self.write_element({'course': course, 'applicant': applicant})

    def write_element(self, element):
        row = [value(element) for value in self.template['values']]
        self.write_row(row)

    def write_row(self, values):
        self.out.writerow(values)

    def get_data(self):
        return self.buf.getvalue()
