# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import stat
from glob import glob
from shutil import rmtree
from shutil import copyfile

from sdt.bin import sdcfloader

from sdt.bin.constants import ST_HOME
from sdt.tests.constants import ST_HOME_TESTS

from sdt.tests.context.models import Context as Base


class Context(Base):

    def __init__(self, capsys=None):
        super(Context, self).__init__(capsys=capsys)

        self.initial_tests_mode_status_value = ""

        self.root = ST_HOME_TESTS
        self.conf_filenames = ["credentials.conf", "sdt.conf"]

        self.locations = dict(
            conf="",
            db="",
            data="",
            sandbox="",
            tmp="",
            log="",
            bin="",
        )

        # create tree root

        self.create_root()

        self.set_locations()

    def create_root(self):

        if not os.path.isdir(self.root):
            os.mkdir(self.root)
            os.chmod(self.root, 0o755)

    def set_locations(self):

        # create sub directories
        for subdirectory in self.locations.keys():
            self.locations[subdirectory] = os.path.join(
                self.root,
                subdirectory,
            )

    def get_sandbox_folder(self):
        return self.locations["sandbox"]

    def get_db_folder(self):
        return self.locations["db"]

    def activate_tests_mode(self):
        os.environ["ST_TESTS_MODE_STATUS"] = "activated"

    def restore_initial_tests_mode_status_value_if_necessary(self):
        if self.initial_tests_mode_status_value:
            os.environ["ST_TESTS_MODE_STATUS"] = self.initial_tests_mode_status_value

    def create_tree(self):

        # create sub directories
        for subdirectory in self.locations.keys():
            location = self.locations[subdirectory]
            if not os.path.isdir(location):
                os.mkdir(location)
                os.chmod(location, 0o755)

        self.copy_files()
        self.allow_scripts_execution()
        self.update_sdt_conf_file_contents()

    def reset(self):
        subdirectories = ["db", "sandbox", "tmp", "log"]
        for subdirectory in subdirectories:
            files_pattern = os.path.join(
                self.locations[subdirectory],
                "*.*",
            )
            for f in glob(files_pattern):
                os.remove(f)

    def allow_scripts_execution(self):

        subdirectory = "bin"
        files_pattern = os.path.join(
            self.locations[subdirectory],
            "*.*",
        )
        for src in glob(files_pattern):
            os.chmod(src, 0o755)

    def copy_files(self):
        subdirectories = ["bin", "conf"]
        for subdirectory in subdirectories:
            files_pattern = os.path.join(

                os.path.join(
                    ST_HOME,
                    subdirectory,
                ),
                "*.*",
            )

            for src in glob(files_pattern):

                dst = os.path.join(

                    self.locations[subdirectory],
                    os.path.basename(src),
                )
                copyfile(src, dst)

    def update_sdt_conf_file_contents(self):
        configuration_file = os.path.join(
            self.locations["conf"],
            "sdt.conf",
        )
        config = sdcfloader.load(configuration_file)

        config.set('core', 'default_path', self.root)

        subdirectories = ["selection", "db", "sandbox", "data"]
        for subdirectory in subdirectories:

            value = os.path.join(
                self.root,
                subdirectory,
            )
            config.set('core', '{}_path'.format(subdirectory), value)

        cfgfile = open(configuration_file,'w')
        config.write(cfgfile)
        cfgfile.close()

    def set_tests_mode(self):

        if "ST_TESTS_MODE_STATUS" in os.environ:
            self.initial_tests_mode_status_value = os.environ["ST_TESTS_MODE_STATUS"]

        self.activate_tests_mode()

    def delete_tree(self):
        if os.path.isdir(self.root):
            rmtree(self.root)

    def cleanup(self):
        self.reset()
