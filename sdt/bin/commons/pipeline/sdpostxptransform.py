#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module perform post xml parsing transformations.

Description
    Transforms vector to scalar (change file attributes's *values* only (name stay the same)).

Note
    sdpostxptransform means 'SynDa post Xml Parsing transform'
"""

from sdt.bin.commons.utils.sdexception import SDException


def run(files):
    force_scalar(files)  # warning: this changes 'files_after_xml_parsing' object
    return files


def force_scalar(files):
    if len(files) > 0:

        # retrieve type
        file_ = files[0]  # 'type' is the same for all files
        type_ = file_['type']  # 'type' itself IS scalar

        if type_ == 'File':

            for f in files:
                for k in f:
                    try:
                        f[k] = list_to_scalar(f[k])
                    except:

                        # If conversion failed, do not raise fatal exception anymore, instead, leave it as vector
                        # (so far, conversion failed only for non-mandatory attributes (from Synda perspective),
                        # so it should not impact the process.
                        #
                        # Examples of attributes that trigger conversion failure are 'experiment_family', 'description'.
                        #
                        # raise SDException("SYNDAXML-003","List to scalar conversion error (key=%s,value=%s)"%(k,f[k]))
                        pass

        elif type_ == 'Dataset':

            for f in files:
                for k in f:
                    # those items are real vector (all other are vector of only one item, which means scalar)
                    # this item is synda specific and do not need transform
                    if k not in ('cf_standard_name', 'variable', 'variable_long_name', 'access',
                                 'attached_parameters'):
                        try:
                            f[k] = list_to_scalar(f[k])
                        except Exception as e:
                            pass


def list_to_scalar(value):
    if isinstance(value, list):
        if len(value) != 1:
            raise SDException("SYNDAXML-002", "Incorrect scalar value ({},{})".format(value, key))
        else:
            return value[0]  # transform to scalar and return
    else:
        # already scalar, return as is

        return value
