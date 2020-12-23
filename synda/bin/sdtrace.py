#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains alias routines."""

import inspect
import sys
import datetime
import traceback
import sdconfig

# -- trace funcs -- #

def log_message(msg):
    frame,outer_filename,outer_line_number,outer_function_name,lines,index = inspect.stack()[1] # warning: must stay in this func

    with open(sdconfig.stacktrace_log_file,'a') as fh:
        fh.write("=============\n")
        fh.write("Trace function called from '%s' file in '%s' function at line %d\n"%(outer_filename,outer_function_name,outer_line_number))
        fh.write("Message printed at %s\n"%datetime.datetime.now())
        fh.write('%s\n'%msg)

def log_exception(stderr=False):
    frame,outer_filename,outer_line_number,outer_function_name,lines,index = inspect.stack()[1] # warning: must stay in this func

    with open(sdconfig.stacktrace_log_file,'a') as fh:
        fh.write("=============\n")
        fh.write("Trace function called from '%s' file in '%s' function at line %d\n"%(outer_filename,outer_function_name,outer_line_number))
        fh.write("Exception occured at %s\n"%datetime.datetime.now())
        traceback.print_exc(file=fh)

    if stderr:
        traceback.print_exc(file=sys.stderr)

def debug(msg):
    with open('/tmp/synda_debug.log','a') as fh:
        fh.write("====== %s =======\n"%msg)

# init.
