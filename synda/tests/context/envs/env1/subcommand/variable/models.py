# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.context.envs.env1.constants import ENV
from synda.tests.context.models import Context as Base
from synda.tests.context.envs.env1.constants import VARIABLE


class Context(Base):

    def __init__(self, variable, capsys=None, validate=True):
        super(Context, self).__init__(
            capsys=capsys,
            validate=validate,
        )
        self.variable = variable

    def get_variable(self):
        return self.variable

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        if not self.variable:
            variables = set(captured.out.split("\n"))
            variables.remove("")
            assert len(variables) == ENV["metrics"]["nb_variables"]
        else:
            assert VARIABLE[self.variable] in captured.out
