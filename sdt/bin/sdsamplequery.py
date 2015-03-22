#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdsamplequery.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
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
