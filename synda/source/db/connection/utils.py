# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sys
import sqlite3


# multiple connections to single database
def multi_connect(conn_num):
    db_name = 'x.db'
    conns = []
    for i in range(0, conn_num):
        try:
            conn = sqlite3.connect(db_name)
            print('connect ok at %d' % i)
        except Exception as e:
            print('connect failed at %d' % i)
            sys.exit(-1)


if __name__ == '__main__':
    multi_connect(2000)
