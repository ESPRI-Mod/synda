# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from glob import glob

from synda.tests.tests.constants import ST_HOME_TESTS
from synda.source.config.file.env.constants import FILENAME as ENV_FILENAME
from synda.tests.process.env.build.installed.constants import INSTALLED_ENV_DATA_DIRECTORY
from synda.tests.process.env.build.installed.remove.constants import DATA_RESOURCES_DIRECTORY

FUNCTIONAL_DIRECTORY_NAME = "remove"
DATA_DIRECTORY = os.path.join(
    INSTALLED_ENV_DATA_DIRECTORY,
    FUNCTIONAL_DIRECTORY_NAME,
)

data_file = glob(
    os.path.join(
        os.path.join(
            DATA_RESOURCES_DIRECTORY,
            "**",
        ),
        "*.nc",
    ),
    recursive=True,
)[0]

items = data_file.replace(DATA_RESOURCES_DIRECTORY, "").split(os.path.sep)
data_file=\
    os.path.join(
        os.path.join(
            ST_HOME_TESTS,
            "data",
        ),
        *items,
    )

ENVS = dict(
    installed=dict(
        env=dict(
            full_filename=os.path.join(
                DATA_DIRECTORY,
                ENV_FILENAME,
            ),
            selection_file=os.path.join(
                DATA_DIRECTORY,
                "selection_file.txt",
            ),
            dataset="tntogw_EmonZ_IPSL-CM6A-LR_historical_r23i1p1f1_grz_195001-201412.nc",
            local_path=os.path.join(
                os.path.join(
                    ST_HOME_TESTS,
                    "data",
                ),
                data_file.replace(DATA_RESOURCES_DIRECTORY, ""),
            ),
        ),
    ),
)
