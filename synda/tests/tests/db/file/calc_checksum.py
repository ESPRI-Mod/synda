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
from synda.sdt import sdtypes

from synda.source.db.task.file.read.models import get_all_rows as get_table_file_all_rows
from synda.source.process.checksum.models import calc_checksum


if __name__ == '__main__':
    all_rows = get_table_file_all_rows()
    row = all_rows[0]
    file_instance = sdtypes.File(**row)
    checksum = calc_checksum(
        file_instance.get_full_local_path(),
        file_instance.checksum_type,
    )
    print(checksum)
