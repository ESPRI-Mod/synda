#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'sdapp' utils routine."""

import os
import sys
import signal
import sdtools

def print_exception(type_, value, tb):
    import os,sys,traceback,datetime # note: those imports must be done here (i.e. it doesn't work if done top of the file)

    def stderr(msg=''):
        sys.stderr.write("%s\n"%msg)

    stderr()
    stderr('*** Error occured at %s ***'%datetime.datetime.now().isoformat(" "))
    stderr()

    if value.__class__.__name__=="SDException":
        stderr()
        stderr('==================')
        stderr('*   Error code   *')
        stderr('==================')
        stderr()
        stderr('%s'%value.code)
        stderr()
        stderr()
        stderr('=====================')
        stderr('*   Error message   *')
        stderr('=====================')
        stderr()
        stderr('%s'%value.msg)
        stderr()

        if 'ST_DEBUG' in os.environ:
            if os.environ.get('ST_DEBUG')=="1":
                stderr('Stacktrace:')
                traceback.print_tb(tb)
    else:
        traceback.print_exception(type_, value, tb)

def set_exception_handler():
    sys.excepthook=print_exception

def singleton_check(file_):
    if os.path.isfile(file_):
        sdtools.print_stderr("%s already exists, exiting" % file_)
        sys.exit(1)

def create_IHM_pid_file(file_):
    with open(file_, 'w') as fh:
        fh.write(str(os.getpid()))

def from_signal_to_atexit(signum, stackframe):
    raise SystemExit # To make sure atexit registered funcs are called also in the signal case.

def signal_init():
    """
    Handle signals (atexit don't handle signal)
    
    Note
        Used in IHM mode only
    """

    signal.signal(signal.SIGINT, from_signal_to_atexit)
    signal.signal(signal.SIGTERM, from_signal_to_atexit)
