#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
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
    level=sdconfig.config.get('log','verbosity_level')
    return LEVELS[level] # string to int conversion

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


##!/usr/bin/env python
#import json
#import logging
#import logging.handlers
#import SocketServer
#import struct
#
#
#class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
#    """Handler for a streaming logging request.
#
#    This basically logs the record using whatever logging policy is
#    configured locally.
#    """
#
#    def handle(self):
#        """
#        Handle multiple requests - each expected to be a 4-byte length,
#        followed by the LogRecord in pickle format. Logs the record
#        according to whatever policy is configured locally.
#        """
#        while True:
#            chunk = self.connection.recv(4)
#            if len(chunk) < 4:
#                break
#            slen = struct.unpack('>L', chunk)[0]
#            chunk = self.connection.recv(slen)
#            while len(chunk) < slen:
#                chunk = chunk + self.connection.recv(slen - len(chunk))
#            obj = self.unPickle(chunk)
#            record = logging.makeLogRecord(obj)
#            self.handleLogRecord(record)
#
#    def unPickle(self, data):
#        return json.loads(data)
#
#    def handleLogRecord(self, record):
#        # if a name is specified, we use the named logger rather than the one
#        # implied by the record.
#        if self.server.logname is not None:
#            name = self.server.logname
#        else:
#            name = record.name
#        logger = logging.getLogger(name)
#        # N.B. EVERY record gets logged. This is because Logger.handle
#        # is normally called AFTER logger-level filtering. If you want
#        # to do filtering, do it at the client end to save wasting
#        # cycles and network bandwidth!
#        logger.handle(record)
#
#class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
#    """
#    Simple TCP socket-based logging receiver suitable for testing.
#    """
#
#    allow_reuse_address = 1
#
#    def __init__(self, host='localhost',
#                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
#                 handler=LogRecordStreamHandler):
#        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
#        self.abort = 0
#        self.timeout = 1
#        self.logname = None
#
#    def serve_until_stopped(self):
#        import select
#        abort = 0
#        while not abort:
#            rd, wr, ex = select.select([self.socket.fileno()],
#                                       [], [],
#                                       self.timeout)
#            if rd:
#                self.handle_request()
#            abort = self.abort
#
#def main():
#    logging.basicConfig(
#        format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')
#    tcpserver = LogRecordSocketReceiver()
#    print('About to start TCP server...')
#    tcpserver.serve_until_stopped()
#
#if __name__ == '__main__':
#    main()

##!/usr/bin/env python
#import logging, logging.handlers, struct, json
#
#class MsgpackHandler(logging.handlers.SocketHandler):
#  def __init__(self, host, port):
#    logging.handlers.SocketHandler.__init__(self,host,port)
#  def makePickle(self,record):
#    s=json.dumps(record.__dict__)
#    slen = struct.pack(">L", len(s))
#    return slen + s
#
#rootLogger = logging.getLogger('')
#rootLogger.setLevel(logging.DEBUG)
#socketHandler = MsgpackHandler('localhost',
#                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
## don't bother with a formatter, since a socket handler sends the event as
## an unformatted pickle
#rootLogger.addHandler(socketHandler)
#
## Now, we can log to the root logger, or any other logger. First the root...
#logging.info('Jackdaws love my big sphinx of quartz.')
#
## Now, define a couple of other loggers which might represent areas in your
## application:
#
#logger1 = logging.getLogger('myapp.area1')
#logger2 = logging.getLogger('myapp.area2')
#
#logger1.debug('Quick zephyrs blow, vexing daft Jim.')
#logger1.info('How quickly daft jumping zebras vex.')
#logger2.warning('Jail zesty vixen who grabbed pay from quack.')
#logger2.error('The five boxing wizards jump quickly.')
#"""
