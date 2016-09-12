#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains transient DB file cleanup routine."""

import os
import re
import sdtools
import sdconfig
import sdexception

def cleanup():
    try:
        for f in sdtools.ls(sdconfig.db_folder,'sdt_transient_storage_*'):
            if is_recent() or is_pid_alive():
                pass
            else:
                os.unlink(f)
    except Exception as e:
        pass

def is_recent(f):
    TODO
    crea_date=get_crea_date(f)

def is_pid_alive():
    pid=get_pid_from_filename(f)
    pid_proc_folder="/proc/%s"%pid
    return os.path.exists(pid_proc_folder) # TAG8UUJIHJH8Y8Y

def get_pid_from_filename(f):
    match=re.search('^sdt_transient_storage_([^_]+)_[^_]+$',f)
    if match!=None:
        pid=match.group(1)
    else:
        raise sdexception.SDException("SYNDTDBF-001","Incorrect filename format (%s)"%(f,))

    return pid

def get_crea_date(f):
    TODO
    try:
        l__epoch=os.path.getatime(f)
        date_str=datetime.datetime.fromtimestamp(l__epoch).strftime('%Y-%m-%d %H:%M:%S.%f')
        return date_str
    except FileNotFoundException,e:
        continue

    except Exception,e:
        sdlog.error("SDOPERAT-532","Fatal error (%s)"%str(e))
        raise
