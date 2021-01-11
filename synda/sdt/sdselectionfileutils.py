#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from synda.source.config.path.tree.models import Config as TreePath


def find_selection_file(_file):

    if os.path.isfile(_file):
        # file found

        return _file
    else:
        if '/' in _file:
            # path

            # if we are here, path is incorrect.
            # we return the path 'as is'
            # (it will trigger an error message in the calling func)

            return _file
        else:
            # filename

            # if we are here, we expect the file to be in the 'selection' folder
            selection_folder = TreePath().get("selection")
            return "%s/%s" % (selection_folder, _file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
