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
from synda.source.db.task.file.read.models import get_all_rows


def get_local_paths_and_sizes():
    all_rows = get_all_rows()
    data = []
    for row in all_rows:
        data.append(
            {
                "local_path": row["local_path"],
                "size": row["size"],
            }
        )

    return data


if __name__ == '__main__':
    print(
        get_local_paths_and_sizes()
    )
