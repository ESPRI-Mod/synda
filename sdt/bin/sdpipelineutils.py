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
