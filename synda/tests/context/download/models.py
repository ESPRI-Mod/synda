# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.tests.context.models import Context as Base
from synda.source.process.asynchronous.download.subcommand.get.task.aiohttp.models import VALIDATED_CHECKSUM_MESSAGE_TEMPLATE
from synda.source.process.subcommand.get.constants import VERIFY_CHECKSUM_ERROR


class Context(Base):

    def __init__(self, folder="", expected_files_description=None, capsys=None, validate=True):
        super(Context, self).__init__(
            capsys=capsys,
            validate=validate,
        )
        self.expected_files_description = []
        self.folder = ""

        if folder:
            self.set_folder(folder)
        else:
            self.folder = os.getcwd()

        if expected_files_description:
            self.set_expected_files_description(expected_files_description)

    def set_expected_files_description(self, expected_files_description):
        self.expected_files_description = expected_files_description

    def set_folder(self, folder):
        self.folder = folder

    def get_folder(self):
        return self.folder

    def get_expected_files(self):
        return self.expected_files_description.get_data()

    # def at_least_one_expected_file_exists(self):
    #     for file in self.expected_files_description.get_data():
    #         if file.exists():
    #             return True
    #     return False
    #
    def all_expected_file_exists(self):
        for expected_file in self.get_expected_files():
            if not expected_file.exists():
                return False
        return True

    def remove_all_expected_files(self):
        for file in self.get_expected_files():
            if file.exists():
                os.remove(
                    file.get_full_filename(),
                )

    def validate_downloaded_files(self):
        assert self.all_expected_file_exists()

    def verify_checksum_error(self):
        # network_bandwidth_test
        captured = self.get_capsys().readouterr()
        assert VERIFY_CHECKSUM_ERROR in captured.err

    def validate_no_checksums(self):
        from synda.source.process.asynchronous.download.subcommand.get.task.aiohttp.models import NO_CHECKSUM_SUCCESS_MESSAGE_TEMPLATE
        captured = self.get_capsys().readouterr()
        for file in self.get_expected_files():
            assert NO_CHECKSUM_SUCCESS_MESSAGE_TEMPLATE.format(
                file.get_full_filename(),
            ) in captured.out

    def validate_checksums(self):
        captured = self.get_capsys().readouterr()
        for file in self.get_expected_files():
            assert VALIDATED_CHECKSUM_MESSAGE_TEMPLATE.format(
                file.get_full_filename(),
            ) in captured.out

    def validation_after_subcommand_execution(self):
        self.validate_downloaded_files()

    # def validate_checksums(self):
    #     for file in self.expected_files_description:
    #         file.validate_checksum()
