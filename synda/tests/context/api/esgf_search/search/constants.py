# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.api.esgf_search.constants import TYPE_FILE
from synda.source.config.api.esgf_search.constants import TYPE_DATASET

expected = {
    TYPE_DATASET: "cmip5.output1.ICHEC.EC-EARTH.rcp45.6hr.atmos.6hrPlev.r7i1p1.v20120417",
    TYPE_FILE: "CMIP6.AerChemMIP.AS-RCEC.TaiESM1.histSST.r1i1p1f1.Amon.cfc11global.gm.v20200309."
               "cfc11global_Amon_TaiESM1_histSST_r1i1p1f1_gm_185001-201412.nc",
}
CONTEXT = {
    'env': {
        'default': {
            "user_cases": {
                "atmos": {
                    'arguments': {
                        'positional': ["realm=atmos"],
                        'optional': [
                            {"--limit": "1"},
                        ],
                    },
                    'expected': expected,
                }
            }
        }
    },
}
