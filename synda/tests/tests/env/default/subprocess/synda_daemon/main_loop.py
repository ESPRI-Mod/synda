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
from synda.source.process.subcommand.manager import Manager

from synda.sdt import sddaemon


def test_main_loop():
    manager = Manager(["synda", "daemon", 'start'])
    manager.validate_env()
    config = manager.get_config_manager()
    sddaemon.start(config)


if __name__ == '__main__':

    test_main_loop()
