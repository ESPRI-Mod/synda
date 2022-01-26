# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.asynchronous.download.subcommand.download.manager.models \
    import Manager as AiohttpBatchManager

from synda.source.process.asynchronous.download.subcommand.download.task.provider.models \
    import Provider as TaskProvider
from synda.source.process.asynchronous.download.scheduler.models import main

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.internal.models import Config as Internal

internal = Internal()
preferences = Preferences()

# EMPTY_QUEUE_MESSAGE constant below is used by tests, do not remove

EMPTY_QUEUE_MESSAGE = """
Download queue is empty.
Load the queue with the 'synda install' subcommand and try again : 'synda download start'.
"""


async def scheduler(
        batch_manager=AiohttpBatchManager,
        task_provider=TaskProvider(),
        nb_max_workers=preferences.download_max_parallel_download,
        nb_max_batch_workers=preferences.download_max_parallel_download_per_datanode,
        config=None,
        verbose=False,
        build_report=False,
):

    # nb_max_batch_workers = 1
    # nb_max_workers = 1

    if not config:
        config = dict(
            http_timeout=preferences.download_async_http_timeout,
            streaming_chunk_size=preferences.download_streaming_chunk_size,
            incorrect_checksum_action=preferences.behaviour_incorrect_checksum_action,
            is_download_http_fallback=preferences.is_download_http_fallback,
            logger_consumer=internal.logger_consumer,
            do_post_download_controls=True,
        )
    success = await main(
        batch_manager,
        task_provider,
        config,
        nb_max_workers=nb_max_workers,
        nb_max_batch_workers=nb_max_batch_workers,
        verbose=verbose,
        build_report=build_report,
    )

    return success
