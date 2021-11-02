# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.context.models import Context as Base
from synda.tests.context.envs.env3.constants import ENV


class Context(Base):

    def __init__(self, capsys=None, validate=True):
        super(Context, self).__init__(
            capsys=capsys,
            validate=validate,
        )

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        for file_selection in ENV["files_selection"]:
            assert file_selection in captured.out
