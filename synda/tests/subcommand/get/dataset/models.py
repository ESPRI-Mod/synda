# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.subcommand.get.models import SubCommand as Base


class DestFolderSubCommand(Base):

    def __init__(self, context, exceptions_codes=None):
        super(DestFolderSubCommand, self).__init__(
            context,
            exceptions_codes=exceptions_codes,
            description="Download configuration is given by command line",
        )

        self.configure(
            context.get_folder(),
            context.get_dataset(),
        )

    def configure(self, dest_folder, dataset):

        self.set_argv(
            ['synda', self.name, "--verify_checksum", "--dest_folder", dest_folder, dataset],
        )
