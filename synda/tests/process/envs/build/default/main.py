# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 1 / Create all the components required to build a new synda user workspace environment
 2 / Create the .tar file
"""
from synda.source.config.env.build.constants import TREE_DIRECTORY as BUILD_TREE_DIRECTORY

from synda.source.config.file.env.models import Config as EnvFile
from synda.source.process.env.build.models import Process


if __name__ == '__main__':

    process = Process(
        build_tree_location=BUILD_TREE_DIRECTORY,
        env_file_name=EnvFile().filename,
        env_file_destination=EnvFile().get(),
    )
    process.process()
