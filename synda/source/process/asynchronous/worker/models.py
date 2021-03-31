# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio
# for generation of uml documentation
# from synda.source.process.asynchronous.manager.batch.models import Manager as BatchManager


class Worker(object):

    def __init__(self, name, queue, manager):

        # initializations
        self.queue = asyncio.Queue()
        self.name = ""
        self.manager = None
        # for generation of uml documentation
        # self.manager = BatchManager([])

        # settings
        self.queue = queue
        self.name = name
        self.manager = manager

    async def process_task(self, start_delay):
        await asyncio.sleep(start_delay)
        while self.manager.has_pending_tasks():
            if self.queue.empty():
                pending_task = await self.manager.put_new_task(self.queue)
                if not pending_task:
                    # at the moment, tasks manager refuses to deliver a new pending task
                    # probably reason :
                    #      1 / the maximum pool of workers for the current batch has been reached,
                    #      2 / the maximum pool of workers for all running batches has been reached
                    # => worker has to wait , why not 1 second, before a new attempt
                    print("no pending task = > worker is waiting")
                    await asyncio.sleep(1)
            else:
                # get a task out of the queue
                task = await self.queue.get()
                # process it
                await task.process()
                # marked it as done
                self.queue.task_done()
        return True
