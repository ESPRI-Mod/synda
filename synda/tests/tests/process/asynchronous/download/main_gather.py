# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""

"""
import asyncio
from synda.source.process.asynchronous.download.scheduler.models import scheduler3
from synda.source.process.asynchronous.download.manager.batch.http.aio.models import Manager as AiohttpBatchManager


if __name__ == '__main__':

    batch_manager = AiohttpBatchManager

    asyncio.run(scheduler3(batch_manager, verbose=True, build_report=False))
