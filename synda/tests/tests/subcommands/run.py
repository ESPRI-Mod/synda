# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.tests.subcommands.synchronous.run import main as run_synchronous_tests
from synda.tests.tests.subcommands.asynchronous.run import main as run_asynchronous_tests


def main():

    run_asynchronous_tests()
    run_synchronous_tests()


if __name__ == '__main__':
    main()

