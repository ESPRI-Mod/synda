#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains search-API 'fields' related routines."""
from synda.source.config.api.constants import LIGHT_FIELDS
from synda.source.config.api.constants import TIMESTAMP_FIELDS
from synda.source.config.api.constants import VARIABLE_FIELDS


def get_timestamp_fields():
    return ','.join(TIMESTAMP_FIELDS)


def get_sample_fields():
    return ','.join(TIMESTAMP_FIELDS)


def get_file_variable_fields():
    return ','.join(VARIABLE_FIELDS)


def get_variable_light_fields():
    return ','.join(LIGHT_FIELDS)


def get_dataset_light_fields():
    return ','.join(LIGHT_FIELDS)


def get_all_dataset_fields():
    return '*'


def get_all_variable_fields():
    return '*'
