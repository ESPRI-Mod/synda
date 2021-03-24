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
from synda.tests.manager import Manager

from synda.source.process.subcommand.manager import Manager as SubCommandManager


def main():

    config = SubCommandManager(["synda", "daemon", 'start']).get_config_manager()
    from synda.sdt import sdtaskscheduler
    # sdtaskscheduler.event_loop(config)
    sdtaskscheduler.run_soft_tasks()


if __name__ == '__main__':

    main()
