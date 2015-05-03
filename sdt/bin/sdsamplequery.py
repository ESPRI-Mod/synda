#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains SQL routines used by sdsample module."""

import sdapp
import sddb

def get_local_projects(conn=sddb.conn):
    """Returns discovered projects"""
    projects=[]

    c=conn.cursor()
    c.execute("select distinct project from dataset")
    rs=c.fetchone()
    while rs is not None:
        projects.append(rs['project'])
        rs=c.fetchone()
    c.close()

    return projects
