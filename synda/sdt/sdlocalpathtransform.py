#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains local path transformation routines."""

import re
from synda.sdt import sdapp
from synda.sdt import sdconst
from synda.sdt import sdpostpipelineutils
from synda.sdt import sdproduct
from synda.sdt import sdexception

def transform_local_path_project(files,key):

    def extract_project(path):
        m=re.search('^([^/]+)/',path)
        if m!=None:
            project=m.group(1)

            return project
        else:
            raise sdexception.SDException('SDLOCALP-006','Incorrect value (path=%s)'%path)

    for f in files:
        fmt=sdpostpipelineutils.get_attached_parameter(f,'local_path_project_format',sdconst.DEFAULT_LOCAL_PATH_PROJECT_FORMAT)
        if fmt=="uc":

            path=f[key]

            project=extract_project(path)

            f[key]=re.sub(r'^'+project,project.upper(),path)

    return files

def transform_local_path_product(files,key):

    for f in files:
        fmt=sdpostpipelineutils.get_attached_parameter(f,'local_path_product_format',sdconst.DEFAULT_LOCAL_PATH_PRODUCT_FORMAT)

        if fmt=="normal":
            pass
        elif fmt=="merge":
            f[key]=sdproduct.replace_output12_product_with_output_product(f[key])
        elif fmt=="remove":
            f[key]=sdproduct.remove_product(f[key])
        else:
            raise sdexception.SDException('SDLOCALP-002',"'local_path_product_format' is incorrect (%s)"%fmt)

    return files
