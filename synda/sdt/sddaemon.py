# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains daemon related operations.

Usage
    pip install python-daemon # note that this will also install 'lockfile' dependency

Note
    This module don't import sdapp on purpose (it will be done after the
    'double-fork'). If we do import it and it's loaded before the
    double-fork, then who_am_i() doesn't work anymore. i.e. sdapp module init
    code doesn't get executed twice. TAGJL54JJJ3JK22LLL.
"""
import os
import grp
import pwd
import psutil
import signal

from synda.sdt import sdtools
from synda.sdt.sdexception import SDException

from synda.source.config.process.synda_daemon.constants import daemon_context, pidfile
from synda.source.config.file.daemon.models import Config as File

FULLFILENAME = File().default


def get_daemon_status():
    if is_running():
        return "Daemon running"
    else:
        return "Daemon not running"


def print_daemon_status():
    print(get_daemon_status())


def is_running():
    # maybe this can be replaced by "pidfile.is_locked()"
    if os.path.isfile(FULLFILENAME):
        return True
    else:
        return False


def main_loop(config_manager):
    # must be here because of double-fork
    from synda.sdt import sdlog, sdtaskscheduler

    preferences = config_manager.get_user_preferences()

    sdlog.info('SDDAEMON-001', "Daemon starting ...")

    try:
        sdtaskscheduler.event_loop(config_manager)

    except SDException as e:

        level = preferences.log_verbosity_level

        if level == 'debug':
            # We log everything in debug mode no matter the exception type

            sdlog.debug('SDDAEMON-008', "Exception occured (%s)" % str(e))

        else:
            if isinstance(e, SDException):
                # In this case, we only print the exception code, as the errmsg
                # is likely to be there already (i.e. low-level func should have
                # log information about this exception).
                # The primary reason for this is to have a clear log entry
                # when authentication failed (e.g. ESGF is down or openid is incorrect)

                sdlog.info('SDDAEMON-010', "Exception occured (%s)" % str(e.code))
            else:
                # This case should not occur, so we log everything to help debugging

                sdlog.info('SDDAEMON-012', "Exception occured (%s)" % str(e))

    sdlog.info('SDDAEMON-034', "Daemon stopped")


def start(config_manager):

    # run daemon as unprivileged user (if run as root and unprivileged user set in configuration file)
    if sdtools.is_root():

        preferences = config_manager.get_user_preferences()
        user = preferences.daemon_user
        group = preferences.daemon_group

        if user and group:
            unprivileged_user_mode()

    if not is_running():
        try:
            print(
                'Handing over to daemon process, you can check the daemons logs at {}.'.format(
                    daemon_context.stdout.name,
                ),
            )
            with daemon_context:
                main_loop(config_manager)

        except Exception as e:
            from synda.sdt import sdtrace
            sdtrace.log_exception()

        # DOESN'T WORK !
        #
        # BEWARE: tricky code here !!!
        # The idea is after waiting for a while, if daemon startup failed,
        # daemon pid file has been removed by the 'python-daemon' mecanism,
        # thus is_running() should return False in this case.
        #
        """
        time.sleep(5)
        if not is_running():
            print('Error occurs during daemon startup.')
        """
    else:
        print('Daemon is already running.')
        print('PID file location: {}'.format(FULLFILENAME))


def stop():
    if is_running():

        pid = pidfile.read_pid()

        if psutil.pid_exists(pid):
            os.kill(pid, signal.SIGTERM)
        else:
            # sdlog import must not be at the top of this file, because of double-fork
            from synda.sdt import sdlog

            sdlog.error(
                'SDDAEMON-014',
                "Warning: daemon pidfile exists but daemon process doesn't exist. "
                "Most often, this is caused by an unexpected system restart (e.g. kernel panic).",
            )

            # remove orphan pidfile
            sdlog.info(
                'SDDAEMON-016',
                "Removing orphan daemon pidfile (%s)." % FULLFILENAME,
            )

        os.unlink(FULLFILENAME)

    else:
        sdtools.print_stderr('Daemon is already stopped.')


def terminate(signum, frame):
    # must be here because of double-fork (i.e. we can't move import at the top of this file,
    # because the first import must occur in 'main_loop' func).

    from synda.sdt import sdtaskscheduler
    sdtaskscheduler.terminate(signum, frame)


def unprivileged_user_mode(user, group):
    # retrieve numeric uid/gid
    uid = pwd.getpwnam(user).pw_uid
    gid = grp.getgrnam(group).gr_gid

    # be sure file permission works for unprivileged user
    #
    # shouldn't be needed anymore as this is now handled externaly
    # (after installation, all synda files are group-writable and belongs to
    # the synda group).
    #
    # sdfilepermission.run(uid,gid)

    # set_daemon process identity
    daemon_context.uid = uid
    daemon_context.gid = gid

    # enable support for supplementary group
    # (used for unprivileged mode)
    #
    # Depends on Python 2.7+ and python-daemon 2.1.1+
    #
    # Note that 'python-daemon 2.1.1' is not the version installed by default by
    # the synda installer, so to enable 'supplementary group' support, you need
    # to run the following command:
    #
    # <virtualenv_path>/pip install python-daemon==2.1.1
    #
    # Also note that Python must be 2.7+, i.e. it will not work with 2.6 as
    # 'python-daemon 2.1.1' itself depends on 2.7+.
    #
    # TODO: modify synda installer (package and install.sh) so to set the right
    #       python-daemon version automatically.
    #
    if hasattr(daemon_context, 'initgroups'):
        daemon_context.initgroups = True

# init.


os.umask(0o0002)


if __name__ == "__main__":
    pass
