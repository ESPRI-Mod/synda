# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.subcommand.get.models import SubCommand as Base


class SubCommand(Base):

    def __init__(self, context, exceptions_codes=None):
        super(SubCommand, self).__init__(
            context,
            exceptions_codes=exceptions_codes,
            description="No optional parameter",
        )

        self.configure(
            context.get_file().get_folder(),
            context.get_file().get_filename(),
        )

    def configure(self, dest_folder, filename):

        self.set_argv(
            [
                '',
                 self.name,
                 "--dest_folder",
                 dest_folder,
                "--openid",
                'https://esgf-node.ipsl.fr/esgf-idp/openid/foo',
                "--password",
                'foobar',
                filename,
             ],
        )
