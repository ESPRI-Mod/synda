# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.context.envs.env1.subcommand.api.esgf_search.models import Context as Base

from synda.source.config.api.esgf_search.constants import TYPE_DATASET as API_TYPE_DATASET

from synda.tests.context.envs.env1.constants import DB
from synda.tests.context.envs.env1.subcommand.api.esgf_search.search.constants \
    import CONTEXT as SEARCH_SUBCOMMAND_CONTEXT


class Context(Base):

    def __init__(self):

        # initializations

        positional = SEARCH_SUBCOMMAND_CONTEXT["arguments"]["positional"]
        optional = SEARCH_SUBCOMMAND_CONTEXT["arguments"]["optional"] + ["--{}".format(API_TYPE_DATASET.lower())]

        arguments = dict(
            positional=positional,
            optional=optional,
        )

        Base.__init__(self, API_TYPE_DATASET, arguments=arguments)

        # settings

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()

        expected_datasets = DB["datasets"]
        for dataset in expected_datasets:
            assert dataset in captured.out
