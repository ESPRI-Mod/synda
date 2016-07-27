#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains pipeline common routines."""

import os
import sys
import json
import sdtypes

def get_input_data(path,deserialize_by_line=False):
    """Deserialize and returns input data (from file or stdin).

    Args:
        deserialize_by_line (bool): if true, each line is one distinct JSON document, 
                                    else the whole stream is one JSON document.
                                    Useful when input come from many outputs merged together
                                    (i.e. make it possible to use "by line" streams, which 
                                    can be merged using simple command (e.g. Unix 'cat')).

    Note
        This func is NOT related with 'selection file'. It is related with JSON file.
    """

    def f_deserialize_by_line(stream):
        """Each line represent a distinct JSON document.
        Note:
            'f_' prefix is prepended to the function name to prevent collision
            with the variable of same name.
        """
        
        keysvals_groups=[]
        lines=stream.readlines()
        for line in lines:
            facets_group=json.loads(line)
            keysvals_groups.append(facets_group)

        return keysvals_groups

    if os.path.isfile(path):
        with open(path, 'r') as fh:
            keysvals_groups=f_deserialize_by_line(fh) if deserialize_by_line else json.load(fh)
    else:
        keysvals_groups=f_deserialize_by_line(sys.stdin) if deserialize_by_line else json.load(sys.stdin)

    return keysvals_groups

def perform_chunk_by_chunk(fetch_mode,metadata,f,*args,**kwargs):

    if fetch_mode=='no_chunk':

        # way 0: load-all-in-memory (no chunk)
        files=f(metadata.get_files(),*args,**kwargs)
        metadata.set_files(files)

    elif fetch_mode=='generator':

        # way 1: chunk-by-chunk (using a second store)
        new_metadata=sdtypes.Metadata()
        for chunk in metadata.get_chunks(fetch_mode):
            chunk=f(chunk,*args,**kwargs)
            new_metadata.add_files(chunk)
        metadata.delete() # FIXME
        metadata=new_metadata

    elif fetch_mode=='pagination':

        # way 2: chunk-by-chunk (updating store on-the-fly)
        for chunk in metadata.get_chunks(fetch_mode):
            chunk=f(chunk,*args,**kwargs)
            metadata.update(chunk)

    else:
        assert False

    return metadata
