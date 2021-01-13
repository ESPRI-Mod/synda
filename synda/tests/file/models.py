# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.file.checksum.models import Checksum


class File(object):

    def __init__(self, name, folder, checksum=None, create_folder=False):
        self.name = ""
        self.folder = ""
        self.created_folder = False
        self.checksum = Checksum(
            "sha256",
            "",
        )

        self.init(name, folder, checksum, create_folder)

    def init(self, name, folder, checksum, create_folder):
        self.name = name
        self.folder = folder
        self.checksum = checksum

        if create_folder:
            self.mkdir()

    def mkdir(self):
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
            if os.path.isdir(self.folder):
                self.created_folder = True

    def get_checksum(self):
        return self.checksum

    def get_calculated_checksum(self):
        if self.exists():
            self.checksum.set_calculated_value(self.get_full_filename())
        return self.checksum


    def validate_checksum(self):
        if self.exists():
            self.checksum.validate(self.get_full_filename())

    def get_filename(self):
        return self.name

    def get_folder(self):
        return self.folder

    def get_full_filename(self):
        return os.path.join(
            self.folder,
            self.name,
        )

    def exists(self):
        return os.path.exists(
            self.get_full_filename(),
        )


class Selection(File):

    def __init__(self, name, folder):
        super(Selection, self).__init__(name, folder)
