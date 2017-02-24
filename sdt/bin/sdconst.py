#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

EVENT_FILE_COMPLETE='file_complete'
EVENT_VARIABLE_COMPLETE='variable_complete'
EVENT_DATASET_COMPLETE='dataset_complete'
EVENT_DATASET_LATEST='dataset_latest'
EVENT_LATEST_DATASET_COMPLETE='latest_dataset_complete'
EVENT_NON_LATEST_DATASET_COMPLETE='non_latest_dataset_complete'
#
EVENT_OUTPUT12_VARIABLE_COMPLETE='variable_complete_output12'
EVENT_OUTPUT12_DATASET_COMPLETE='dataset_complete_output12'
EVENT_OUTPUT12_LATEST_DATASET_COMPLETE='latest_dataset_complete_output12'
EVENT_OUTPUT12_NON_LATEST_DATASET_COMPLETE='non_latest_dataset_complete_output12'
EVENT_OUTPUT12_DATASET_LATEST='dataset_latest_output12' # triggered when dataset is promoted latest
#
EVENT_CDF_INT_VARIABLE='cdf_int_variable' # not used
EVENT_CDF_INT_DATASET='cdf_int_dataset'
EVENT_CDF_INT_VARIABLE_O='cdf_int_variable_o' # project with One variable per dataset
EVENT_CDF_INT_VARIABLE_N='cdf_int_variable_n' # project with N variable per dataset

EVENT_CDF_COR_VARIABLE='cdf_cor_variable' # not used
EVENT_CDF_COR_DATASET='cdf_cor_dataset'
EVENT_CDF_COR_VARIABLE_O='cdf_cor_variable_o' # project with One variable per dataset
EVENT_CDF_COR_VARIABLE_N='cdf_cor_variable_n' # project with N variable per dataset

EVENT_STATUS_NEW='new'
EVENT_STATUS_ANOMALY='anomaly'
EVENT_STATUS_OLD='old'

TRANSFER_PROTOCOL_OPENDAP='opendap'
TRANSFER_PROTOCOL_HTTP='http'
TRANSFER_PROTOCOL_GRIDFTP='gridftp'
TRANSFER_PROTOCOL_GLOBUSTRANSFER='globustransfer'

TRANSFER_PROTOCOLS=[TRANSFER_PROTOCOL_HTTP,TRANSFER_PROTOCOL_GRIDFTP,TRANSFER_PROTOCOL_GLOBUSTRANSFER]

HTTP_CLIENT_URLLIB='urllib'
HTTP_CLIENT_WGET='wget'

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

# SDSSSP means 'SynDa Specific Scalar Selection Parameters'
SDSSSP=['action',
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
        'verbose']

# SDSSP means 'SynDa Specific Selection Parameters'
SDSSP=SDSSSP+['local_path',
              'status',
              'error_msg',
              'sdget_status',
              'timeslice',
              'insertion_group_id']

# SANAP means 'Search-API Non Authorized Parameter'
SANAP=['offset', 'facets', 'format']

# SASP means 'Search-API Scalar Parameter' (note that unlike 'SDSSSP' parameters, those parameters are not converted to scalar type in 'sdvectortoscalar' (this is because they will be processed using a generic function at the end of the pipeline, which need argument type to be 'list')
SASP=['type','limit']

BIDPP='bidp_' # 'BIDPP' means 'Before Inference Default Parameter Prefix'. 'bidp_' means 'Before Inference Default Parameter'.
BIFPP='bifp_' # 'BIFPP' means 'Before Inference Forced Parameter Prefix'. 'bifp_' means 'Before Inference Forced Parameter'.
AIDPP='aidp_' # 'AIDPP' means 'After Inference Default Parameter Prefix'. 'aidp_' means 'After Inference Default Parameter'.
AIFPP='aifp_' # 'AIFPP' means 'After Inference Forced Parameter Prefix'. 'aifp_' means 'After Inference Forced Parameter'.
#
LOGGER_FEEDER='feeder'
LOGGER_CONSUMER='consumer'
LOGGER_DOMAIN='domain'
#
LOGFILE_FEEDER='discovery.log'
LOGFILE_CONSUMER='transfer.log'
LOGFILE_DOMAIN='domain.log'

CHECKSUM_TYPE_MD5='md5'
CHECKSUM_TYPE_SHA256='sha256'
CHECKSUM_TYPES=[CHECKSUM_TYPE_MD5,CHECKSUM_TYPE_SHA256]

METADATA_SERVER_TYPES=['esgf_search_api','thredds_catalog','apache_default_listing']

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
SEARCH_API_CHUNKSIZE=9000

PROCESSING_CHUNKSIZE=5000 # as list maybe duplicated in memory at some point in the pipeline, we use a lower value here than SEARCH_API_CHUNKSIZE
PROCESSING_FETCH_MODE_GENERATOR='generator'

SEARCH_API_HTTP_TIMEOUT=300 # Search-API HTTP timeout (time to wait for HTTP response)
DIRECT_DOWNLOAD_HTTP_TIMEOUT=30 # Direct download HTTP timeout (time to wait for HTTP response)
ASYNC_DOWNLOAD_HTTP_TIMEOUT=360 # Async download HTTP timeout (time to wait for HTTP response)
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
SEARCH_API_OUTPUT_FORMAT_JSON='json'
SEARCH_API_OUTPUT_FORMAT_XML='xml'
#
ACTION_ADD='add'
ACTION_DELETE='delete'
ACTION_PEXEC='pexec'
#
DEFAULT_LIMITS={
    'small':{'search':100,'dump':50,'list':20},
    'medium':{'search':1000,'dump':100,'list':200},
    'big':{'search':6000,'dump':6000,'list':20000}
}
#
IDXHOSTMARK='IDXHOSTMARK'
#
SA_TYPE_FILE='File'
SA_TYPE_AGGREGATION='Aggregation' # aggregation ~ variable (only use locally (i.e. search-api doesn't support it for now except for some special project))
SA_TYPE_DATASET='Dataset'
#
PENDING_PARAMETER='pending_parameter' # this parameter contains unnamed parameters list (i.e. it contains a  list of parameter values)
#
SELECTION_FROM_CMDLINE='cli'
SELECTION_FROM_STDIN='stdin'
#
PROJECT_WITH_ONE_VARIABLE_PER_DATASET=['CORDEX','CMIP6']


# Fields that MUST be part of every search-api requests
#
# Notes
#     - 'size' is required as non-optional part of basic data structure (Metadata, Response..)
#
REQUIRED_FIELDS=['type','size']

# Light fields are used to retrieve just the necessary fields, so to limit the bandwidth footprint.
#
# Notes
#     - we add data_node here, because it's needed for many thing ('-r' option, nearest..)
#     - we add variable for file too, so to be able to remove malformed files (i.e. some malformed files have many variables set instead of one)
#     - 'instance_id' is used for example in 'sdremoveaggregation'
#
LIGHT_FIELDS=['instance_id','id','variable','data_node']+REQUIRED_FIELDS

TIMESTAMP_FIELDS=['instance_id','timestamp','_timestamp']+REQUIRED_FIELDS

URL_FIELDS=['url']+REQUIRED_FIELDS

VARIABLE_FIELDS=['title','instance_id','variable']+REQUIRED_FIELDS

DATASET_VERSION_FIELDS=['master_id','version','timestamp']+REQUIRED_FIELDS


POST_PIPELINE_MODES=['file','dataset','generic',None]

ADMIN_SUBCOMMANDS=['autoremove','install','open','pexec','remove','reset','retry','update','upgrade']

# security_dir values
SECURITY_DIR_TMP='tmp'
SECURITY_DIR_TMPUID='tmpuid'
SECURITY_DIR_HOME='home'
SECURITY_DIR_MIXED='mixed'
