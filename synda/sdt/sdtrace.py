#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from synda.source.config.file.log.models import Config


def log_message(msg):

    # warning: must stay in this func
    frame, outer_filename, outer_line_number, outer_function_name, lines, index = inspect.stack()[1]

    with open(Config().get("stack_trace"), 'a') as fh:
        fh.write("=============\n")
        fh.write(
            "Trace function called from '{}' file in '{}' function at line {}\n".format(
                outer_filename,
                outer_function_name,
                outer_line_number,
            ),
        )
        fh.write(
            "Message printed at {}\n".format(
                datetime.datetime.now(),
            ),
        )
        fh.write('{}\n'.format(msg))


def log_exception(stderr=False):

    # warning: must stay in this func
    frame, outer_filename, outer_line_number, outer_function_name, lines, index = inspect.stack()[1]

    with open(Config().get("stack_trace"), 'a') as fh:
        fh.write("=============\n")
        fh.write(
            "Trace function called from '{}' file in '{}' function at line {}\n".format(
                outer_filename,
                outer_function_name,
                outer_line_number,
            ),
        )
        fh.write(
            "Exception occured at {}\n".format(
                datetime.datetime.now(),
            ),
        )

        traceback.print_exc(file=fh)

    if stderr:
        traceback.print_exc(file=sys.stderr)


def debug(msg):

    with open(Config().get("debug"), 'a') as fh:
        fh.write(
            "======= {} =======\n".format(
                msg,
            ),
        )

