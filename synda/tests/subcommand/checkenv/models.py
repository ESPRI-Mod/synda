# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.env.manager import Manager
from synda.tests.subcommand.models import SubCommand as Base


class SubCommand(Base):

    def __init__(self, context, exceptions_codes=None):
        super(SubCommand, self).__init__(
            "check-env",
            context,
            exceptions_codes=exceptions_codes,
            description="Check Synda Environment",
        )

    def execute(self):

        self.context.controls_before_subcommand_execution()

        env_manager = Manager()
        env_manager.check(interactive_mode=False)

        if self.context.validate:
            self.context.validation_after_subcommand_execution()
