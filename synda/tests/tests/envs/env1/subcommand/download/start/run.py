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

from synda.sdt.sdtools import print_stderr

from synda.tests.tests.utils import run_test_under_subprocess
from synda.tests.tests.envs.env1.constants import TESTS_DIR
from synda.tests.manager import Manager
from synda.source.db.task.file.models import get_rows_filtered_on_file_functional_id as get_record
from synda.tests.context.envs.env1.constants import DB as DB_CONTEXT
from synda.tests.context.envs.env1.constants import ENV


def get_subcommand_dirname(subcommand):
    return os.path.join(
        TESTS_DIR,
        subcommand,
    )


def get_test_download_start_fullfilename():
    dirname = os.path.join(
        get_subcommand_dirname("download"),
        "start",
    )

    fullfilename = os.path.join(
        dirname,
        "test_env1_download_start.py",
    )

    return fullfilename


def test_download_start(manager):

    source = ENV["full_filename"]
    manager.create_test_environment(source=source)

    fullfilename = get_test_download_start_fullfilename()

    # STEP 1 : start the asynchronous download process

    run_test_under_subprocess(fullfilename, popen=False)

    manager.delete_test_environment()


def main(coverage_activated=False):

    manager = Manager()
    manager.set_tests_mode()
    manager.delete_test_environment()

    test_download_start(manager)


if __name__ == '__main__':
    main()

