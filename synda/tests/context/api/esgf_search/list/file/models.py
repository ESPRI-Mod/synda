# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.tests.context.api.esgf_search.models import Context as Base

from synda.source.config.api.esgf_search.constants import TYPE_FILE as API_TYPE_FILE

from synda.tests.context.api.esgf_search.list.constants import ENVS
from synda.source.config.process.download.constants import TRANSFER_STATUS_DONE


class Context(Base):

    def __init__(self):

        # initializations

        arguments = dict(
            positional=[],
            optional=[
                "--{}".format(
                    API_TYPE_FILE.lower(),
                ),
            ],
        )
        Base.__init__(self, API_TYPE_FILE, arguments=arguments)

        # settings

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()

        assert TRANSFER_STATUS_DONE in captured.out

        expected_filenames = ENVS["installed"]["env"]["expected"][self.get_api_type()]
        for filename in expected_filenames:
            assert filename in captured.out
