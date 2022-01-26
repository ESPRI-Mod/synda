# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio
import uvloop

uvloop.install()


async def default_post_process(task):
    task.set_status("done")
    success = True
    return success


class Process(object):
    def __init__(self, task):
        self.task = task

    async def execute(self):
        await asyncio.sleep(10)
