#!/usr/bin/python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'sandbox' folder related routines."""
import os
import argparse

from synda.source.config.path.tree.models import Config as TreePath

sandbox_folder = TreePath().get("sandbox")


def file_exists(filename):
    path = os.path.join(
        sandbox_folder,
        filename,
    )

    return os.path.isfile(path)


def get_file_path(filename):
    path = os.path.join(
        sandbox_folder,
        filename,
    )

    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
