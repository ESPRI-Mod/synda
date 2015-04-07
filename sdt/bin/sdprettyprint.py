#!/usr/bin/python -u
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

import sdapp
from sdtypes import File

def run(files):
    
    pretty_label={'done':'installed'} # this is have a listing like dpkg/apt-get

    for file in files:
        f=File(**file)
        print "%-12s %s"%(pretty_label.get(f.status,f.status),f.filename)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('path')
	args = parser.parse_args()
