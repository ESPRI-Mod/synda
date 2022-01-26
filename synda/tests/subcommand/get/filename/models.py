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
            context.get_parameters(),
        )

    def configure(self, dest_folder, filename, parameters):

        if parameters:
            argv = ['', self.name, "--dest_folder", dest_folder]
            for parameter in parameters:
                argv.append(parameter)
            self.set_argv(
                argv,
            )
        else:
            self.set_argv(
                ['', self.name, "--dest_folder", dest_folder, filename],
            )


class VerifyChecksumSubCommand(Base):

    def __init__(self, context, exceptions_codes=None):
        super(VerifyChecksumSubCommand, self).__init__(
            context,
            exceptions_codes=exceptions_codes,
            description="Optional parameters : --dest_folder --verify_checksum",
        )

        self.configure(
            context.get_file().get_folder(),
            context.get_file().get_filename(),
        )

    def configure(self, dest_folder, filename):

        self.set_argv(
            ['', self.name, "--verify_checksum", "--dest_folder", dest_folder, filename],
        )


class VerifyChecksumWithNetworkBandwidthTestSubCommand(Base):

    def __init__(self, context, exceptions_codes=None):
        super(VerifyChecksumWithNetworkBandwidthTestSubCommand, self).__init__(
            context,
            exceptions_codes=exceptions_codes,
            description="Optional parameters : --dest_folder --verify_checksum --network_bandwidth_test",
        )

        self.configure(
            context.get_file().get_folder(),
            context.get_file().get_filename(),
        )

    def configure(self, dest_folder, filename):

        self.set_argv(
            ['', self.name, "--verify_checksum", "--dest_folder", dest_folder, "--network_bandwidth_test", filename],
        )


class DestFolderSubCommand(Base):

    def __init__(self, context, exceptions_codes=None):
        super(DestFolderSubCommand, self).__init__(
            context,
            exceptions_codes=exceptions_codes,
            description="Optional parameter : only --dest_folder",
        )
        self.configure(
            context.get_file().get_folder(),
            context.get_file().get_filename(),
        )

    def configure(self, dest_folder, filename):

        self.set_argv(
            ['synda', self.name, "--dest_folder", dest_folder, filename],
        )
