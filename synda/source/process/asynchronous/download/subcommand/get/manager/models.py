# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.asynchronous.download.manager.models import Manager as Base
from synda.source.process.asynchronous.download.subcommand.get.worker.models import Worker


class Manager(Base):

    def __init__(self, scheduler, max_workers=1, name="", verbose=False):
        Base.__init__(self, scheduler, worker_cls=Worker, max_workers=max_workers, name=name, verbose=verbose)
