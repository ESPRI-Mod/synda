# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.context.download.models import Context as Base
from synda.tests.file.models import File


class BasicContext(Base):

    def __init__(self, filename="", folder="", parameters =None, expected_files_description=None, capsys=None, validate=True):
        super(BasicContext, self).__init__(
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
            validate=validate,
        )

        self.parameters = []
        self.file = None
        if filename and folder:
            self.file = File(filename, folder)

    def set_parameters(self, value):
        self.parameters = value

    def get_parameters(self):
        return self.parameters

    def set_file(self, filename, dest_folder=""):
        if dest_folder:
            self.folder = dest_folder
        else:
            dest_folder = self.folder

        if os.path.exists(dest_folder):
            self.file = File(filename, dest_folder)

    def get_file(self):
        return self.file

    def validation_after_subcommand_execution(self):
        self.validate_no_checksums()


class VerifyChecksumContext(BasicContext):

    def __init__(self, filename="", folder="", expected_files_description=None, capsys=None):
        super(VerifyChecksumContext, self).__init__(
            filename=filename,
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
        )

    def validation_after_subcommand_execution(self):
        self.validate_checksums()


class VerifyChecksumWithNetworkBandwidthTestContext(BasicContext):

    def __init__(self, filename="", folder="", expected_files_description=None, capsys=None):
        super(VerifyChecksumWithNetworkBandwidthTestContext, self).__init__(
            filename=filename,
            folder=folder,
            expected_files_description=expected_files_description,
            capsys=capsys,
        )

    def validation_after_subcommand_execution(self):
        self.verify_checksum_error()
