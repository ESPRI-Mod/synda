# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.subcommand.models import SubCommand as Base


class SubCommand(Base):

    def __init__(self, context, exceptions_codes=None):
        super(SubCommand, self).__init__(
            "remove",
            context,
            exceptions_codes=exceptions_codes,
            description="Remove",
        )
        self.configure(
            context.get_selection_file(),
        )

    def configure(self, selection_file):

        self.set_argv(
            ['synda', self.name, "--yes", "--selection_file", selection_file],
        )
