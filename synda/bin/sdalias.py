#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains alias routines."""

def keep_old_model_name(model):
    """This func is used when you have a lot of already transferred data and
    don't want to move on a new naming scheme.

    Not used for now.

    Deprecated, as we now use model and institute from dataset path, which are the same from the beginning (i.e. CCCma, inmcm4, etc...)
    """
    
    if model=="INM-CM4":
        return "inmcm4"
    elif model=="GFDL-CM2-1":
        return "GFDL-CM2p1"
    elif model=="BCC-CSM1-1":
        return "bcc-csm1-1"
    elif model=="BCC-CSM1-1-m":
        return "bcc-csm1-1-m"
    else:
        return model

def keep_old_institute_name(institute):
    """This func is used when you have a lot of already transferred data and
    don't want to move on a new naming scheme.

    Not used for now.

    Deprecated, as we now use model and institute from dataset path, which are the same from the beginning (i.e. CCCma, inmcm4, etc...)
    """

    if institute=="CCCMA":
        return "CCCma"
    else:
        return institute
