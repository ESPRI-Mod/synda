# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.sdt import sdfiledao
from synda.sdt.sdtypes import File


def delete_files(_files):
    sdfiledao.delete_file(_files)


if __name__ == '__main__':

    from synda.source.db.task.file.read.models import get_all_rows
    all_rows = get_all_rows()
    rows = all_rows[0:3]
    rows.extend(
        all_rows[4::],
    )
    # rows = all_rows[5::]
    # rows = all_rows[40::]

    # rows = all_rows[0:39]
    # rows.extend(
    #     all_rows[40::],
    # )

    # rows = all_rows[0:39]
    # rows.extend(
    #     all_rows[40::],
    # )
    # rows = all_rows[20::]
    # rows = all_rows
    for row in rows:
        _file = File(**row)
        sdfiledao.delete_file(_file)
