# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
import os
import tarfile
from glob import glob
from shutil import copyfile
from shutil import move


from synda.source.utils import create_dir
from synda.source.utils import delete_dirs

from synda.source.identifier import Identifier

from synda.source.config.env.build.constants import DIRECTORY as BUILD_DIRECTORY

from synda.source.config.file.db.constants import FILENAME as DEFAULT_DB_FILENAME
from synda.source.db.connection.dao.create.request import Request as CreateDBRequest

from synda.source.config.file.env.constants import SUB_DIRECTORIES as ENV_SUB_DIRECTORIES

from synda.source.config.file.internal.constants import FILENAME as INTERNAL_FILENAME
from synda.source.config.file.internal.dao.create.models import Create as CreateInternal

from synda.source.config.file.user.preferences.constants import FILENAME as PREFERENCES_FILENAME
from synda.source.config.file.user.preferences.dao.create.models import Create as CreatePreferences

from synda.source.config.file.user.credentials.constants import FILENAME as CREDENTIALS_FILENAME
from synda.source.config.file.user.credentials.dao.create.models import Create as CreateCredentials

from synda.source.process.env.build.constants import IDENTIFIER

DEFAULT_SELECTION_FILE_DIR = os.path.join(*[BUILD_DIRECTORY, "conf", 'default'])
SELECTION_SAMPLE_DIR = os.path.join(*[BUILD_DIRECTORY, "selection", 'sample'])
BIN_DIR = os.path.join(*[BUILD_DIRECTORY, "bin"])


def create_tree_tar_file(build_location, tar_filename, tar_file_destination):
    # go to the requested build directory
    current_dir = os.getcwd()
    os.chdir(build_location)
    # open tar file that will contain the environment sub directories
    tar = tarfile.open(tar_filename, "w:gz")
    for directory in ENV_SUB_DIRECTORIES:
        tar.add(directory)
    tar.close()

    # move raise an error if destination already exists
    full_filename = os.path.join(
        tar_file_destination,
        tar_filename,
    )
    if os.path.exists(full_filename):
        os.remove(full_filename)

    move(
        tar_filename,
        tar_file_destination,
    )

    os.chdir(current_dir)

    return True if os.path.isfile(tar_file_destination) else False


class Process(Identifier):

    def __init__(
            self,
            build_tree_location,
            env_file_name,
            env_file_destination,
    ):
        Identifier.__init__(self, IDENTIFIER)
        # initializations
        self.build_directory = ""
        self.env_file_name = ""
        self.env_file_destination = ""

        # settings
        self.build_directory = build_tree_location
        self.env_file_name = env_file_name
        self.env_file_destination = env_file_destination

    def process(self):

        # create tree root if necessary
        create_dir(self.build_directory)

        self.create_tree()

        self.add_db()
        self.add_credentials_file()
        self.add_preferences_file()
        self.add_internal_file()
        self.add_selection_file_samples()
        self.add_scripts()
        self.add_default_selection_file()

        self.customize()

        self.create_env_file()
        self.delete_build_directory()

    def customize(self):
        """
        This method can be implemented in child classes
        It is useful for tests to create customized 'envs'
        Use this method to customize the contents of your new envs
        see : synda.tests.process.env.build.installed.env1.models as an example
        """
        pass

    def add_db(self):
        full_filename = os.path.join(
            os.path.join(
                self.build_directory,
                "db",
            ),
            DEFAULT_DB_FILENAME,
        )
        request = CreateDBRequest(full_filename)
        request.process()

    def create_env_file(self):

        return create_tree_tar_file(self.build_directory, self.env_file_name, self.env_file_destination)

    def add_selection_file_samples(self):
        files_pattern = os.path.join(
            SELECTION_SAMPLE_DIR,
            "*.txt",
        )

        new_conf_default_path = os.path.join(
            os.path.join(
                self.build_directory,
                "selection",
            ),
            "sample",
        )
        create_dir(new_conf_default_path)

        for src in glob(files_pattern):
            dst = os.path.join(
                new_conf_default_path,
                os.path.basename(src),
            )
            copyfile(src, dst)

    def add_default_selection_file(self):
        files_pattern = os.path.join(
            DEFAULT_SELECTION_FILE_DIR,
            "*.txt",
        )

        new_conf_default_path = os.path.join(
            os.path.join(
                self.build_directory,
                "conf",
            ),
            "default",
        )
        create_dir(new_conf_default_path)

        for src in glob(files_pattern):
            dst = os.path.join(
                new_conf_default_path,
                os.path.basename(src),
            )
            copyfile(src, dst)

    def add_scripts(self):
        files_pattern = os.path.join(
            BIN_DIR,
            "*.sh",
        )

        for src in glob(files_pattern):
            dst = os.path.join(

                os.path.join(
                    self.build_directory,
                    "bin",
                ),
                os.path.basename(src),
            )
            copyfile(src, dst)
            os.chmod(dst, 0o755)

    def add_internal_file(self):
        path = os.path.join(
            self.build_directory,
            "conf",
        )
        full_filename = os.path.join(
            path,
            INTERNAL_FILENAME,
        )
        CreateInternal(full_filename)

    def add_preferences_file(self):
        path = os.path.join(
            self.build_directory,
            "conf",
        )
        full_filename = os.path.join(
            path,
            PREFERENCES_FILENAME,
        )
        CreatePreferences(full_filename)

    def add_credentials_file(self):
        path = os.path.join(
            self.build_directory,
            "conf",
        )
        full_filename = os.path.join(
            path,
            CREDENTIALS_FILENAME,
        )
        CreateCredentials(full_filename)

    def create_tree(self):
        for directory in ENV_SUB_DIRECTORIES:
            location = os.path.join(
                self.build_directory,
                directory,
            )
            create_dir(location)

    def delete_tree(self, target):
        delete_dirs(target)

    def delete_build_directory(self):
        self.delete_tree(self.build_directory)
