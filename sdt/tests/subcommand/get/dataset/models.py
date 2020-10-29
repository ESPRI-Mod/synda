# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.tests.subcommand.get.models import SubCommand as Base


class ConfigFileSubCommand(Base):

    def __init__(self, context):
        super(ConfigFileSubCommand, self).__init__(
            context,
            description="Download configuration is given by file",
        )

        self.configure(
            context.get_dataset(),
        )

    def configure(self, dataset):

        self.set_argv(
            ['synda', self.name, "--verify_checksum", dataset],
        )
