#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains args shared across multiple modules."""

def add_playback_record_options(parser):
    grp=parser.add_mutually_exclusive_group(required=False)
    grp.add_argument('-p','--playback',help='Read metadata from FILE',metavar='FILE')
    grp.add_argument('-r','--record',help='Write metadata to FILE',metavar='FILE')
