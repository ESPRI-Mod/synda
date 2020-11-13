# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.tests.subcommand.get.models import SubCommand as Base


class SelectionGetSubCommand(Base):

    def __init__(self, context, exceptions_codes=None):
        super(SelectionGetSubCommand, self).__init__(
            context,
            exceptions_codes=exceptions_codes,
            description="Download configuration driven by selection file",
        )

        self.configure(
            context.get_folder(),
            context.get_selection_file(),
        )

    def configure(self, dest_folder, selection_file):

        self.set_argv(
            ['', self.name, "--verify_checksum", "--dest_folder", dest_folder, "--selection_file", selection_file],
        )
