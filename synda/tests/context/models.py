# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################


class Context(object):

    def __init__(self, arguments=None, capsys=None, validate=True):

        # initialization
        self.arguments = dict(
            positional=[],
            optional=[],
        )
        # During test execution any output sent to stdout and stderr is captured
        self.capsys = None

        # After test execution, a context post process can be executed to validate the test
        # It may be disabled with this property
        self.validate = False

        # settings

        self.capsys = capsys
        self.arguments = arguments
        self.validate = validate

    def get_arguments(self):
        return self.arguments

    def get_optional_arguments(self):
        return self.arguments["optional"]

    def get_positional_arguments(self):
        return self.arguments["positional"]

    def get_capsys(self):
        return self.capsys

    def set_capsys(self, capsys):
        self.capsys = capsys

    def controls_before_subcommand_execution(self):
        pass

    def validation_after_subcommand_execution(self):
        pass
