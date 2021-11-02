#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains code related to logging."""
import os
import logging
import argparse

from synda.sdt import sdtools
from synda.sdt.sdexception import SDException

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.path.tree.models import Config as TreePath
from synda.source.config.file.internal.models import Config as Internal
internal = Internal()


FORMAT = '%(asctime)-15s %(levelname)s %(code)s %(message)s'

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


def debug(code, message, stdout=False, stderr=False, logfile=True, logger_name=None):
    log(code, message, logging.DEBUG, stdout, stderr, logfile, logger_name)


def info(code, message, stdout=False, stderr=False, logfile=True, logger_name=None):
    log(code, message, logging.INFO, stdout, stderr, logfile, logger_name)


def warning(code, message, stdout=False, stderr=False, logfile=True, logger_name=None):
    log(code, message, logging.WARNING, stdout, stderr, logfile, logger_name)


def error(code, message, stdout=False, stderr=False, logfile=True, logger_name=None):
    log(code, message, logging.ERROR, stdout, stderr, logfile, logger_name)


def critical(code, message, stdout=False, stderr=False, logfile=True, logger_name=None):
    log(code, message, logging.CRITICAL, stdout, stderr, logfile, logger_name)


def log(code, message, level, stdout=False, stderr=False, logfile=True, logger_name=None):
    # check code length
    if len(code) != 12:
        raise SDException("SYNDALOG-002", "%s have an incorrect length" % code)

    if level >= get_verbosity_level():

        if stdout:
            sdtools.print_stdout(message)

        if stderr:

            # add msg prefix
            label = get_verbosity_label(level)
            formatted_msg = '%s: %s' % (label.upper(), message)

            sdtools.print_stderr(formatted_msg)

    if logfile:
        if logger_name is None:
            # default logger
            default_logger.log(level, message, extra={'code': code})
        else:
            if logger_name == internal.logger_domain:
                domain_logger.log(level, message, extra={'code': code})
            elif logger_name == internal.logger_consumer:
                transfer_logger.log(level, message, extra={'code': code})
            else:
                assert False


def get_verbosity_level():

    label = Preferences().log_verbosity_level
    # string to int conversion
    level = LEVELS[label]
    return level


def get_verbosity_label(level):
    # int to string conversion
    label = LABELS[level]
    return label


def create_logger(name, filename):
    verbosity_level = get_verbosity_level()

    logger = logging.getLogger(name)
    logger.setLevel(verbosity_level)

    fullpath_filename = os.path.join(
        TreePath().get("log"),
        filename,
    )

    fh = logging.FileHandler(fullpath_filename)
    fh.setLevel(verbosity_level)
    fh.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(fh)

    return logger


def remove_handler(logger):
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)


def set_default_logger(name):
    global default_logger
    default_logger = logging.getLogger(name)

# module init.


os.umask(0o0002)

discovery_logger = create_logger(internal.logger_feeder, internal.logger_feeder_file)
transfer_logger = create_logger(internal.logger_consumer, internal.logger_consumer_file)
domain_logger = create_logger(internal.logger_domain, internal.logger_domain_file)

default_logger = discovery_logger

# default_logger_file_name = default_logger.handlers[0].baseFilename

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--name', default=internal.logger_feeder)
    args = parser.parse_args()

    set_default_logger(args.name)

    info('SYNDALOG-001', 'test {}'.format(internal.logger_feeder))

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--name', default=internal.logger_consumer)
    args = parser.parse_args()

    set_default_logger(args.name)

    info('SYNDALOG-001', 'test {}'.format(internal.logger_consumer))
