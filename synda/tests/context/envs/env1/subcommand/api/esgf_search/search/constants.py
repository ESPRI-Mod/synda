# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.context.envs.env1.constants import ENV

EXPECTED_FILE = list(ENV["files"].keys())[0]
EXPECTED_DATASET = ENV["datasets"][0]

CONTEXT = {
    'arguments': {
        'positional': [ENV["data_node"]],
        'optional': [],
    },
}
