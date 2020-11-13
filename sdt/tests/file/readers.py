# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
import os

from sdt.source.readers import read_data, read_csv, read_header

from sdt.tests.file.exceptions import NotFound as FileNotFound
from sdt.tests.file.exceptions import FormatError as FileFormatError


class Reader(object):
    """
    Basic ile reader

    """
    def __init__(self, full_filename, delimiter):
        self.full_filename = full_filename
        self.delimiter = delimiter
        self._data = None
        self.init()

    def _validate(self):
        res = False
        if os.path.exists(self.full_filename):
            res = True
        else:
            raise FileNotFound(self.full_filename)

        if not res:
            raise FileFormatError(self.full_filename)

        return res

    def init(self, header=0):
        if self._validate():
            self.read(header)

    def read(self, header=0, index_col=True):
        names = \
            read_header(self.full_filename, delimiter=self.delimiter)

        if index_col:
            self._data = \
                read_data(
                    self.full_filename,
                    sep=self.delimiter,
                    header=header,
                    names=names,
                    index_col=names[0])
        else:
            self._data = \
                read_data(
                    self.full_filename,
                    sep=self.delimiter,
                    header=header,
                    names=names,
                    index_col=False)

    def get_columns(self):
        return self._data.columns.tolist()

    def get_index(self):
        return self._data.index

    def _get_dataframe(self):
        return self._data


if __name__ == '__main__':
    pass
