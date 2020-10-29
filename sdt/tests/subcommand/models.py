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

from sdt.bin import synda


class SubCommand(object):

    def __init__(self, name, context, description=""):

        self.description = ""
        self.name = ""
        self.argv = []

        self.context = None

        self.init(name, context, description)

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
        return self.argv

    def init(self, name, context, description):
        self.name = name
        self.set_context(context)
        self.description = description

    def execute(self):

        self.context.pre_validation()

        sys.argv = self.get_argv()

        with pytest.raises(BaseException) as exception:
            synda.run()
        assert exception.value.code in [0, 1]

        # self.context.post_validation()
        # self.context.cleanup()
