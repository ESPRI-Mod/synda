# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 Create a workspace (i.e. a .tar file) with no data and no credentials
 It will be located into the tests/data/envs/no_credentials directory
"""
import os

from synda.tests.process.envs.build.env0.models import Process


if __name__ == '__main__':
    source = os.environ["ST_HOME"]
    config = Process()
    config.process()

    print("new environment created")
