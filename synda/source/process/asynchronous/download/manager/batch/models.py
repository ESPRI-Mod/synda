# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import aiohttp

from synda.source.process.asynchronous.manager.batch.models import Manager as Base
from synda.source.process.asynchronous.download.worker.models import Worker

from synda.source.config.file.user.preferences.models import Config as Preferences

preferences = Preferences()


class Manager(Base):

    def __init__(self, scheduler, worker_cls=Worker, max_workers=1, name="", verbose=False):
        Base.__init__(self, scheduler, worker_cls=worker_cls, max_workers=max_workers, name=name, verbose=verbose)

        # initializations
        self.http_client_session = None

        # settings
        self.http_client_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=preferences.download_async_http_timeout),
        )

    def get_http_client_session(self):
        return self.http_client_session

    async def clean(self):
        await self.http_client_session.close()
