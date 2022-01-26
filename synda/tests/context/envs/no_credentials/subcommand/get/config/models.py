# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.context.download.filename.models import Context as Base
from synda.source.process.subcommand.get.models import CONFIG_CREDENTIALS_ERROR


class Context(Base):

    def __init__(self, filename="", folder="", expected_files_description=None, capsys=None, validate=True):
        super(Context, self).__init__(
            filename=filename,
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
            validate=validate,
        )

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        assert CONFIG_CREDENTIALS_ERROR in captured.err
