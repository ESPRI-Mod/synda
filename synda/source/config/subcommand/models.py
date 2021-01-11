# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.identifier import Identifier


class Subcommand(Identifier):

    def __init__(self, name, args=None):
        super(Subcommand, self).__init__(name)

        self.config_manager = None
        self.args = None

        # initialization

        self.args = args

    def set_config_manager(self, value):
        self.config_manager = value

    def get_config_manager(self):
        return self.config_manager

    def get_name(self):
        return self.get_identifier()

    def get_args(self):
        return self.args


if __name__ == '__main__':
    pass
