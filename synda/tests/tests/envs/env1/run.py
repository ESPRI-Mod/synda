# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
MAIN run for TEST SUITE
it allows to control the tests sequences from the most required to the most advanced ones
"""
from synda.tests.tests.envs.env1.subcommand.api.esgf_search.run import main as run_env1_esgf_search_api
from synda.tests.tests.envs.env1.subcommand.variable.run import main as run_env1_variable
from synda.tests.tests.envs.env1.subcommand.download.run import main as run_env1_download


def main(coverage_activated=False):

    run_env1_esgf_search_api(coverage_activated=coverage_activated)
    run_env1_variable(coverage_activated=coverage_activated)
    run_env1_download(coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()

