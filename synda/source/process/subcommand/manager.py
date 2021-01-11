# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.manager import Manager as Base
from synda.source.config.manager import Manager as ConfigManager
from synda.source.process.env.manager import Manager as EnvManager
from synda.source.config.subcommand.constants import NAMES as SUB_COMMAND_NAMES

from synda.source.process.subcommand.constants import get_process_class
from synda.source.process.subcommand.exceptions import InvalidRequest


class Manager(Base):

    def __init__(self, argv):
        super(Manager, self).__init__()
        # initialize
        self.env_manager = None
        self.sub_command = ""
        self.error = ""
        self.config_manager = None
        # settings
        self.settings(argv)

    def settings(self, argv):
        self.env_manager = EnvManager()
        self.load()
        validated = self.validate(argv)

    def is_validated_sub_command(self):
        return self.sub_command is not ""

    def validate_subcommand(self, argv):
        strerror = ""
        if len(argv) >= 2:
            sub_command_candidate = argv[1]
            if sub_command_candidate in SUB_COMMAND_NAMES:
                self.sub_command = sub_command_candidate
            else:
                strerror = "Invalid sub command request '{}'".format(sub_command_candidate)
        else:
            strerror = 'Invalid request'

        return strerror

    def validate(self, argv):
        strerror = self.validate_subcommand(argv)
        if strerror == "":
            self.validate_env()
        else:
            raise InvalidRequest(strerror)
        return strerror == ""

    def check_env(self, interactive_mode=False):
        checked = self.env_manager.check(interactive_mode=interactive_mode)
        if not checked:
            self.env_manager.init()
            checked = self.env_manager.check(interactive_mode=interactive_mode)
        return checked

    def validate_env(self):
        checked = False
        if self.is_environment_required():
            interactive_mode = False if self.get_user_credentials().is_read_access_allowed() else True
            checked = self.check_env(interactive_mode=interactive_mode)

        self.config_manager = ConfigManager(checked=checked)

    def load(self):

        for name in SUB_COMMAND_NAMES:
            process_class = get_process_class(name)
            process_instance = process_class()
            self.add(
                process_instance,
            )

    def get_config_manager(self):
        return self.config_manager

    def get_user_preferences(self):
        return self.config_manager.get_user_preferences()

    def get_authority(self):
        return self.get_subcommand(self.sub_command).get_authority()

    def get_user_credentials(self):
        return self.get_subcommand(self.sub_command).get_authority().get_user_credentials()

    def get_command_line_user_customization(self):

        preferences = self.config_manager.get_user_preferences()

        download_direct_http_timeout = preferences.download_direct_http_timeout
        interface_default_listing_size = preferences.interface_default_listing_size
        show_advanced_options = preferences.is_interface_show_advanced_options

        return dict(
            direct_http_timeout=download_direct_http_timeout,
            default_listing_size=interface_default_listing_size,
            show_advanced_options=show_advanced_options,
        )

    def add_subcommand(self, item):
        item.set_config_manager(
            self.config_manager,
        )
        self.add(item)

    def get_subcommand(self, identifier):
        return self.get_item(identifier)

    def is_environment_required(self):
        return self.get_item(self.sub_command).is_environment_required


if __name__ == '__main__':
    pass
