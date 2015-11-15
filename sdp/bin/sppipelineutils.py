#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains post-processing pipeline job argument builder.

Note
    - 'sppparg' means 'Synda Post-Processing Pipeline ARGument'
"""
import spconfig

def remove_first_facet(path):
    """Remove first item in path

    path sample
        CMIP5/*/MIROC/MIROC5/historical/day/atmos/day/r2i1p1/v20120710
    """
    dataset_pattern=dataset_pattern.strip('/') # if leading and/or trailing slash exist, remove them

    li=dataset_pattern.split('/')

    li=li[1:]

    return '/'.join(li)

def remove_product(dataset_pattern):
    return dataset_pattern.replace('/*/','/merge/')

def replace_product(dataset_pattern):
    return dataset_pattern.replace('/*/','/merge/')

def get_full_path_variable(dataset_pattern,project,variable,prefix):
    return '%s/%s/%s/%s/'%(spconfig.data_folder,prefix,dataset_pattern,variable)
