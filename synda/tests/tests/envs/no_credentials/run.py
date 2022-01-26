# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.tests.envs.no_credentials.subcommand.get.run import main as run_no_credentials_get

def main(coverage_activated=False):
    run_no_credentials_get(coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()

