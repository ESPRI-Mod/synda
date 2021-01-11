# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.context.api.esgf_search.models import Context as Base

from synda.source.config.api.esgf_search.constants import TYPE_DATASET as API_TYPE_DATASET

from synda.tests.context.api.esgf_search.list.constants import ENVS
from synda.source.config.process.download.dataset.constants import DATASET_STATUS_COMPLETE


class Context(Base):

    def __init__(self):

        # initializations

        arguments = dict(
            positional=[],
            optional=[
                "--{}".format(
                    API_TYPE_DATASET.lower(),
                ),
            ],
        )
        Base.__init__(self, API_TYPE_DATASET, arguments=arguments)

        # settings

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()

        expected_datasets = ENVS["installed"]["env1"]["expected"][self.get_api_type()]
        expected_dataset = expected_datasets[0]
        assert DATASET_STATUS_COMPLETE in captured.out
        assert expected_dataset in captured.out
