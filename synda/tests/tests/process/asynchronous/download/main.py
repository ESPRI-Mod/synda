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
from synda.source.process.asynchronous.download.scheduler.models import scheduler
from synda.source.process.asynchronous.download.manager.batch.http.aio.models import Manager as AiohttpBatchManager
from synda.source.process.asynchronous.download.manager.batch.http.x.models import Manager as HttpxBatchManager
from synda.source.process.asynchronous.download.manager.batch.http.blocking.myrequests.models import Manager as HttpBlockingBatchManager
from synda.source.process.asynchronous.download.manager.batch.http.blocking.mywget.models import Manager as WgetBatchManager
from synda.source.process.asynchronous.download.manager.batch.http.blocking.mywget2.models import Manager as Wget2BatchManager


if __name__ == '__main__':

    # batch_manager = AiohttpBatchManager
    # batch_manager = HttpxBatchManager
    # batch_manager = HttpBlockingBatchManager
    # batch_manager = WgetBatchManager
    batch_manager = Wget2BatchManager

    asyncio.run(
        scheduler(batch_manager, verbose=True, build_report=False),
    )
