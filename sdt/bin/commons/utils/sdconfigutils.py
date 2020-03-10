#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved€
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains sdconfig utils."""

import os
from sdt.bin.commons.utils import sdcfbuilder
from sdt.bin.commons.utils import sdtools


class SourceInstallPaths(object):
    def __init__(self, root_folder):
        self.bin_folder = os.path.join(root_folder, 'bin')
        self.tmp_folder = os.path.join(root_folder, 'tmp')
        self.log_folder = os.path.join(root_folder, 'log')
        self.conf_folder = os.path.join(root_folder, 'conf')

        self.default_selection_folder = os.path.join(root_folder, 'selection')
        self.default_db_folder = os.path.join(root_folder, 'db')
        self.default_data_folder = os.path.join(root_folder, 'data')
        self.default_sandbox_folder = os.path.join(root_folder, 'sandbox')
        self.default_folder_default_path = os.path.join(self.conf_folder, "default")
        self.configuration_file = os.path.join(self.conf_folder, "sdt.conf")
        self.credential_file = os.path.join(self.conf_folder, "credentials.conf")
