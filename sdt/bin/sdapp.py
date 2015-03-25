#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdapp.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains application initialization code.

Note
    This module must be imported in every other script (daemon included)
"""

import os
import sys
import atexit
import sdapputils
import sdconfig
import sdtools

def cleanup():
    if os.path.isfile(sdconfig.ihm_pid_file):
        os.unlink(sdconfig.ihm_pid_file)

    # HACK
    #
    # Something is hidding the cursor in 'synda' command, but I don't know what
    # exactly. Code below is a hack/quickfix used to turn on the cursor.
    #
    if sdconfig.config.getboolean('interface','progress'):
        sdtools.set_terminal_cursor_visible()

def is_daemon():

    # the parent of a daemon is always Init, so check for ppid 1 
    if os.getppid() == 1:

        # note that in some case, some non-daemon also have init as parent
        # so we double check with controlling tty (i.e. daemon have no controlling tty)
        if not os.isatty(sys.stdout.fileno()):
            return True
        else:
            return False

    else:
        return False

def who_am_i():
    """This func line checks if we are IHM or daemon.

    Note
        There are many different IHM commands, but only one daemon command
    """

    if not is_daemon():
        return 'ihm'
    else:
        return 'daemon'

# Init.

name='transfer'
version='3.0'
sdapputils.set_exception_handler()

# maybe remove the two mkdir below as it is a bit overkill
# (those 2 paths are already created by installation script ("install.sh"))
if not os.path.exists(sdconfig.log_folder):
    os.mkdirs(sdconfig.log_folder)
if not os.path.exists(sdconfig.tmp_folder):
    os.mkdirs(sdconfig.tmp_folder)

if who_am_i()=='ihm':

    if sdconfig.prevent_daemon_and_ihm:
        sdapputils.singleton_check(sdconfig.daemon_pid_file)
    if sdconfig.prevent_ihm_and_ihm:
        sdapputils.singleton_check(sdconfig.ihm_pid_file)

    sdapputils.create_IHM_pid_file(sdconfig.ihm_pid_file)

    # configure non-daemon start/stop routines 
    # (daemon start/stop routines are configured directly in sdtaskscheduler module)
    atexit.register(cleanup) # in case of unexpected exit (e.g. exception)
    sdapputils.signal_init()

if __name__ == '__main__':
    print "Synchro-data initialization module."
