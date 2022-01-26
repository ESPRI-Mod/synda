# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio
import os
from signal import SIGTERM

from synda.sdt import sdlog
from synda.sdt import sdexception
from synda.sdt.sdtools import print_stderr

from synda.source.process.subcommand.required.env.models import Process as Base
from synda.source.config.file.downloading.models import Config as File

PIDFILE = File().default
TIMEOUT = 60


def process_action(pid, signal=0):
    """Send a signal to a process.
    :Returns:
    ----------
    True if the pid is dead
    with no signal argument, sends no signal.
    """
    # if 'ps --no-headers' returns no lines, the pid is dead
    from os import kill
    try:
        return kill(pid, signal)
    except OSError as e:
        # process is dead
        if e.errno == 3:
            return True
        # no permissions
        elif e.errno == 1:
            return False
        else:
            raise e


def process_kill_action(pid):
    return process_action(pid, signal=SIGTERM)


def process_info_action(pid):
    return process_action(pid, signal=0)


def is_process_killed(pid):
    return process_info_action(pid)


def kill(pid, interval=1, timeout=TIMEOUT):
    """Let process die gracefully.
    Gradually send harsher signals
    if necessary.
    :Returns:
    ---------
    True if the process was killed and exited cleanly.
    False if the process kill hung up and couldn't be cleaned.
    """

    from time import sleep
    i = 0
    killed = process_kill_action(pid)

    while not killed and i < timeout:
        sleep(interval)
        killed = is_process_killed(pid)
        i += 1
    if not killed:
        print(f"Unexpected problem occured. Donwloading process (pid : {pid}) has to be killed manually by user ")


class Process(Base):

    def __init__(self, payload, arguments=None, exceptions_codes=None):
        super(Process, self).__init__(
            "download",
            payload,
            arguments=arguments,
            exceptions_codes=exceptions_codes,
        )
        self.messages = dict(
            start=dict(
                error="Downloading is already active",
                warning="",
            ),
            stop=dict(
                info="Downloading process successfully stopped",
                warning="Downloading process already inactive",
            )
        )
        self.pid_file = File()

    def create_downloading_file(self):
        # First, we create a file that contains the pid of the current process
        # The existence of this particular file is the proof that a downloading process is in progress
        self.pid_file.set_content(f"{os.getpid()}")

    def delete_downloading_file(self):
        error = self.pid_file.delete()

    def set_is_done(self):
        # Third, remove of the pid file because of the end of the downloading process
        self.delete_downloading_file()

    @property
    def status(self):
        return "running" if self.pid_file.process_is_active() else "not running"

    def print_status(self):
        print(f"Downloading process is {self.status}")

    def print_stderr(self, action):
        level = "error"
        print(self.messages[action][level])

    def stop(self):
        pid = self.pid_file.get_pid()
        if pid:
            kill(pid)
        else:
            sdlog.error(
                'DL-STOP-ERR1',
                "Warning: pid file exists but downloading process doesn't exist. "
                "Most often, this is caused by an unexpected system restart (e.g. kernel panic).",
            )

            # remove orphan pidfile
            sdlog.info(
                'DL-STOP-ERR1',
                f"Removing orphan downloading pid file ({self.pid_file.default}).",
            )
            self.delete_downloading_file()

    def start(self):
        print_stderr(
            "You can follow the download using 'synda download watch' and 'synda download queue' commands",
        )
        from synda.source.process.asynchronous.download.subcommand.download.scheduler.models import scheduler
        self.create_downloading_file()
        # Run the downloading process
        asyncio.run(scheduler(verbose=False, build_report=False))
        self.delete_downloading_file()

    def queue(self, args):
        from synda.sdt import sdfilequery
        from tabulate import tabulate
        from synda.sdt.sdprogress import ProgressThread

        # spinner start
        ProgressThread.start(
            sleep=0.1,
            running_message='Collecting status information.. ',
            end_message='',
        )
        li = sdfilequery.get_download_status(args.project)
        # spinner stop
        ProgressThread.stop()
        print(tabulate(li, headers=['status', 'count', 'size'], tablefmt="plain"))

    def watch(self, args):
        from synda.sdt import sdreport
        sdreport.print_running_transfers()

    def run(self, args):
        action = args.action
        if action == "start" or action == "restart":
            if self.pid_file.process_is_active():
                # Process is already in progress
                self.print_stderr(action)
            else:
                self.start()
        elif action == "stop":
            if self.pid_file.process_is_active():
                try:
                    self.stop()
                    print(self.messages["stop"]["info"])
                except sdexception.SDException as e:
                    print_stderr(
                        f'error occured : {e.msg}',
                    )
            else:
                print(self.messages["stop"]["warning"])
        elif action == "queue":
            self.queue(args)
        elif action == "watch":
            self.watch(args)
        elif action == "status":
            self.print_status()
        else:
            print_stderr(
                f'error occured, unknown action for download subcommand : {action}',
            )
