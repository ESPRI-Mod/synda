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
from synda.source.config.api.esgf_search.constants import TYPE_FILE, TYPE_DATASET
from synda.tests.process.env.build.installed.list.constants import DATA_DIRECTORY

FILE1 = 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc'
FILE2 = 'aims3.llnl.gov'

ENVS = dict(
    installed=dict(
        env=dict(
            full_filename=os.path.join(
                DATA_DIRECTORY,
                ENV_FILENAME,
            ),
            expected={
                TYPE_DATASET: ["cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006"],
                TYPE_FILE: [FILE1, FILE2],
           },
        ),
    ),
)
