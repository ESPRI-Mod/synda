#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

import spapp

EVENT_VARIABLE_COMPLETE='variable_complete'
EVENT_LATEST_DATASET_COMPLETE='latest_dataset_complete'
#
EVENT_OUTPUT12_VARIABLE_COMPLETE='variable_complete_output12'
EVENT_OUTPUT12_DATASET_COMPLETE='dataset_complete_output12'
EVENT_OUTPUT12_LATEST_DATASET_COMPLETE='latest_dataset_complete_output12'
EVENT_OUTPUT12_NON_LATEST_DATASET_COMPLETE='non_latest_dataset_complete_output12'
EVENT_OUTPUT12_DATASET_LATEST='dataset_latest_output12' # triggered when dataset is promoted latest

EVENT_STATUS_NEW='new'
EVENT_STATUS_ANOMALY='anomaly'
EVENT_STATUS_OLD='old'

PPPRUN_STATUS_NEW="new"
PPPRUN_STATUS_WAITING="waiting"
PPPRUN_STATUS_RUNNING="running"
PPPRUN_STATUS_DONE="done"
PPPRUN_STATUS_ERROR="error"
PPPRUN_STATUS_PAUSE="pause"
#
JOB_STATUS_RUNNING="running"
JOB_STATUS_DONE="done"
JOB_STATUS_ERROR="error"
#
LOGGER='daemon'
LOGFILE='daemon.log'
#
CHUNKSIZE=10000 # maximum files number returned by one search-api call
#
SEARCH_API_HTTP_TIMEOUT=300 # Search-API HTTP timeout (time to wait for HTTP response)
#
PARAM_TYPE_CONTROLLED='param_type_controlled'
PARAM_TYPE_FREE='param_type_free'
#
DEFAULT_PRIORITY=1000
#
PROJECT_WITH_ONE_VARIABLE_PER_DATASET=['CORDEX','CMIP6']
