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


class CSVWriter:

    def __init__(self, template_path):
        self.buf = io.StringIO()
        self.out = csv.writer(self.buf, delimiter=';')
        self.header_written = False
        self.template = read_template(template_path)

    def write_heading(self):
        if not self.header_written:
            self.write_row(self.template['keys'])
            self.header_written = True

    def write_element(self, element):
        row = [value(element) for value in self.template['values']]
        self.write_row(row)

    def write_row(self, values):
        self.out.writerow(values)

    def new_section(self, name):
        # CSV does not support sections
        pass

    def get_data(self):
        return self.buf.getvalue()
