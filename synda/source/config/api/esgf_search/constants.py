# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
OUTPUT_FORMAT = 'json'

# SANAP means 'Search-API Non Authorized Parameter'
SANAP = ['offset', 'facets', 'format']

# SASP means 'Search-API Scalar Parameter' (note that unlike 'SDSSSP' parameters,
# those parameters are not converted to scalar type in 'sdvectortoscalar'
# (this is because they will be processed using a generic function at the end of the pipeline,
# which need argument type to be 'list')
SASP = ['type', 'limit']

TYPE_FILE = 'File'
# aggregation ~ variable (only use locally (i.e. search-api doesn't support it for now except for some special project))
TYPE_AGGREGATION = 'Aggregation'

TYPE_DATASET = 'Dataset'

TYPES = [
    TYPE_AGGREGATION,
    TYPE_DATASET,
    TYPE_FILE,

]

STRUCTURE = dict(
    type=dict(
        aggregation=TYPE_AGGREGATION,
        dataset=TYPE_DATASET,
        file=TYPE_FILE,

    ),
    types=TYPES,
)
