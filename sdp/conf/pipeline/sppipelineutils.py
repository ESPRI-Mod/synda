#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains post-processing pipeline utils."""

TODO_CHECK

def remove_first_facet(path):
    """Remove first item in path

    path sample
        CMIP5/*/MIROC/MIROC5/historical/day/atmos/day/r2i1p1/v20120710
    """
    path=path.strip('/') # if leading and/or trailing slash exist, remove them

    li=path.split('/')

    li=li[1:]

    return '/'.join(li)

def replace_product_facet(dataset_pattern):
    return dataset_pattern.replace('/*/','/merge/')

def build_user_path(kw):
    """Build end-user path.

    Sample
        /prodigfs/project/CMIP5/main/CNRM-CM5/historicalGHG/fx/atmos/fx/...
    """

    # Remove project facet. WARNING: we assume all datasets start with 'project'
    # facet (but this is not the case for some projects, e.g. obs4MIPs /
    # RMBE.ARMBE_Wind_Direction)
    dataset_pattern=remove_first_facet(kw.dataset_pattern)

    # Remove product facet
    dataset_pattern=remove_first_facet(dataset_pattern) if kw.project in ['CMIP5','CORDEX'] else dataset_pattern

    path='%s/%s/%s/%s/%s'%(kw.data_folder,'project',kw.project,'main',dataset_pattern)
    path='%s/%s'%(path,kw.variable) if kw.path_type=='variable' else path
    path+='/' # add ending slash

    return path

def build_mirror_path(kw):

    path='%s/%s/%s'%(kw.data_folder,'esgf/mirror',kw.dataset_pattern)
    path='%s/%s'%(path,kw.variable) if kw.path_type=='variable' else path
    path+='/' # add ending slash

    return path

def build_process_path(kw):
    dataset_pattern=replace_product_facet(kw.dataset_pattern) if kw.project=='CMIP5' else kw.dataset_pattern # product coalesce hack

    path='%s/%s/%s'%(kw.data_folder,'esgf/process',dataset_pattern)
    path='%s/%s'%(path,kw.variable) if kw.path_type=='variable' else path
    path+='/' # add ending slash

    return path
