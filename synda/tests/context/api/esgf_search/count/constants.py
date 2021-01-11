# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.api.esgf_search.constants import TYPE_DATASET
from synda.source.config.api.esgf_search.constants import TYPE_FILE


CONTEXT = {
    'env': {
        'default': {
            "user_cases": {
                "cmip5": {
                    'arguments': {
                        'positional': ["CMIP5"],
                        'optional': [],
                    },
                    'expected': {
                        TYPE_DATASET: 138513,
                        TYPE_FILE: 8055230,
                    },
                }
            }
        }
    },
}
