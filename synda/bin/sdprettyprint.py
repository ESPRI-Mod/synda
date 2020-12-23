#!/usr/bin/python -u
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains specific printing routines."""

import sys
import argparse
import json
import sdapp
import humanize
from sdtypes import File

def run(files):
    
    pretty_label={'done':'installed'} # this is have a listing like dpkg/apt-get

    for file_ in files:

        if 'status' in file_:
            # this case is to print file after the file pipeline 

            f=File(**file_)

            size=humanize.naturalsize(f.size,gnu=False)

            print "%-12s %-8s %s"%(pretty_label.get(f.status,f.status),size,f.filename)
        else:
            # this case is to print file in a early step (before 'status' has
            # been retrieved from local db and before filename has been added)

            f=File(**file_)

            size=humanize.naturalsize(f.size,gnu=False)

            print "%-8s %s"%(size,f.title)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )

    run(files)
