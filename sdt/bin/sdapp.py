#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains application initialization code.

Note
    This module must be imported in every other scripts (daemon included)
"""

import os
import atexit
import sdapputils
import sdconfig
import sdtools
import sdtransientdbfilecleanup

def cleanup():
    if sdconfig.prevent_daemon_and_ihm or sdconfig.prevent_ihm_and_ihm:
        if os.path.isfile(sdconfig.ihm_pid_file):
            os.unlink(sdconfig.ihm_pid_file)

    # hack
    #
    # Something is hidding the cursor in 'synda' command, but I don't know what
    # exactly. Code below is a quickfix used to turn on the cursor.
    #
    if sdconfig.config.getboolean('interface','progress'):
        sdtools.set_terminal_cursor_visible()

# Init.

os.umask(0002)

name='transfer'
version='3.9'
sdapputils.set_exception_handler()

# maybe remove the two mkdir below as it is a bit overkill
# (those 2 paths are already created by installation script ("install.sh"))
if not os.path.exists(sdconfig.log_folder):
    os.makedirs(sdconfig.log_folder)
if not os.path.exists(sdconfig.tmp_folder):
    os.makedirs(sdconfig.tmp_folder)

if sdtools.who_am_i()=='ihm':
    sdtransientdbfilecleanup.run()

    if sdconfig.prevent_daemon_and_ihm:
        sdapputils.singleton_check(sdconfig.daemon_pid_file)
    if sdconfig.prevent_ihm_and_ihm:
        sdapputils.singleton_check(sdconfig.ihm_pid_file)

    if sdconfig.prevent_daemon_and_ihm or sdconfig.prevent_ihm_and_ihm:
        sdapputils.create_IHM_pid_file(sdconfig.ihm_pid_file)

    # configure non-daemon start/stop routines 
    # (daemon start/stop routines are configured directly in sdtaskscheduler module)
    atexit.register(cleanup) # in case of unexpected exit (e.g. exception)
    sdapputils.signal_init()

if __name__ == '__main__':
    print "Synda transfer initialization module."
