#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains product related routines."""

def remove_product(path):
    for product in ['/output/','/output1/','/output2/']:
        path=path.replace(product,"/")
    return path

def replace_output12_product_with_output_product(path):
    for product in ['/output1/','/output2/']:
        path=path.replace(product,"/output/")
    return path

def replace_output12_product_with_wildcard(path):
    for product in ['/output1/','/output2/']:
        path=path.replace(product,"/*/")
    return path

def get_output12_dataset_paths(path,replace_func=replace_output12_product_with_wildcard):
    """Return tuple with output1 based dataset path and output2 based dataset path."""

    dataset_pattern=replace_func(path)

    o1=dataset_pattern.replace("/*/","/output1/")
    o2=dataset_pattern.replace("/*/","/output2/")

    tu=(o1,o2)

    return tu

def replace_product_with_sql_wildcard(path):
    """Replace product with SQL wildcard."""
    for product in ['/output1/','/output2/','/output/','/merge/']:
        path=path.replace(product,'/%/')
    return path
