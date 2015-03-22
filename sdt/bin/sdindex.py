#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdindex.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
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
