#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains domain utils."""

import sdconst

def is_one_var_per_ds(project):
    if project in sdconst.PROJECT_WITH_ONE_VARIABLE_PER_DATASET:
        return True
    else:
        return False
