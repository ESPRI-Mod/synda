# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from synda.tests.context.models import Context as Base
from synda.tests.context.remove.constants import ENVS


class Context(Base):

    def __init__(self):

        # initializations

        arguments = dict(
            positional=[],
            optional=[],
        )
        Base.__init__(self, arguments=arguments)

        # settings
        self.selection_file = ENVS["installed"]["env"]["selection_file"]

    def get_selection_file(self):
        return self.selection_file

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()

        expected_removed_data_file = ENVS["installed"]["env"]["data_file"]
        assert "1 file(s) will be removed." in captured.err
        assert not os.path.isfile(expected_removed_data_file)
