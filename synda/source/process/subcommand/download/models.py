# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio
import threading

# from synda.sdt import sdlog

from synda.source.process.authority.models import Authority
from synda.source.process.subcommand.required.env.models import Process as Base
# from synda.source.process.asynchronous.download.scheduler.models import scheduler

THREAD_NAME = 'download'


class Process(Base):

    def __init__(self, arguments=None, exceptions_codes=None):
        super(Process, self).__init__(
            name="download",
            authority=Authority(),
            arguments=arguments,
            exceptions_codes=exceptions_codes,
        )
    #     self.loop = None
    #     self.thread = None
    #     self.stop_event = None
    #
    #     self.loop = asyncio.get_event_loop()
    #     self.stop_event = threading.Event()
    #
    # def enabled(self):
    #     return self.is_thread_alive()
    #
    # def disabled(self):
    #     return not self.is_thread_alive()
    #
    # def print_state(self):
    #     enable = True
    #     if self.enable():
    #         msg = "Download enabled"
    #     else:
    #         msg = "Download disabled"
    #     print(msg)
    #
    # def disable(self):
    #     print(
    #         "Thread 'download' is alive ? {}".format(
    #             self.is_thread_alive(),
    #         ),
    #     )
    #     self.stop_event.set()
    #     # sdlog.info('SDDOWNLD-001', "Download state : disabled")
    #
    # def to_thread(self):
    #     asyncio.set_event_loop(self.loop)
    #     self.loop.run_until_complete(
    #         scheduler(verbose=True, build_report=False, stop_event=self.stop_event),
    #     )
    #
    # def is_thread_alive(self):
    #     return threading.Thread(name=THREAD_NAME).is_alive()
    #
    # def start_thread(self):
    #     self.thread.start()
    #     print(
    #         "Thread 'download' is alive ? {}".format(
    #             self.is_thread_alive(),
    #         ),
    #     )
    #
    # def enable(self):
    #     self.thread = threading.Thread(target=self.to_thread, name=THREAD_NAME)
    #     self.thread.setDaemon(True)
    #     self.start_thread()
    #     # sdlog.info('SDDOWNLD-001', "Download state : enabled")
    #     self.thread.join()
    #     print("Thread : '{}' successed".format(THREAD_NAME))
