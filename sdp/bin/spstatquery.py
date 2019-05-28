#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""Contains statistics queries.
"""

import spapp
import spdb

def get_ppprun_stat():
    di={}

    conn=spdb.connect()
    c=conn.cursor()

    q='select project,status,count(*) as count from ppprun group by project,status'

    c.execute(q)
    rs=c.fetchone()
    if rs<>None:

        project=rs[0]
        status=rs[1]
        count=rs[2]

        if project not in di:
            di[project]={status:count}
        else:
            if status not in di[project]:
                di[project][status]=count
            else:
                assert False

        rs=c.fetchone()
    c.close()

    spdb.disconnect(conn)

    return di
