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

import argparse
import sdapp
import humanize
from sdtypes import File

def run(files):
    
    pretty_label={'done':'installed'} # this is have a listing like dpkg/apt-get

    for file_ in files:
        f=File(**file_)

        size=humanize.naturalsize(f.size,gnu=False)

        print "%-12s %-8s %s"%(pretty_label.get(f.status,f.status),f.filename,size)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	args = parser.parse_args()

    files=json.load( sys.stdin )

    run(files)
