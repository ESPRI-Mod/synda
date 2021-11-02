# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from synda.tests.tests.constants import DATA_HOME_TESTS
from synda.tests.context.download.filename.models import Context as Base
from synda.tests.context.envs.env1.constants import DB as DB_CONTEXT


class Context(Base):

    def __init__(self, filename="", folder="", expected_files_description=None, capsys=None):
        super(Context, self).__init__(
            filename=filename,
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
        )

    def validation_after_subcommand_execution(self):
        from synda.source.db.task.file.models import get_rows_filtered_on_file_functional_id as get_record
        file_functional_id = DB_CONTEXT["files"][0]["functional_id"]

        record = get_record(file_functional_id)
        assert record["status"] == "done"

        observed_file_size = 0
        local_path = DB_CONTEXT["files"][0]["local_path"]
        full_filename = os.path.join(
            DATA_HOME_TESTS,
            local_path,
        )
        if os.path.isfile(full_filename):
            observed_file_size = os.path.getsize(full_filename)

        expected_file_size = record["size"]
        assert observed_file_size == expected_file_size
