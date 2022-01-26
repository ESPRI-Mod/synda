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
from synda.source.db.task.file.read.models import get_row
from synda.source.db.task.file.update.models import checksum as update_file_checksum


if __name__ == '__main__':
    file_id = 1
    row = get_row(file_id)
    print(
        f'Checksum before updating : {row["checksum"]}',
    )
    if row:
        checksum = ""
        success = update_file_checksum(file_id, checksum)
        row = get_row(file_id)
        print(
            f'Checksum after updating  : {row["checksum"]}',
        )
        pass
