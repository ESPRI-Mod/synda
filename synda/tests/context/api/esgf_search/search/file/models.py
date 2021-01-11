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

from synda.tests.context.api.esgf_search.search.constants import CONTEXT


class Context(Base):

    def __init__(self):

        # settings

        positional = CONTEXT["env"]["default"]["user_cases"]["atmos"]["arguments"]["positional"]
        optional = CONTEXT["env"]["default"]["user_cases"]["atmos"]["arguments"]["optional"] + \
                   ["--{}".format(API_TYPE_FILE.lower())]

        arguments = dict(
            positional=positional,
            optional=optional,
        )
        Base.__init__(self, API_TYPE_FILE, arguments=arguments)

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()

        expected_filenames = CONTEXT["env"]["default"]["user_cases"]["atmos"]["expected"][self.get_api_type()]
        expected_filename = expected_filenames[0]
        assert expected_filename in captured.out
