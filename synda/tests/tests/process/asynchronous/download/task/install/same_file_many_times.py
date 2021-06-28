# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from synda.sdt import sdfiledao
from synda.sdt.sdtypes import File

from synda.source.db.task.file.read.models import get_all_rows
from synda.source.db.connection.models import Connection


if __name__ == '__main__':
    """
    install -s /home_local/journoud/DEV/WORKSPACES/synda/selection/sample/sample_selection_01_bis.txt before execution
    """

    conn = Connection()
    all_rows = get_all_rows()
    row = all_rows[0]
    _file = File(**row)
    local_path0 = _file.local_path
    prefix = local_path0.split(".")[0]
    extend = local_path0.split(".")[1]
    nb_duplication = 10

    for i in range(nb_duplication):
        _file = File(**row)
        # set new local_path
        prefix = _file.local_path.split(".nc")[0]
        local_path = ".".join(
            [
                "_".join([prefix, str(i)]),
                "nc",
            ]

        )

        _file.local_path = local_path

        # set new file_functional_id
        prefix = _file.file_functional_id.split(".nc")[0]
        file_functional_id = ".".join(
            [
                "_".join([prefix, str(i)]),
                "nc",
            ]

        )

        _file.file_functional_id = file_functional_id

        sdfiledao.add_file(_file, commit=True, conn=conn.get_database_connection())
