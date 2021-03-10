# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sys
import os
import re
import subprocess
import pytest


def get_pytest_source_fullfilename():

    fullfilename = os.path.join(
        os.path.dirname(pytest.__file__),
        "__main__.py",
    )
    return fullfilename


def is_test_filename(filename):
    regex = "^test_.*.py$"
    match = re.search(regex, filename)
    return True if match else False


def search_requested_fullfilenames(dirname):
    fullfilenames = []
    for dirpath, subdirectories, filenames in os.walk(dirname):
        for filename in filenames:
            if is_test_filename(filename):
                fullfilenames.append(
                    os.path.join(
                        dirpath,
                        filename,
                    ),
                )
    return fullfilenames


def run_simple_tests(fullfilenames, coverage_activated=False):
    for f in fullfilenames:
        print(
            "Testing : {}".format(f),
        )
        try:
            if coverage_activated:
                args = ["-v", "-m", "on_all_envs", "--cov=sdt", "-x", "--capture=no", f]
            else:
                args = ["-v", "-m", "on_all_envs", "-x", "--capture=no", f]
            pytest.main(args)
        except Exception:
            sys.exit(-1)


def run_test_under_subprocess(fullfilename, coverage_activated=False):
    print(
        "Testing : {}".format(fullfilename),
    )
    if coverage_activated:
        args = ["python", get_pytest_source_fullfilename(), "-v", "-m", "on_all_envs", "--cov=sdt", "-x", fullfilename]
    else:
        args = ["python", get_pytest_source_fullfilename(), "-v", "-m", "on_all_envs", "-x", fullfilename]
    subprocess.call(args)
