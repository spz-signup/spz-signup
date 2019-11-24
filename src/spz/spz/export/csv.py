# -*- coding: utf-8 -*-

"""Formatter that writes csv files.
"""

from . import TableWriter

import csv
import io


class CSVWriter(TableWriter):

    mimetype = 'text/csv'

    extension = 'csv'

    template_file_mode = 'r'

    def __init__(self, template, delimiter=';'):
        self.delimiter = delimiter
        self.buf = io.StringIO()
        self.out = csv.writer(self.buf, delimiter=self.delimiter)
        TableWriter.__init__(self, template, binary_template=False)

    def parse_template(self, file):
        reader = csv.reader(file, delimiter=self.delimiter)
        # read heading from first row
        self.write_row(next(reader))
        # parse jinja expressions from second row
        return super().parse_template(next(reader))

    def write_row(self, values):
        self.out.writerow(values)

    def get_data(self):
        return self.buf.getvalue()
