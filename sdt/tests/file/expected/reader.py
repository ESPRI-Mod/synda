# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 Reader of the files that describe the 'expected downloaded files characteristics' CONCERNING the TESTS

 These files have the .expected extension and are created by a built process
"""
from sdt.tests.file.readers import Reader as Base
from .constants import DELIMITER
from sdt.tests.file.exceptions import IndexError


class Reader(Base):
    """
    Nationality file reader

    """
    def __init__(self, full_filename):
        super(Reader, self).__init__(full_filename, DELIMITER)

    def _get_line(self, filename):

        if filename in self._data.index:
            res = self._data.loc[filename]
        else:
            raise IndexError(filename, self.full_filename)
        return res

    def get_checksum(self, index):
        return self._get_line(index)["checksum"]
