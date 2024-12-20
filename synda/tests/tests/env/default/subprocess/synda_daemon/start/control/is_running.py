# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

def test_main():

    print("Control that the status of the daemon is : 'running'...")
    from synda.tests.manager import Manager
    Manager().set_tests_mode()
    from synda.sdt import sddaemon

    assert sddaemon.is_running()


def main():

    print("Control that the status of the daemon is : 'running'...")
    from synda.tests.manager import Manager
    Manager().set_tests_mode()
    from synda.sdt import sddaemon

    assert sddaemon.is_running()


if __name__ == '__main__':
    main()
