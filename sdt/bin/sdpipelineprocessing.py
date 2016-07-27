#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains pipeline execution routines."""

import sdtypes

def run_pipeline(io_mode,metadata,f,*args,**kwargs):
    """
    Note
        Beware: metadata input argument is modified in this func !
        (you have to make a copy before calling this func if you want
        to keep original data)
    """

    if io_mode=='no_chunk':

        # way 0: load-all-in-memory (no chunk).
        files=f(metadata.get_files(),*args,**kwargs)
        metadata.set_files(files)

    elif io_mode=='generator':

        # way 1: chunk-by-chunk (using a second store)
        new_metadata=sdtypes.Metadata()
        for chunk in metadata.get_chunks(io_mode):
            chunk=f(chunk,*args,**kwargs)
            new_metadata.add_files(chunk)
        metadata.delete() # FIXME everywhere
        metadata=new_metadata

    elif io_mode=='pagination':

        # way 2: chunk-by-chunk (updating store on-the-fly)
        for chunk in metadata.get_chunks(io_mode):
            chunk=f(chunk,*args,**kwargs)
            metadata.update(chunk)

    else:
        assert False

    return metadata
