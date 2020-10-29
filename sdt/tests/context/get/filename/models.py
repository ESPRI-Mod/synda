# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from sdt.tests.context.models import Context as Base
from sdt.tests.file.models import File


class Context(Base):

    def __init__(self, filename, folder, expected_files_description=None, capsys=None):
        super(Context, self).__init__(
            folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
        )
        self.file = File(filename, folder)

    def get_file(self):
        return self.file

    def remove_all_expected_files(self):
        if self.file:
            os.remove(
                self.file.get_full_filename(),
            )

        super(Context, self).remove_all_expected_files()


class TestEnvContext(Context):

    def validate_checksums(self):
        for file in self.expected_files:
            file.validate_checksum()
