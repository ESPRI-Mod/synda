# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 Create a workspace (i.e. a .tar file) with already installed data
 it will be located into the tests/data/envs/env1 directory
 it is used for testing the following subcommands:
    - download (start/stop/queue/status/watch)

"""
import os

from synda.tests.process.envs.build.env1.models import Process


if __name__ == '__main__':
    source = os.environ["ST_HOME"]
    config = Process()
    config.process()
