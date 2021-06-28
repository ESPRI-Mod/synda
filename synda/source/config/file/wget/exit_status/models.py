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
from synda.source.readers import Reader as Base
from synda.source.config.file.wget.exit_status.constants import DELIMITER

from synda.source.config.file.wget.exit_status.constants import DEFAULT_FULL_FILENAME

from synda.source.config.file.wget.exit_status.exceptions import InvalidExistStatus
from synda.source.config.file.wget.exit_status.exceptions import UnknownStatusError


class Reader(Base):
    """
    Wget exits status file reader

    """
    def __init__(self):
        super(Reader, self).__init__(DEFAULT_FULL_FILENAME, DELIMITER)

    def validate(self, code):

        # parsing
        parsing_ok = False

        if isinstance(code, int):
            parsing_ok = True
        elif isinstance(code, str):
            try:
                int(code)
                parsing_ok = True
            except ValueError:
                pass

        # validation
        validated = False

        if parsing_ok:
            ivalue: int = int(code)
            if -1 < ivalue < 9:
                code = ivalue
                validated = True

        if not validated:
            raise InvalidExistStatus(code, self.full_filename)

        return code

    def _get_line(self, code):
        code = self.validate(code)
        if code in self._data.index:
            res = self._data.loc[code]
        else:
            raise UnknownStatusError(code, self.full_filename)
        return res

    def get_exit_status_message(self, index):
        return self._get_line(index)["message"]
