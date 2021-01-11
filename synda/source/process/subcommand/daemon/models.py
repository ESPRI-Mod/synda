# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.process.authority.models import Authority
from synda.source.process.subcommand.required.env.models import Process as Base

from synda.source.config.file.daemon.models import Config as File


def is_running():
    # maybe this can be replaced by "pidfile.is_locked()"
    if os.path.isfile(File().default):
        return True
    else:
        return False


class Process(Base):

    def __init__(self):
        super(Process, self).__init__(name="daemon", authority=Authority())
