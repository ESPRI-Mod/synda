# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import logging
from logging import FileHandler
from logging import Formatter

LOG_FORMAT = '%(asctime)s, %(levelname)s %(message)s'
LOG_LEVEL = logging.INFO


def get_default_logger(name="default_logger", filename="default_logger.log"):

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger_file_handler = FileHandler(filename)
    logger_file_handler.setLevel(LOG_LEVEL)
    logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
    logger.addHandler(logger_file_handler)

    return logger

class Logger(object):

    def __init__(self):
        super(Authority, self).__init__()

    def is_authorized(self):
        raise MethodNotImplemented("is_authorized", self.__class__)


