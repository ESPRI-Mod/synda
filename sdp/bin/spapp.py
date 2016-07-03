#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""This module contains application initialization code.

Note
    This module must be imported in every other script (daemon included)
"""

import os
import sys
import atexit
import spapputils
import spconfig

def cleanup():
    if os.path.isfile(spconfig.ihm_pid_file):
        os.unlink(spconfig.ihm_pid_file)

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

name='postprocessing'
version='1.0'
spapputils.set_exception_handler()

if who_am_i()=='ihm':

    if spconfig.prevent_daemon_and_ihm:
        spapputils.singleton_check(spconfig.daemon_pid_file)
    if spconfig.prevent_ihm_and_ihm:
        spapputils.singleton_check(spconfig.ihm_pid_file)

    spapputils.create_IHM_pid_file(spconfig.ihm_pid_file)

    # configure non-daemon start/stop routines 
    # (daemon start/stop routines are configured directly in sptaskscheduler module)
    atexit.register(cleanup) # in case of unexpected exit (e.g. exception)
    spapputils.signal_init()

if __name__ == '__main__':
    print "sdp initialization module."
