# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
METADATA_SERVER_TYPES = ['esgf_search_api']

OUTPUT_FORMAT_JSON = 'json'
OUTPUT_FORMAT_XML = 'xml'


# Fields that MUST be part of every search-api requests
#
# Notes
#     - 'size' is required as non-optional part of basic data structure (Metadata, Response..)
#
REQUIRED_FIELDS = ['type', 'size']

# Light fields are used to retrieve just the necessary fields, so to limit the bandwidth footprint.
#
# Notes
#     - we add data_node here, because it's needed for many thing ('-r' option, nearest..)
#     - we add variable for file too, so to be able to remove malformed files
#       (i.e. some malformed files have many variables set instead of one)
#     - 'instance_id' is used for example in 'sdremoveaggregation'
#
BASIC_URL_FIELDS = ['url']
BASIC_VARIABLE_FIELDS = ['title', 'instance_id', 'variable']
BASIC_TIMESTAMP_FIELDS = ['instance_id', 'timestamp', '_timestamp']
BASIC_LIGHT_FIELDS = ['instance_id', 'id', 'variable', 'data_node']

LIGHT_FIELDS = BASIC_LIGHT_FIELDS + REQUIRED_FIELDS
TIMESTAMP_FIELDS = BASIC_TIMESTAMP_FIELDS + REQUIRED_FIELDS
URL_FIELDS = BASIC_URL_FIELDS + REQUIRED_FIELDS
VARIABLE_FIELDS = BASIC_VARIABLE_FIELDS + REQUIRED_FIELDS
