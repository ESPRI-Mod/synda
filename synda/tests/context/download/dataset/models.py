# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.tests.context.download.models import Context as Base


class Context(Base):

    def __init__(self, dataset="", folder="", expected_files_description=None, capsys=None):
        super(Context, self).__init__(
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
        )
        self.dataset = ""
        self.dataset = dataset

    def get_dataset(self):
        return self.dataset

    def set_dataset(self, dataset, dest_folder=""):
        self.dataset = dataset
        self.set_folder(dest_folder)


class TestEnvContext(Context):

    def validate_checksums(self):
        for file in self.expected_files_description:
            file.file_checksum()
