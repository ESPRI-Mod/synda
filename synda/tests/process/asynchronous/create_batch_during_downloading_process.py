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
from synda.source.process.asynchronous.scheduler.models import scheduler
from synda.source.process.asynchronous.task.provider.models \
    import CreateBatch as TaskProvider


if __name__ == '__main__':
    asyncio.run(
        scheduler(
            nb_max_workers=4,
            nb_max_batch_workers=2,
            task_provider_class=TaskProvider,
            verbose=True,
            build_report=False,
        ),
    )
