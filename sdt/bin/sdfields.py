#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains search-API 'fields' related routines."""

import sdconst

def get_timestamp_fields():
    return ','.join(sdconst.TIMESTAMP_FIELDS)

def get_sample_fields():
    return ','.join(sdconst.TIMESTAMP_FIELDS)

def get_file_variable_fields():
    return ','.join(sdconst.VARIABLE_FIELDS)

def get_dataset_version_fields():
    return ','.join(sdconst.DATASET_VERSION_FIELDS)

def get_file_light_fields():
    return ','.join(sdconst.LIGHT_FIELDS)

def get_variable_light_fields():
    return ','.join(sdconst.LIGHT_FIELDS)

def get_dataset_light_fields():
    return ','.join(sdconst.LIGHT_FIELDS)

def get_all_dataset_fields():
    return '*'

def get_all_variable_fields():
    return '*'

# init.
