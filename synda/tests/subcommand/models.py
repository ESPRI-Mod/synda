# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sys
import pytest

from synda.sdt import main as synda


def get_list(options):
    """

    :param options: list of dictionaries to be reformatted as list [key1, value1, key2, value2...]
    examples
        {"realm" : "atmos"}
        {"atmos": None}
    :return:
    """
    result = []
    for option in options:
        if isinstance(option, dict):
            for key, value in list(option.items()):
                result.append(key)
                if value is not None:
                    result.append(str(value))
        elif isinstance(option, str):
            result.append(option)
    return result


class SubCommand(object):

    def __init__(self, name, context, exceptions_codes=None, description=""):

        self.description = ""
        self.name = ""
        self.argv = []
        self.exceptions_codes = []

        self.context = None

        self.init(name, context, description, exceptions_codes)

    def set_context(self, context):
        """
            Test objective is to compare an expected result with an observed one
            expected property must be set to an object that represents the 'expected result'

            The expected object must have a method to compare itself with the observed object
        """
        self.context = context

    def get_context(self):
        return self.context

    def set_argv(self, value):
        self.argv = value

    def get_argv(self):
        if self.argv:
            argv = self.argv
        else:
            argv = ['synda', self.name]
            argv.extend(
                get_list(self.context.get_arguments()["positional"]),
            )
            argv.extend(
                get_list(self.context.get_arguments()["optional"]),
            )
        return argv

    def init(self, name, context, description, exceptions_codes):
        self.name = name
        self.set_context(context)
        self.description = description
        self.exceptions_codes = exceptions_codes

    def execute(self):

        self.context.controls_before_subcommand_execution()

        sys.argv = self.get_argv()

        # synda.run()

        with pytest.raises(BaseException) as exception:
            synda.run()

        assert exception.value.code in self.exceptions_codes

        if isinstance(exception.value.code, int):
            if exception.value.code in [0, 1]:
                self.context.validation_after_subcommand_execution()
