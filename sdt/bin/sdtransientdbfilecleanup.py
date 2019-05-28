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
import time
import sdtools
import sdconfig
import sdexception

def run():
    try:
        for f in sdtools.ls(sdconfig.db_folder,'sdt_transient_storage_*'):
            if is_recent(f) or is_pid_alive(f):
                pass
            else:
                os.unlink(f)
    except Exception as e:
        pass

def is_recent(f):
    age=file_age_in_seconds(f)

    if age < (86400*2): # two days
        return True
    else:
        return False

def is_pid_alive(f):
    pid=get_pid_from_filename(f)
    pid_proc_folder="/proc/%s"%pid

    if os.path.exists(pid_proc_folder): # TAG8UUJIHJH8Y8Y
        return True
    else:
        return False

def get_pid_from_filename(f):
    match=re.search('^.*sdt_transient_storage_([^_]+)_[^_]+$',f)
    if match!=None:
        pid=match.group(1)
    else:
        raise sdexception.SDException("SYNDTDBF-001","Incorrect filename format (%s)"%(f,))

    return pid

def file_age_in_seconds(pathname):
    age = time.time() - os.path.getmtime(pathname)
    return int(age)
