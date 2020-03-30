#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from tabulate import tabulate
from sdt.bin.db import dao
from sdt.bin.db import session


def run(args):
    """
    retrieves all history lines from db and prints them in a table.
    :param args:
    :return:
    """
    with session.create():
        li = [h.to_list() for h in dao.get_all_history_lines()]
    print(tabulate(li, headers=['action', 'selection source', 'date', 'insertion_group_id'], tablefmt="orgtbl"))
