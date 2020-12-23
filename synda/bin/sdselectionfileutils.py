#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains selection file utils."""

import os
import argparse
import sdapp
import sdconfig

def find_selection_file(file):
    if os.path.isfile(file):
        # file found

        return file
    else:
        if '/' in file:
            # path

            # if we are here, path is incorrect.
            # we return the path 'as is'
            # (it will trigger an error message in the calling func)

            return file
        else:
            # filename

            # if we are here, we expect the file to be in the 'selection' folder

            return "%s/%s"%(sdconfig.selection_folder,file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
