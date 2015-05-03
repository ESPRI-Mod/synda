#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains bug fixes.

Not used.
"""

import os
import re
import sys
import argparse
import sdapp
import sdlog
import sqlite3

def run(dbfile):
    conn=sqlite3.connect(dbfile)
    conn.row_factory=sqlite3.Row # this is for "by name" colums indexing

    conn.commit()
    conn.close()

# module init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dbfile',required=True)
    args = parser.parse_args()

    run(args.dbfile)
