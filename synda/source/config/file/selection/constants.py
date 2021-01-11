# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
IDENTIFIER = "selection"

DEFAULT = 'default.txt'
DEFAULT_PROJECT_TEMPLATE = 'default_{}.txt'

# SDSSSP means 'SynDa Specific Scalar Selection Parameters'

SDSSSP = [
    'action',
    'selection_group',
    'nearest',
    'keep_replica',
    'last_query',
    'protocol',
    'url_replace',
    'selection_file',
    'selection_filename',
    'searchapi_host',
    'local_path_format',
    'local_path_product_format',
    'local_path_project_format',
    'local_path_drs_template',
    'onemgf',
    'priority',
    'progress',
    'tps',
    'verbose',
]

# SDSSP means 'SynDa Specific Selection Parameters'

OTHERS = [
    'local_path',
    'status',
    'error_msg',
    'sdget_status',
    'timeslice',
    'insertion_group_id',
]

SDSSP = SDSSSP + OTHERS

# 'BIDPP' means 'Before Inference Default Parameter Prefix'.
# 'bidp_' means 'Before Inference Default Parameter'.
BIDPP = 'bidp_'

# 'BIFPP' means 'Before Inference Forced Parameter Prefix'.
# 'bifp_' means 'Before Inference Forced Parameter'.
BIFPP = 'bifp_'

# 'AIDPP' means 'After Inference Default Parameter Prefix'.
# 'aidp_' means 'After Inference Default Parameter'.
AIDPP = 'aidp_'

# 'AIFPP' means 'After Inference Forced Parameter Prefix'.
# 'aifp_' means 'After Inference Forced Parameter'.
AIFPP = 'aifp_'

# this parameter contains unnamed parameters list (i.e. it contains a  list of parameter values)
PENDING_PARAMETER = 'pending_parameter'

PARAM_TYPE_CONTROLLED = 'param_type_controlled'
PARAM_TYPE_FREE = 'param_type_free'

TYPES = [
    PARAM_TYPE_CONTROLLED,
    PARAM_TYPE_FREE,

]


STRUCTURE = dict(
    param=dict(
        type=dict(
            controlled=PARAM_TYPE_CONTROLLED,
            free=PARAM_TYPE_FREE,

        ),
        types=TYPES,
    ),
)
