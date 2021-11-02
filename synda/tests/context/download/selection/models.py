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

    def __init__(self, selection_file="", folder="", expected_files_description=None, capsys=False):
        super(Context, self).__init__(
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
        )
        self.selection_file = ""
        self.selection_file = selection_file

    def get_selection_file(self):
        return self.selection_file

    def set_selection_file(self, value):
        self.selection_file = value


class TestEnvContext(Context):

    def validate_checksums(self):
        for file in self.expected_files_description:
            file.validate_checksum()
