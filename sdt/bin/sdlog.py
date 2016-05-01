#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains code related to logging."""

import sys
import logging
import argparse
import sdapp
import sdconst
import sdconfig
import sdtools
from sdexception import SDException

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

LABELS = {logging.DEBUG: 'debug',
          logging.INFO: 'info',
          logging.WARNING: 'warning',
          logging.ERROR: 'error',
          logging.CRITICAL: 'critical'}

def die(code,msg):
	critical(code,msg)
	sys.exit(1)

def debug(code,message,stdout=False,stderr=False,logfile=True):
    log(code,message,logging.DEBUG,stdout,stderr,logfile)
def info(code,message,stdout=False,stderr=False,logfile=True):
    log(code,message,logging.INFO,stdout,stderr,logfile)
def warning(code,message,stdout=False,stderr=False,logfile=True):
    log(code,message,logging.WARNING,stdout,stderr,logfile)
def error(code,message,stdout=False,stderr=False,logfile=True):
    log(code,message,logging.ERROR,stdout,stderr,logfile)
def critical(code,message,stdout=False,stderr=False,logfile=True):
    log(code,message,logging.CRITICAL,stdout,stderr,logfile)

def log(code,message,level,stdout=False,stderr=False,logfile=True):
    # check code length
    if len(code)!=12:
        raise SDException("SYNDALOG-002","%s have an incorrect length"%code)

    # retrieve modulecode part of code
    modulecode=code[0:8]

    if level>=get_verbosity_level():
        if stdout:
            sdtools.print_stdout(message)
        if stderr:
            sdtools.print_stderr(message)

    if logfile:
        logger.log(level,message,extra={'code' : code})

def get_verbosity_level():
    label=sdconfig.config.get('log','verbosity_level')
    level=LEVELS[label] # string to int conversion
    return level

def get_verbosity_label(level):
    label=LEVELS[level] # int to string conversion
    return label

def create_logger(name,filename):
    FORMAT = '%(asctime)-15s %(levelname)s %(code)s %(message)s'
    verbosity_level=get_verbosity_level()

    logger = logging.getLogger(name)
    logger.setLevel(verbosity_level)
    fullpath_filename="%s/%s"%(sdconfig.log_folder,filename)
    fh = logging.FileHandler(fullpath_filename)
    fh.setLevel(verbosity_level)
    fh.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(fh)

    return logger

def set_logger(name):
    global logger
    logger=logging.getLogger(name)

# module init.

create_logger(sdconst.LOGGER_FEEDER,sdconst.LOGFILE_FEEDER)
create_logger(sdconst.LOGGER_CONSUMER,sdconst.LOGFILE_CONSUMER)

logger=logging.getLogger(sdconst.LOGGER_FEEDER)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name',required=True,choices=[sdconst.LOGGER_FEEDER,sdconst.LOGGER_CONSUMER])
    args = parser.parse_args()

    set_logger(args.name)

    info('SYNDALOG-001','test1')
