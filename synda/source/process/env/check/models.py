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

from synda.source.identifier import Identifier

from synda.source.config.env.check.constants import REQUIRED_FILES
from synda.source.config.env.check.constants import REQUIRED_DIRECTORIES
from synda.source.config.env.check.constants import ERROR_ENVIRONMENT_VARIABLE_PREFIX
from synda.source.config.env.check.constants import ERROR_KEY_FILE_MISSING_TEMPLATE
from synda.source.config.env.check.constants import ERROR_KEY_DIRECTORY_MISSING_TEMPLATE
from synda.source.config.env.check.constants import CHECK_COMPLETE
from synda.source.config.env.check.constants import CHECK_ERROR

from synda.source.process.env.check.constants import IDENTIFIER

from synda.source.config.file.user.preferences.dao.update.models \
    import check_paths as preferences_check_paths
from synda.source.config.file.user.credentials.dao.update.models import update as update_credentials


class Config(Identifier):

    def __init__(
            self,
            root,
            required_files=REQUIRED_FILES,
            required_directories=REQUIRED_DIRECTORIES,
    ):
        Identifier.__init__(self, IDENTIFIER)

        self.root = root

        self.required = dict()

        self.user_action_if_env_not_checked = ""

        # settings

        self.user_action_if_env_not_checked = \
            'You can either copy previously used file into your ST_HOME ({}) ' \
            'or use synda init-env command to ' \
            'initialize a new synda home file system with stubs to fill properly.'.format(
                self.root,
            )

        self.required = dict(
            files=required_files,
            directories=required_directories,
        )

    def process(self, interactive_mode=False):
        checked = os.path.isdir(self.root)
        if checked:
            checked = self.process_required_files()
            if checked:
                checked = self.process_required_directories()
                if checked:
                    checked = preferences_check_paths()
                    if checked:
                        if interactive_mode:
                            self.update_credentials_file()
                        print(CHECK_COMPLETE)
                    else:
                        print(CHECK_ERROR)
        else:
            print(
                "{} {}".format(
                    ERROR_ENVIRONMENT_VARIABLE_PREFIX,
                    "ST_HOME",
                ),
            )
        return checked

    def update_credentials_file(self):
        # To ease up credentials setting.
        answer = ''
        while answer not in ['y', 'n']:
            answer = input('Would you like to set your openID credentials? y/n: ').lower()
            if answer == 'y':
                openid = input('openID url: ')
                password = input('password: ')
                update_credentials(openid, password)

    def get_required_files(self, index):
        filename = self.required["files"][index]
        return os.path.join(
            self.root,
            filename,
        )

    def process_required_files(self):
        nb_records = len(self.required["files"])
        i = 0
        eod = i >= nb_records
        full_filename = self.get_required_files(i)
        while not eod and os.path.isfile(full_filename):
            i += 1
            eod = i >= nb_records
            if not eod:
                full_filename = self.get_required_files(i)

        checked = i == nb_records

        if not checked:
            print(
                ERROR_KEY_FILE_MISSING_TEMPLATE.format(
                    self.required["files"][i],
                ),
            )
            print(self.user_action_if_env_not_checked)

        return checked

    def process_required_directories(self):
        nb_records = len(self.required["directories"])
        i = 0
        eod = i >= nb_records
        directory = os.path.join(
            self.root,
            self.required["directories"][i],
         )

        while not eod and os.path.isdir(directory):
            i += 1
            eod = i >= nb_records
            if not eod:
                directory = os.path.join(
                    self.root,
                    self.required["directories"][i],
                )

        checked = i == nb_records

        if not checked:
            print(
                ERROR_KEY_DIRECTORY_MISSING_TEMPLATE.format(
                    self.required["directories"][i],
                ),
            )
            print(self.user_action_if_env_not_checked)

        return checked
