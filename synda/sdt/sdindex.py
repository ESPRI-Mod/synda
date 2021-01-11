#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

import random
import sdtools
from synda.source.config.file.user.preferences.models import Config

"""This module contains index related routines."""


def get_index_list():
    return sdtools.split_values(
        Config().index_indexes,
    )


def get_default_index():
    return Config().index_default_index


def get_random_index():
    return random.choice(index_host_list)

# init.


index_host_list = get_index_list()
