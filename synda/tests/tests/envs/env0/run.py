# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.tests.envs.env0.subcommand.download.run import main as run_env0_download
from synda.tests.tests.envs.env0.subcommand.version.run import main as run_env0_version
from synda.tests.tests.envs.env0.subcommand.get.run import main as run_env0_get

def main(coverage_activated=False):

    run_env0_download(coverage_activated=coverage_activated)
    run_env0_version(coverage_activated=coverage_activated)
    run_env0_get(coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()

