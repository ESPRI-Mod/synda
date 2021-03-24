#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from synda.sdt import sdtools
from synda.sdt import sdexception

from synda.source.config.path.tree.models import Config as TreePath


def run():
    try:
        for f in sdtools.ls(TreePath().get("db"), 'sdt_transient_storage_*'):
            if is_recent(f) or is_pid_alive(f):
                pass
            else:
                os.unlink(f)

    except Exception:
        pass


def is_recent(f):
    age = file_age_in_seconds(f)

    # two days
    if age < (86400*2):
        return True
    else:
        return False


def is_pid_alive(f):
    pid = get_pid_from_filename(f)
    pid_proc_folder = "/proc/%s" % pid

    # TAG8UUJIHJH8Y8Y
    if os.path.exists(pid_proc_folder):
        return True
    else:
        return False


def get_pid_from_filename(f):
    match = re.search('^.*sdt_transient_storage_([^_]+)_[^_]+$', f)
    if match:
        pid = match.group(1)
    else:
        raise sdexception.SDException("SYNDTDBF-001", "Incorrect filename format (%s)" % (f,))

    return pid


def file_age_in_seconds(pathname):
    age = time.time() - os.path.getmtime(pathname)
    return int(age)
