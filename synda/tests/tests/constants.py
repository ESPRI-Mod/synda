# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from synda.tests import tests


TESTS_DIR = os.path.dirname(tests.__file__)


# INPUT DATA REQUIRED FOR TESTS

DATADIR = os.path.join(
    TESTS_DIR,
    'data',
)

# OUTPUT DATA LOCATION

ST_HOME_TESTS = os.path.join(
    os.environ["ST_HOME"],
    ".tests",
)

# TESTS DB LOCATION

DATA_HOME_TESTS = os.path.join(
    ST_HOME_TESTS,
    "data",
)

# TESTS DB LOCATION

DB_HOME_TESTS = os.path.join(
    ST_HOME_TESTS,
    "db",
)

# TESTS DATA FILE LOCATION

FILE_HOME_TESTS = os.path.join(
    DATADIR,
    "file",
)

# TESTS DATA INPUT LOCATION

USER_FILE_HOME_TESTS = os.path.join(
    FILE_HOME_TESTS,
    "user",
)

PREFERENCES_USER_FILE_HOME_TESTS = os.path.join(
    USER_FILE_HOME_TESTS,
    "preferences",
)


DATASET_EXAMPLE = dict(
    name="cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601",
    version="20120601",
    files=[
        "areacella_fx_CanCM4_decadal1972_r0i0p0.nc",
        "orog_fx_CanCM4_decadal1972_r0i0p0.nc",
        "sftlf_fx_CanCM4_decadal1972_r0i0p0.nc",
    ]
)
