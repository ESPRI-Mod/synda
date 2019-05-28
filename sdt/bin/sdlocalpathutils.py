#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains local path utils."""

import sdapp
import sdconst
import sdpostpipelineutils
import sdtools
from sdexception import SDException

def build_dataset_local_path(f):
    fmt=sdpostpipelineutils.get_attached_parameter(f,'local_path_format',sdconst.DEFAULT_LOCAL_PATH_FORMAT)

    if fmt=="treevar":
        path="%(dataset_path)s"%f # note that we don't add var folder here (we do it only for the file local path)
    elif fmt=="tree":
        path="%(dataset_path)s"%f
    elif fmt=="custom" or fmt=="customvar": # TAGJ34234JK24

        # note: 'sdreducecol' filter must be disabled when using this format

        custom_dataset_template=sdpostpipelineutils.get_attached_parameter(f,'local_path_drs_template')
        if custom_dataset_template is not None:

            keys=sdtools.extract_keys_from_template(custom_dataset_template)

            # check that only scalar facets are involved here
            # (i.e. we raise an exception if a facet is used in 'custom_dataset_template' and contains more than one value)
            # 
            for key in keys:
                if key in f:
                    val=f[key]
                    if isinstance(val,list):
                        if len(val)==0:
                            raise SDException('SDLOCALP-018',"'%s' key used in 'local_path_drs_template' but value missing in file's attributes (%s,%s)"%(key,f['dataset_functional_id'],val))
                        elif len(val)>1:
                            raise SDException('SDLOCALP-016',"Only scalar value can be used in 'local_path_drs_template' (%s,%s)"%(f['dataset_functional_id'],val))
                else:
                    raise SDException('SDLOCALP-020',"'%s' key used in 'local_path_drs_template' but value missing in file's attributes (%s)"%(key,f['dataset_functional_id'],))

            # hack
            #
            # cast list to scalar if any
            #
            # this is needed when an attribute type is 'list' AND the attribute contains exactly one item.
            #
            # currently, it is used only for the following case:
            #     - we trigger CDF event for CORDEX dataset (ie which is a project with one var per dataset)
            #     - at TAGJ43KJ234JK, we build a dataset local path in a DATASET pipeline context,
            #       which mean that the variable attribute have the 'list' type (see sdpostxptransform for details) 
            #     - so we solve this case here by casting list to scalar (this is ok because there is only
            #       one item in the dataset variable attribute with the CORDEX project (not true for every project)
            #
            values={}
            for key in keys:
                values[key]=sdtools.scalar(f[key])

            path=custom_dataset_template%values
        else:
            raise SDException('SDLOCALP-014',"'local_path_drs_template' must be set when 'local_path_format' is set to 'custom'.")

    elif fmt=="homemade":

        # note: 'sdreducecol' filter must be disabled when using this format

        path=local_path_homemade_transform(f)
    elif fmt=="notree":
        path=""
    else:
        raise SDException('SDLOCALP-010',"'local_path_format' is incorrect (%s)"%fmt)

    return path

def build_file_local_path(f):
    fmt=sdpostpipelineutils.get_attached_parameter(f,'local_path_format',sdconst.DEFAULT_LOCAL_PATH_FORMAT)

    if fmt=="treevar":
        path="%(dataset_local_path)s/%(variable)s/%(filename)s" % f
    elif fmt=="tree":
        path="%(dataset_local_path)s/%(filename)s"%f
    elif fmt=="custom":
        path="%(dataset_local_path)s/%(filename)s"%f
    elif fmt=="customvar": # TAGJ34234JK24
        path="%(dataset_local_path)s/%(variable)s/%(filename)s"%f
    elif fmt=="homemade":
        path="%(dataset_local_path)s/%(filename)s"%f
    elif fmt=="notree":
        path="%(filename)s"%f
    else:
        raise SDException('SDLOCALP-001',"'local_path_format' is incorrect (%s)"%fmt)

    return path

def local_path_homemade_transform(f):
    """
    This is to implement complex rules to build local_path (rules which cannot
    fit even using custom format).

    TODO
        Make a plugin of this func
    """

    # user code goes here
    #
    # sample
    path="%(dataset_path)s"%f

    return path
