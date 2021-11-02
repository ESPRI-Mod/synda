# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import humanize
from tabulate import tabulate
from synda.source.db.task.file.read.models import get_all_rows


def watchdog_report():
    all_rows = get_all_rows()
    li=[]
    for row in all_rows:
        li.append(
            [
                humanize.naturalsize(row['size'], gnu=False),
                row['filename'],
            ],
        )

    if len(li) > 0:
        print(
            tabulate(
                li,
                headers=['Total size', 'Filename'],
                tablefmt="plain",
            ),
        )
    else:
        print('No record in File table')


if __name__ == '__main__':
    watchdog_report()
