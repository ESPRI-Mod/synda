# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 From an existing synda user workspace environment with installed files & datasets,
 create a .tar file that will be located into the tests/data/env/installed/list directory
"""
import os

from synda.tests.process.env.build.installed.list.models import Process


if __name__ == '__main__':
    source = os.environ["ST_HOME"]
    config = Process()
    config.process()

    print("ok")
