# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from sdt.tests.file.models import File
from sdt.tests.stderr import VERIFY_CHECKSUM_KO


class Context(object):

    def __init__(self, folder, expected_files_description=None, capsys=None):

        self.expected_files = []
        self.folder = ""
        self.created_folder = False

        # During test execution any output sent to stdout and stderr is captured
        self.capsys = None

        self.folder = folder
        self.capsys = capsys

        if expected_files_description:
            for filename, checksum in expected_files_description.items():
                self.expected_files.append(
                    File(
                        filename,
                        folder,
                        checksum=checksum,
                    ),
                )

        if not os.path.isdir(self.folder):
            self.mkdir()

    def get_folder(self):
        return self.folder

    def mkdir(self):
        os.mkdir(self.folder)
        if os.path.isdir(self.folder):
            self.created_folder = True

    def get_capsys(self):
        return self.capsys

    def get_expected_files(self):
        return self.expected_files

    def at_least_one_expected_file_exists(self):
        for file in self.expected_files:
            if file.exists():
                return True
        return False

    def all_expected_file_exists(self):
        for file in self.expected_files:
            if not file.exists():
                return False
        return True

    def remove_all_expected_files(self):
        for file in self.expected_files:
            if file.exists():
                os.remove(
                    file.get_full_filename(),
                )

    def pre_validation(self):
        assert not self.at_least_one_expected_file_exists()

    def validate_downloaded_files(self):
        assert self.all_expected_file_exists()

    def validate_checksums(self):
        captured = self.get_capsys().readouterr()
        assert VERIFY_CHECKSUM_KO not in captured.err

    def post_validation(self):
        self.validate_downloaded_files()
        self.validate_checksums()

    def cleanup(self):
        self.remove_all_expected_files()
        if self.created_folder:
            os.rmdir(self.folder)
