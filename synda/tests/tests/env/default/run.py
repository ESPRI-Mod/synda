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
from synda.tests.tests.env.default.synchronous.run import main as run_synchronous_tests
from synda.tests.tests.env.default.subprocess.run import main as run_subprocess_tests


def main(coverage_activated=False):

    run_synchronous_tests(coverage_activated=coverage_activated)
    run_subprocess_tests(coverage_activated=coverage_activated)


if __name__ == '__main__':
    main()

