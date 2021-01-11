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
            "version",
            context,
            exceptions_codes=exceptions_codes,
            description="List all versions of a dataset",
        )

        self.configure(
            context.get_dataset(),
        )

    def configure(self, dataset):

        self.set_argv(
            ['synda', self.name, dataset],
        )
