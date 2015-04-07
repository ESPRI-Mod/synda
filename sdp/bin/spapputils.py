#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains 'spapp' utils routine."""

import os
import sys
import __main__
import signal
import sptools

def print_exception(type_, value, tb):
    import os,sys,traceback,datetime # note: those imports must be done here (i.e. it doesn't work if done top of the file)

    def stderr(msg=''):
        sys.stderr.write("%s\n"%msg)

    stderr()
    stderr('*** Error occured at %s ***'%datetime.datetime.now().isoformat(" "))
    stderr()

    if value.__class__.__name__=="SPException":
        stderr('Error code: %s'%value.code)
        stderr('Error message: %s'%value.msg)
        stderr()

        if 'SP_DEBUG' in os.environ:
            if os.environ.get('SP_DEBUG')=="1":
                stderr('Stacktrace:')
                traceback.print_tb(tb)
    else:
        traceback.print_exception(type_, value, tb)

def set_exception_handler():
    sys.excepthook=print_exception

def singleton_check(file_):
    if os.path.isfile(file_):
        sptools.print_stderr("%s already exists, exiting" % file_)
        sys.exit(1)

def create_IHM_pid_file(file_):
    with open(file_, 'w') as fh:
        fh.write(str(os.getpid()))

def from_signal_to_atexit(signum, stackframe):
    raise SystemExit # To make sure atexit registered funcs are called also in the signal case.

def signal_init():
    # handle signals (atexit don't handle signal)
    signal.signal(signal.SIGINT, from_signal_to_atexit)
    signal.signal(signal.SIGTERM, from_signal_to_atexit)
