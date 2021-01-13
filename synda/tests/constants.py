# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda import tests


TESTS_DIR = os.path.join(
    os.path.dirname(tests.__file__),
    'tests',
)


# INPUT DATA REQUIRED FOR TESTS

DATADIR = os.path.join(
    TESTS_DIR,
    'data',
)

SUBCOMMANDS_DIR = os.path.join(
    TESTS_DIR,
    "subcommands",
)

SYNCHRONOUS_SUBCOMMANDS_DIR = os.path.join(
    SUBCOMMANDS_DIR,
    "synchronous",
)

ASYNCHRONOUS_SUBCOMMANDS_DIR = os.path.join(
    SUBCOMMANDS_DIR,
    "asynchronous",
)

# OUTPUT DATA LOCATION

ST_HOME_TESTS = os.path.join(
    os.environ["ST_HOME"],
    ".tests",
)

# TESTS DB LOCATION

DB_HOME_TESTS = os.path.join(
    ST_HOME_TESTS,
    "db",
)


def is_test_mode_activated():
    test_mode_activated = False
    if "ST_TESTS_MODE_STATUS" in os.environ:
        if os.environ["ST_TESTS_MODE_STATUS"] == "activated":
            test_mode_activated = True
    return test_mode_activated

# SQLITE DATABASE CONFIG

# 2 minute timeout
DB_CONNECTION_TIMEOUT = 120

# DAEMON

WAIT_DURATION_AFTER_DAEMON_START = 20
WAIT_DURATION_AFTER_DAEMON_STOP = 10
