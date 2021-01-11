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
from synda.tests.tests.env.default.init.run import main as run_init_env_tests
from synda.tests.tests.env.default.run import main as run_default_env_tests
from synda.tests.tests.env.installed.run import main as run_installed_env_tests


def main(coverage_activated=False):

    run_init_env_tests()
    run_installed_env_tests(coverage_activated=coverage_activated)
    run_default_env_tests(coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()

