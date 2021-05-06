# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.identifier import Identifier


class Process(Identifier):

    def __init__(self, name, authority, is_environment_required=False, arguments=None, exceptions_codes=None):
        super(Process, self).__init__(name)

        # initializations
        self.authority = None
        self.is_environment_required = False
        self.exceptions_codes = []

        self.arguments = dict(
            positional=[],
            optional=[],
        )

        # settings
        self.authority = authority
        self.is_environment_required = is_environment_required
        self.arguments = arguments
        self.exceptions_codes = exceptions_codes

    def set_exceptions_codes(self, exceptions_codes):
        self.exceptions_codes = exceptions_codes

    def set_arguments(self, arguments):
        self.arguments = arguments

    def get_authority(self):
        return self.authority

    def get_arguments(self):
        return self.arguments

    def get_subcommand_name(self):
        return self.get_identifier()

    def get_optional_arguments(self):
        return self.arguments["optional"]

    def get_positional_arguments(self):
        return self.arguments["positional"]

    def get_sys_argv(self):
        argv = ['synda', self.get_subcommand_name()]
        argv.extend(
            [p for p in self.get_arguments()["positional"]]
        )
        argv.extend(
            [p for p in self.get_arguments()["optional"]]
        )
        return argv
