#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdconst.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

import sdapp

EVENT_OUTPUT12_VARIABLE_COMPLETE='variable_complete_output12'
EVENT_OUTPUT12_DATASET_COMPLETE='dataset_complete_output12'
EVENT_OUTPUT12_LATEST_DATASET_COMPLETE='latest_dataset_complete_output12'
EVENT_OUTPUT12_NON_LATEST_DATASET_COMPLETE='non_latest_dataset_complete_output12'
EVENT_OUTPUT12_DATASET_LATEST='dataset_latest_output12' # triggered when dataset is promoted latest

EVENT_STATUS_NEW='new'
EVENT_STATUS_ANOMALY='anomaly'
EVENT_STATUS_OLD='old'

TRANSFER_STATUS_NEW="new"
TRANSFER_STATUS_WAITING="waiting"
TRANSFER_STATUS_RUNNING="running"
TRANSFER_STATUS_DONE="done"
TRANSFER_STATUS_ERROR="error"
TRANSFER_STATUS_DELETE="delete"
TRANSFER_STATUS_PAUSE="pause"
#
TRANSFER_STATUSES_PENDING=[TRANSFER_STATUS_WAITING,TRANSFER_STATUS_RUNNING,TRANSFER_STATUS_ERROR,TRANSFER_STATUS_PAUSE]
TRANSFER_STATUSES_ALL=[TRANSFER_STATUS_NEW,TRANSFER_STATUS_DONE,TRANSFER_STATUS_DELETE]+TRANSFER_STATUSES_PENDING
#
SELECTION_STATUS_NEW="new"           # means it has never been retrieved yet
SELECTION_STATUS_MODIFIED="modified" # means the selection has new modifications since the last run
SELECTION_STATUS_NORMAL="normal"     # means no modification since the last run (and last run complete successfully)
#
DATASET_STATUS_NEW="new"                  # this means it has never been retrieved yet
DATASET_STATUS_EMPTY="empty"              # this means there is no complete variables yet in the dataset (although there may be many files already downloaded)
DATASET_STATUS_IN_PROGRESS="in-progress"  # this means there is at least one complete variable in the dataset
DATASET_STATUS_COMPLETE="complete"        # complete here is related to selection (i.e. it doesn't mean that of variable of the dataset are done)
#
VARIABLE_COMPLETE="complete"
VARIABLE_NOT_COMPLETE="not-complete"
#
DEFAULT_GROUP="default"
#
SDSSSP=['group',
        'nearest',
        'keep_replica',
        'last_query',
        'selection_filename',
        'searchapi_host',
        'local_path_product_format',
        'local_path_format',
        'local_path_project_format',
        'onemgf',
        'priority',
        'progress',
        'tps',
        'verbose']                               # SDSSSP means 'Synchro Data Specific Scalar Selection Parameters'
SDSSP=SDSSSP+['local_path','status','timeslice'] # SDSSP means 'Synchro Data Specific Selection Parameters'
SANAP=['offset', 'facets', 'format']             # SANAP means 'Search-API Non Authorized Parameter'
SASP=['type','limit']                            # SASP means 'Search-API Scalar Parameter' (note that unlike 'SDSSSP' parameters, those parameters are not converted to scalar type in 'sdvectortoscalar' (this is because they will be processed using a generic function at the end of the pipeline, which need argument type to be 'list')
#
BIDPP='bidp_' # 'BIDPP' means 'Before Inference Default Parameter Prefix'. 'bidp_' means 'Before Inference Default Parameter'.
BIFPP='bifp_' # 'BIFPP' means 'Before Inference Forced Parameter Prefix'. 'bifp_' means 'Before Inference Forced Parameter'.
AIDPP='aidp_' # 'AIDPP' means 'After Inference Default Parameter Prefix'. 'aidp_' means 'After Inference Default Parameter'.
AIFPP='aifp_' # 'AIFPP' means 'After Inference Forced Parameter Prefix'. 'aifp_' means 'After Inference Forced Parameter'.
#
LOGGER_FEEDER='feeder'
LOGGER_CONSUMER='consumer'
LOGFILE_FEEDER='discovery.log'
LOGFILE_CONSUMER='transfer.log'


# Maximum files number returned by one search-api call.
#
# Normally, max is 10000 so it should be set to 10000.
# But in some case, when set to 10000, the following strange behaviour occurs:
# the url below
# http://esgf-data.dkrz.de/esg-search/search?fields=instance_id,timestamp&replica=false&type=Dataset&format=application%2Fsolr%2Bxml&limit=10000&offset=8900
# gives this
# <result name="response" numFound="11782" start="8900" maxScore="1.0">
# instead of this
# <result name="response" numFound="314345" start="8900" maxScore="1.0">
# It seems to be of bug on the server side.
#
# So from now, it's set to 9000
CHUNKSIZE=9000

SEARCH_API_HTTP_TIMEOUT=300 # Search-API HTTP timeout (time to wait for HTTP response)
#
PARAM_TYPE_CONTROLLED='param_type_controlled'
PARAM_TYPE_FREE='param_type_free'
#
DEFAULT_LOCAL_PATH_PRODUCT_FORMAT='normal'
DEFAULT_LOCAL_PATH_PROJECT_FORMAT='normal'
DEFAULT_LOCAL_PATH_FORMAT='tree'
#
DEFAULT_PRIORITY=1000
#
ACTION_ADD='add'
ACTION_DELETE='delete'
#
IDXHOSTMARK='IDXHOSTMARK'
#
SA_TYPE_FILE='File'
SA_TYPE_AGGREGATION='Aggregation' # aggregation ~ variable (only use locally (i.e. search-api doesn't support it for now except for some special project))
SA_TYPE_DATASET='Dataset'
#
SA_TYPE_DEFAULT=SA_TYPE_DATASET
SD_TYPE_DEFAULT=SA_TYPE_FILE
#
PENDING_PARAMETER='pending_parameter' # this parameter contains unnamed parameters list (i.e. it contains a  list of parameter values)
#
SELECTION_FROM_CMDLINE='cli'
SELECTION_FROM_STDIN='stdin'
#
PROJECT_WITH_ONE_VARIABLE_PER_DATASET=['CORDEX']

#    name,           type_, default_value,               search_api_facet, option
# TODO => what is 'option' flag for ??? (i.e. is just the exact opposite of 'search_api_facet' flag, isn't it ?
DEFAULT_SESSION_PARAMS=[
    ['verbose',      bool,  True,                         False,           True],
    ['ignorecase',   bool,  False,                        False,           True],
    ['onemgf',       bool,  False,                        False,           True],
    ['last_query',   str,   '',                           False,           True],
    ['dry_run',      bool,  False,                        False,           True],
    ['debug',        bool,  False,                        False,           True],
    ['localsearch',  bool,  False,                        False,           True],
    ['replica',      bool,  False,                        False,           False],
    ['limit',        int,  '20',                          False,           False],
    ['distrib',      bool,  True,                         False,           False],
    ['latest',       bool,  None,                         False,           False],
    ['type',         str,   SD_TYPE_DEFAULT,              False,           False]
]

# Light fields are used to retrieve just the necessary fields, so to limit the bandwidth footprint.
#
# Notes
#     - we add data_node in all light fields, because it's needed for many thing ('-r' option, nearest..)
#     - we add variable for file too, so to be able to remove malformed files (i.e. some malformed files have many variables set instead of one)
#     - 'instance_id' is used for example in 'sdremoveaggregation'
#
LIGHT_FIELDS='instance_id,id,type,data_node,variable'

POST_PIPELINE_MODES=['file','dataset','generic',None]
