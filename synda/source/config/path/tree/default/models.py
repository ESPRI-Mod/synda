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

from synda.source.containers import Container
from synda.source.identifier import Identifier
from synda.source.constants import get_env_folder

from synda.source.config.path.tree.constants import STRUCTURE, IDENTIFIER


class Config(Container, Identifier):

    def __init__(self, identifier=IDENTIFIER):
        Container.__init__(self)
        Identifier.__init__(self, identifier)

        paths = dict()

        for directory in STRUCTURE:
            paths[directory] = os.path.join(
                get_env_folder(),
                directory,
            )

        self.set_data(paths)

    def provides(self, directory):
        return True if directory in list(self.get_data().keys()) else False

    @property
    def structure(self):
        return list(self.get_data().keys())

    def get(self, directory):
        return self.get_data()[directory]

    def set(self, directory, value):
        self.get_data()[directory] = value


if __name__ == '__main__':
    pass
