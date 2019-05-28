#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains sdconfig utils."""

import os
import sdcfbuilder
import sdtools

class Paths(object):
    def add_common_paths(self):
        self.default_folder_default_path=os.path.join(self.conf_folder,"default")
        self.configuration_file=os.path.join(self.conf_folder,"sdt.conf")
        self.credential_file=os.path.join(self.conf_folder,"credentials.conf")

class PackageSystemPaths(Paths):
    def __init__(self):
        self.bin_folder='/usr/share/python/synda/sdt/bin'
        self.tmp_folder='/var/tmp/synda/sdt'
        self.log_folder='/var/log/synda/sdt'
        self.conf_folder='/etc/synda/sdt'

        self.default_selection_folder='/etc/synda/sdt/selection'
        self.default_db_folder='/var/lib/synda/sdt'
        self.default_data_folder='/srv/synda/sdt/data'
        self.default_sandbox_folder='/srv/synda/sdt/sandbox'

        self.add_common_paths()

    def create_tree():
        pass # nothing to do as done when installing from package

class SourceInstallPaths(Paths):
    def __init__(self,root_folder):
        self.bin_folder="%s/bin"%root_folder
        self.tmp_folder="%s/tmp"%root_folder
        self.log_folder="%s/log"%root_folder
        self.conf_folder="%s/conf"%root_folder

        self.default_selection_folder="%s/selection"%root_folder
        self.default_db_folder="%s/db"%root_folder
        self.default_data_folder="%s/data"%root_folder
        self.default_sandbox_folder="%s/sandbox"%root_folder

        self.add_common_paths()

    def create_tree():
        pass # nothing to do as done when installing from source

class UserPaths(SourceInstallPaths):
    """This class contains 'user instance' paths.

    Notes
        -
            'user instance' means a SDT environment specific to each user (no
            centralization, each user has his own selection files, his own local
            database, his own X.509 certificate, his own data files,
            etc.. Only binaries are shared)
        -
            Currently, there is only one daemon per machine, but this may change in the
            future (i.e. maybe remove sysv/systemd service and allow one daemon per user).
            TAG43J2K253J43
    """

    def create_tree(self):

        # create folder
        li=[self.bin_folder,
            self.tmp_folder,
            self.log_folder,
            self.conf_folder,

            self.default_selection_folder,
            self.default_db_folder,
            self.default_data_folder,
            self.default_sandbox_folder]

        sdtools.mkdir(li)


        # create USER credential sample file
        if not os.path.exists(self.credential_file):
            sdcfbuilder.create_credential_file_sample(self.credential_file)
            os.chmod(self.credential_file,0600)

        # create USER configuration sample file
        if not os.path.exists(self.configuration_file):
            sdcfbuilder.create_configuration_file_sample(self.configuration_file)
            os.chmod(self.configuration_file,0644)
