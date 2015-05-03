#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

import random
import sdconfig
import sdtools

"""This module contains index related routines."""

def get_index_list():
    return sdtools.split_values(sdconfig.config.get('index','indexes'))

def get_default_index():
    return sdconfig.config.get('index','default_index')

def get_random_index():
    return random.choice(index_host_list)

# init.

index_host_list=get_index_list()
