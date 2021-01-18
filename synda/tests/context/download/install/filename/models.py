# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.task.file.models import get_rows_filtered_on_file_functional_id
from synda.tests.context.download.filename.models import Context as Base


class Context(Base):

    def __init__(self, filename="", folder="", expected_files_description=None, capsys=None):
        super(Context, self).__init__(
            filename=filename,
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
        )

    def validation_after_subcommand_execution(self):
        data = get_rows_filtered_on_file_functional_id(
            self.get_file().get_filename(),
        )

        assert len(data) == 1

        record = data[0]
        assert record['status'] == "waiting"


class TestEnvContext(Context):

    def validate_checksums(self):
        for file in self.expected_files:
            file.validate_checksum()
