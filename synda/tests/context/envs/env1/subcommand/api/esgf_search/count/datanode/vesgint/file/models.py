# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.context.envs.env1.constants import ENV
from synda.tests.context.envs.env1.subcommand.api.esgf_search.models import Context as Base
from synda.source.config.api.esgf_search.constants import TYPE_FILE as API_TYPE_FILE

from synda.source.config.process.count.messages import FILE_FOUND_TEMPLATE as EXPECTED_MESSAGE
from synda.tests.context.envs.env1.subcommand.api.esgf_search.count.constants \
    import CONTEXT as COUNT_SUBCOMMAND_CONTEXT


class Context(Base):

    def __init__(self):

        # initializations

        positional = COUNT_SUBCOMMAND_CONTEXT["arguments"]["positional"]
        optional = COUNT_SUBCOMMAND_CONTEXT["arguments"]["optional"] + ["--{}".format(API_TYPE_FILE.lower())]

        arguments = dict(
            positional=positional,
            optional=optional,
        )
        Base.__init__(self, API_TYPE_FILE, arguments=arguments)

        # settings

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()

        expected_count = ENV["metrics"]["nb_files"]
        assert EXPECTED_MESSAGE.format(
            expected_count,
        ) in captured.out
