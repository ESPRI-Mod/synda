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
from synda.tests.stderr import VERIFY_CHECKSUM_KO, VERIFY_CHECKSUM_OK


class Context(Base):

    def __init__(self, folder="", expected_files_description=None, capsys=None):
        super(Context, self).__init__(
            capsys=capsys,
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
        return self.expected_files_description

    # def at_least_one_expected_file_exists(self):
    #     for file in self.expected_files_description.get_data():
    #         if file.exists():
    #             return True
    #     return False
    #
    def all_expected_file_exists(self):
        for expected_file in self.expected_files_description.get_data():
            if not expected_file.exists():
                return False
        return True

    def remove_all_expected_files(self):
        for file in self.expected_files:
            if file.exists():
                os.remove(
                    file.get_full_filename(),
                )

    def validate_downloaded_files(self):
        assert self.all_expected_file_exists()

    # def validate_checksums(self):
    #     captured = self.get_capsys().readouterr()
    #     assert VERIFY_CHECKSUM_OK in captured.err
    #     assert VERIFY_CHECKSUM_KO not in captured.err
    #
    def validation_after_subcommand_execution(self):
        self.validate_downloaded_files()
        # self.validate_checksums()
