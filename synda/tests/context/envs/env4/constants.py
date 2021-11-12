# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.config.file.env.constants import FILENAME as ENV_FILENAME
from synda.tests.process.envs.constants import DATA_DIRECTORY

FUNCTIONAL_DIRECTORY_NAME = "env4"

DATA_DIRECTORY = os.path.join(
    DATA_DIRECTORY,
    FUNCTIONAL_DIRECTORY_NAME,
)


ENV = dict(
    full_filename=os.path.join(
        DATA_DIRECTORY,
        ENV_FILENAME,
    ),
    config=dict(
        core=dict(
            selection_path="/env4/my/selection/path",
            default_path="/env4/my/default/path",
            data_path="/env4/my/data/path",
            db_path="/env4/my/db/path",
            sandbox_path="/env4/my/sandbox/path",
        ),
        check=dict(
            paths=dict(
                error_type="[core] Section of your sdt.conf file / The following Path has not been Found",
            ),
        ),
    ),
)

DB = dict(
    files=[],
    dataset=dict(
        name="CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605",
        version="20180727",
    ),
)
