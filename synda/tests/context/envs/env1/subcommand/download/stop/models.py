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

    def __init__(self, filename="", folder="", expected_files_description=None, capsys=None, validate=True):
        super(Context, self).__init__(
            filename=filename,
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
            validate=validate,
        )

    # def validation_after_subcommand_execution(self):
    #     from synda.source.db.task.file.models import get_rows_filtered_on_file_functional_id as get_record
    #     from synda.source.config.file.downloading.models import Config as Filedownloading
    #
    #     fd = Filedownloading()
    #     assert not fd.process_is_active()
    #
    #     file_functional_id = DB_CONTEXT["files"][0]["functional_id"]
    #     record = get_record(file_functional_id)
    #     print(record)
    #     assert record["status"] == "waiting"
