#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdfix.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
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
