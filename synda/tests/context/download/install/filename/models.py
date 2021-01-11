# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.db.connection.cursor.models import Cursor
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
        cursor = Cursor()
        sql_request = "SELECT status FROM file WHERE file_functional_id = '{}';".format(
            self.get_file().get_filename(),
        )

        cursor.execute(sql_request)
        data = cursor.get_data()
        cursor.close()

        assert len(data) == 1

        record = data[0]
        assert record['status'] == "waiting"


class TestEnvContext(Context):

    def validate_checksums(self):
        for file in self.expected_files:
            file.validate_checksum()
