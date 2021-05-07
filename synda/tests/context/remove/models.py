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
        self.dataset = ENVS["installed"]["env"]["dataset"]

    def get_dataset(self):
        return self.dataset

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()

        local_path = ENVS["installed"]["env"]["local_path"]
        assert "1 file(s) will be removed." in captured.err
        assert not os.path.isfile(local_path)
