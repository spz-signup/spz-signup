# -*- coding: utf-8 -*-

"""Formatter that writes csv files.
"""

import csv
import io


class CSVWriter:

    def __init__(self):
        self.buf = io.StringIO()
        self.out = csv.writer(self.buf, delimiter=";", dialect=csv.excel)
        self.header_written = False

    def write_heading(self, values):
        if not self.header_written:
            self.write_row(values)
            self.header_written = True

    def write_row(self, values):
        string_values = [str(v) if v else '' for v in values]
        self.out.writerow(string_values)

    def new_section(self, name):
        # CSV does not support sections
        pass

    def get_data(self):
        return self.buf.getvalue()
