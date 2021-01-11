# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from shutil import rmtree


def delete_dirs(target):
    if os.path.isdir(target):
        rmtree(target)


def create_dir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)
        os.chmod(directory, 0o755)


def has_environment_variable(var_name):
    checked = False
    if var_name in os.environ.keys():
        checked = True
    return checked
