# -*- coding: utf-8 -*-

"""Formatter that writes csv files.
"""

import csv
import io


class CSVWriter:

    default_template = {  # needs to be ordered
        'Kurs': 'course.full_name',
        'Nachname': 'applicant.last_name',
        'Vorname': 'applicant.first_name',
        'Hochschule': 'applicant.origin.short_name',
        'Matrikelnummer': 'applicant.tag',
        'E-Mail': 'applicant.mail',
        'Telefon': 'applicant.phone'
    }

    def __init__(self, template=default_template):
        self.buf = io.StringIO()
        self.out = csv.writer(self.buf, delimiter=";", dialect=csv.excel)
        self.header_written = False
        self.template = template

    def write_heading(self):
        if not self.header_written:
            self.write_row(self.template.keys())
            self.header_written = True

    def get_nested_value(self, element, key):
        path = key.split('.')
        value = element
        while path:
            subkey = path.pop(0)
            if isinstance(value, dict):
                value = value.get(subkey)
            elif hasattr(value, subkey):
                value = getattr(value, subkey)
            else:
                return None
        return value

    def write_element(self, element):
        row = [self.get_nested_value(element, key) for key in self.template.values()]
        self.write_row(row)

    def write_row(self, values):
        string_values = [str(v) if v else '' for v in values]
        self.out.writerow(string_values)

    def new_section(self, name):
        # CSV does not support sections
        pass

    def get_data(self):
        return self.buf.getvalue()
