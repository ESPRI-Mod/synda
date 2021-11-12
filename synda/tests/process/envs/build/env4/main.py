# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 Create a workspace (i.e. a .tar file) with no installed data
 it will be located into the tests/data/envs/env4 directory
 it is used for testing the following subcommands:
    - download (checkenv)

"""
from synda.tests.process.envs.build.env4.models import Process


if __name__ == '__main__':
    config = Process()
    config.process()
