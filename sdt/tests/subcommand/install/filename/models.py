# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.tests.subcommand.install.models import SubCommand as Base
from sdt.tests.exceptions import MethodNotImplemented


class SubCommand(Base):

    def __init__(self, context):
        super(SubCommand, self).__init__(
            context,
            description="Download with install subcommand, configuration is given by file",
        )
        self.configure(
            context.get_file().get_filename(),
        )

    def configure(self, filename):

        self.set_argv(
            ['synda', self.name, "--yes", filename],
        )
