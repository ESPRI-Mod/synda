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

from synda.tests.context.api.esgf_search.search.constants import CONTEXT
from synda.source.config.process.download.dataset.constants import DATASET_STATUS_NEW


class Context(Base):

    def __init__(self):

        # settings

        positional = CONTEXT["env"]["default"]["user_cases"]["atmos"]["arguments"]["positional"]
        optional = CONTEXT["env"]["default"]["user_cases"]["atmos"]["arguments"]["optional"] + \
                   ["--{}".format(API_TYPE_DATASET.lower())]

        arguments = dict(
            positional=positional,
            optional=optional,
        )
        Base.__init__(self, API_TYPE_DATASET, arguments=arguments)

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()

        expected_datasets = CONTEXT["env"]["default"]["user_cases"]["atmos"]["expected"][self.get_api_type()]
        expected_dataset = expected_datasets[0]
        assert DATASET_STATUS_NEW in captured.out
        assert expected_dataset in captured.out
