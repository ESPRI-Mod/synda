#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""This module contains code related to logging."""

import sys
import logging
import argparse
import spapp
import spconst
import spconfig
import sptools
from spexception import SPException

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

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

def log(code,message,level,stdout,stderr,logfile):
    # check code length
    if len(code)!=12:
        raise SPException("SYNDALOG-002","%s have an incorrect length"%code)

    # retrieve modulecode part of code
    modulecode=code[0:8]

    if level>=get_verbosity_level():
        if stdout:
            sptools.print_stdout(message)
        if stderr:
            sptools.print_stderr(message)

    if logfile:
        logger.log(level,message,extra={'code' : code})

def get_verbosity_level():
    level=spconfig.config.get('log','verbosity_level')
    return LEVELS[level] # string to int conversion

def create_logger(name,filename):
    FORMAT = '%(asctime)-15s %(levelname)s %(code)s %(message)s'
    verbosity_level=get_verbosity_level()

    logger = logging.getLogger(name)
    logger.setLevel(verbosity_level)
    fullpath_filename="%s/%s"%(spconfig.log_folder,filename)
    fh = logging.FileHandler(fullpath_filename)
    fh.setLevel(verbosity_level)
    fh.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(fh)

    return logger

def set_logger(name):
    global logger
    logger=logging.getLogger(name)

# module init.

os.umask(0002)

create_logger(spconst.LOGGER,spconst.LOGFILE)

logger=logging.getLogger(spconst.LOGGER)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    set_logger(spconst.LOGGER)

    info('SYNDALOG-001','test1')
