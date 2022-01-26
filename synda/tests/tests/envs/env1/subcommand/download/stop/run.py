# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import time
import datetime

from synda.sdt.sdtools import print_stderr

from synda.tests.tests.utils import run_test_under_subprocess
from synda.tests.tests.envs.env1.constants import TESTS_DIR
from synda.tests.manager import Manager
from synda.source.db.task.file.models import get_rows_filtered_on_file_functional_id as get_record
from synda.tests.context.envs.env1.constants import DB as DB_CONTEXT
from synda.tests.context.envs.env1.constants import ENV
from synda.source.constants import is_test_mode_activated

TIMEOUT = 60


def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def get_test_download_start_fullfilename():
    dirname = os.path.join(
        get_subcommand_dirname("download"),
        "stop",
    )

    fullfilename = os.path.join(
        dirname,
        "test_env1_download_start_before_stop.py",
    )

    return fullfilename


def get_test_download_stop_fullfilename():
    dirname = os.path.join(
        get_subcommand_dirname("download"),
        "stop",
    )

    fullfilename = os.path.join(
        dirname,
        "test_env1_download_stop.py",
    )

    return fullfilename


def test_download_stopped_by_user(manager):

    source = ENV["full_filename"]
    manager.create_test_environment(source=source)

    fullfilename = get_test_download_start_fullfilename()

    # STEP 1 : start the asynchronous download process

    run_test_under_subprocess(fullfilename, popen=True)

    # STEP 2 : control that the status of the downloading process is : "active"

    from synda.source.config.file.downloading.models import Config as DownloadingFile

    test_title = "START CONTROL | The Status of the Downloading Process (Active)"

    downloading_file = DownloadingFile()

    end = datetime.datetime.now() + datetime.timedelta(seconds=TIMEOUT)
    while not downloading_file.process_is_active() and end > datetime.datetime.now():
        time.sleep(1)

    if not downloading_file.process_is_active():
        print_stderr(f'{test_title} | FAILED')
        p = downloading_file.get_data()["default"]["path"]
        print_stderr(
            f"START CONTROL | The Downloading Process not active [active expected] ("
            f"see file content : {os.path.join(p, 'downloading.pid')})"
        )
        exit(1)

    assert downloading_file.process_is_active()

    file_functional_id = DB_CONTEXT["files"][0]["functional_id"]
    record = get_record(file_functional_id)

    if record["status"] != "running":
        print_stderr(f'{test_title} | FAILED')
        print_stderr(
            f"START CONTROL | File status is {record['status']} (running expected)",
        )
        exit(1)

    assert record["status"] == "running"

    print(f'{test_title} PASSED [100%]')

    # STEP 3 : stop the download process

    fullfilename = get_test_download_stop_fullfilename()
    run_test_under_subprocess(fullfilename, popen=False)

    # STEP 4 : control that the status of the downloading process is now : "not active"
    test_title = "STOP CONTROL | The Status of the Downloading Process (not Active)"

    if downloading_file.process_is_active():
        print_stderr(f'{test_title} | FAILED')
        p = downloading_file.get_data()["default"]["path"]
        print_stderr(
            f"STOP CONTROL | The Downloading Process is still active [not active expected] ("
            f"see file content : {os.path.join(p, 'downloading.pid')})"
        )
        exit(1)

    # STEP 5 : control of the file record status (waiting)
    test_title = "STOP CONTROL | Download has been stopped by user"

    file_functional_id = DB_CONTEXT["files"][0]["functional_id"]
    record = get_record(file_functional_id)

    if record["sdget_error_msg"] != "Download has been stopped by user":
        print_stderr(f'{test_title} | FAILED')
        print_stderr(
            f"STOP CONTROL | sdget_error_msg : {record['sdget_error_msg']} ['Download has been stopped by user' expected]",
        )
        exit(1)

    print(f'{test_title} PASSED [100%]')

    manager.delete_test_environment()


def main(coverage_activated=False):

    manager = Manager()
    manager.set_tests_mode()
    manager.delete_test_environment()
    assert is_test_mode_activated()
    test_download_stopped_by_user(manager)


if __name__ == '__main__':
    main()

