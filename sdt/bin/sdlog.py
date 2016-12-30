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
import os
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

def debug(code,message,stdout=False,stderr=False,logfile=True,logger_name=None):
    log(code,message,logging.DEBUG,stdout,stderr,logfile,logger_name)
def info(code,message,stdout=False,stderr=False,logfile=True,logger_name=None):
    log(code,message,logging.INFO,stdout,stderr,logfile,logger_name)
def warning(code,message,stdout=False,stderr=False,logfile=True,logger_name=None):
    log(code,message,logging.WARNING,stdout,stderr,logfile,logger_name)
def error(code,message,stdout=False,stderr=False,logfile=True,logger_name=None):
    log(code,message,logging.ERROR,stdout,stderr,logfile,logger_name)
def critical(code,message,stdout=False,stderr=False,logfile=True,logger_name=None):
    log(code,message,logging.CRITICAL,stdout,stderr,logfile,logger_name)

def log(code,message,level,stdout=False,stderr=False,logfile=True,logger_name=None):
    # check code length
    if len(code)!=12:
        raise SDException("SYNDALOG-002","%s have an incorrect length"%code)

    # retrieve modulecode part of code
    modulecode=code[0:8]

    if level>=get_verbosity_level():

        if stdout:
            sdtools.print_stdout(message)

        if stderr:

            # add msg prefix
            label=get_verbosity_label(level)
            formatted_msg='%s: %s'%(label.upper(),message)

            sdtools.print_stderr(formatted_msg)

    if logfile:
        if logger_name is None:
            # default logger

            default_logger.log(level,message,extra={'code' : code})
        else:
            if logger_name==sdconst.LOGGER_DOMAIN:
                domain_logger.log(level,message,extra={'code' : code})
            else:
                assert False

def get_verbosity_level():
    label=sdconfig.config.get('log','verbosity_level')
    level=LEVELS[label] # string to int conversion
    return level

def get_verbosity_label(level):
    label=LABELS[level] # int to string conversion
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

def set_default_logger(name):
    global default_logger
    default_logger=logging.getLogger(name)

# module init.

os.umask(0002)

discovery_logger=create_logger(sdconst.LOGGER_FEEDER,sdconst.LOGFILE_FEEDER)
transfer_logger=create_logger(sdconst.LOGGER_CONSUMER,sdconst.LOGFILE_CONSUMER)
domain_logger=create_logger(sdconst.LOGGER_DOMAIN,sdconst.LOGFILE_DOMAIN)

default_logger=discovery_logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name',required=True,choices=[sdconst.LOGGER_FEEDER,sdconst.LOGGER_CONSUMER])
    args = parser.parse_args()

    set_default_logger(args.name)

    info('SYNDALOG-001','test1')
