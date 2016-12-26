#!/usr/bin/env python
import logging, logging.handlers, struct, json

class MsgpackHandler(logging.handlers.SocketHandler):
  def __init__(self, host, port):
    logging.handlers.SocketHandler.__init__(self,host,port)
  def makePickle(self,record):
    s=json.dumps(record.__dict__)
    slen = struct.pack(">L", len(s))
    return slen + s

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
socketHandler = MsgpackHandler('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')
