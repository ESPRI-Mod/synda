# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from sdt.tests.context.models import Context as Base


class Context(Base):

    def __init__(self, selection_file, folder, expected_files_description=None, capsys=False):
        super(Context, self).__init__(
            folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
        )
        self.selection_file = ""
        self.selection_file = selection_file

    def get_selection_file(self):
        return self.selection_file


class TestEnvContext(Context):

    def validate_checksums(self):
        for file in self.expected_files:
            file.validate_checksum()
