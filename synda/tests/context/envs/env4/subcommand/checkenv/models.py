# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.context.models import Context as Base

from synda.source.config.file.user.preferences.models import Config as Preferences


class Context(Base):

    def __init__(self, config, capsys=None, validate=True):
        super(Context, self).__init__(
            capsys=capsys,
            validate=validate,
        )
        # init
        self.config = ""
        self.exception_instance = ""
        # settings
        self.config = config

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        assert not captured.err

        config = self.get_config()

        preferences = Preferences()

        core_selection_path = preferences.core_selection_path
        print(f"sdt.conf / observed selection_path = {core_selection_path}")
        print(f"sdt.conf / expected selection_path = {config['core']['selection_path']}")

        print(f"sdt.conf / observed default_path   = {preferences.core_default_path}")
        print(f"sdt.conf / expected default_path   = {config['core']['default_path']}")

        print(f"sdt.conf / observed db_path        = {preferences.core_db_path}")
        print(f"sdt.conf / expected db_path        = {config['core']['db_path']}")

        print(f"sdt.conf / observed data_path      = {preferences.core_data_path}")
        print(f"sdt.conf / expected data_path      = {config['core']['data_path']}")

        print(f"sdt.conf / observed sandbox_path   = {preferences.core_sandbox_path}")
        print(f"sdt.conf / expected sandbox_path   = {config['core']['sandbox_path']}")

        assert config['core']['db_path'] in captured.out
        assert config['check']['paths']['error_type'] in captured.out
