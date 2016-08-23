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

import sdapp
import sdtypes
import sdlog
import sdconst

class ProcessingObject(object):
    def __init__(self,f,*args,**kwargs):
        self.f=f # note: this func must take files list as first argument (i.e. chunk).
        self.args=args # note: this do not contain the first argument of f. It will be set automatically during processing (see below).
        self.kwargs=kwargs

def run_pipeline(metadata,po,io_mode=sdconst.PROCESSING_FETCH_MODE_GENERATOR):
    """
    Note
        Beware: metadata input argument is modified in this func !
        (you have to make a copy before calling this func if you want
        to keep original data)
    """

    # alias
    f=po.f
    args=po.args
    kwargs=po.kwargs

    sdlog.debug("SYNDPIPR-001","Start chunk loop (files-count=%d)"%metadata.count())

    if io_mode=='no_chunk':

        # way 0: load-all-in-memory (no chunk).
        files=f(metadata.get_files(),*args,**kwargs)
        metadata.set_files(files)

    elif io_mode=='generator':

        # way 1: chunk-by-chunk (using a second store)
        new_metadata=sdtypes.Metadata()
        for chunk in metadata.get_chunks(io_mode):

            sdlog.debug("SYNDPIPR-002","Process chunk")

            chunk=f(chunk,*args,**kwargs)
            new_metadata.add_files(chunk)

        metadata=new_metadata # note: metadata old value get's removed here (destructor is called). This is to enforce that this function IS destructive with its input argument (see func comment for more info).

    elif io_mode=='pagination':

        # way 2: chunk-by-chunk (updating store on-the-fly)
        for chunk in metadata.get_chunks(io_mode):
            chunk=f(chunk,*args,**kwargs)
            metadata.update(chunk) # TODO: check if 'size' is handled here

    elif io_mode=='experimental':

        # use 'ALTER TABLE foo RENAME TO bar' here

        pass

    else:
        assert False

    sdlog.debug("SYNDPIPR-003","Chunk loop completed (files-count=%d)"%metadata.count())

    return metadata
