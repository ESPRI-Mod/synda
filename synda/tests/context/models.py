# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################


class Context(object):

    def __init__(self, capsys=None):

        # During test execution any output sent to stdout and stderr is captured
        self.capsys = None

        self.capsys = capsys

    def get_capsys(self):
        return self.capsys

    def set_capsys(self, capsys):
        self.capsys = capsys

    def controls_before_subcommand_execution(self):
        pass

    def validation_after_subcommand_execution(self):
        pass
