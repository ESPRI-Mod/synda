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

from synda.source.config.path.tree.constants import IDENTIFIER

from synda.source.config.path.tree.default.selection.constants import DEFAULT as DEFAULT_DIRECTORY
from synda.source.config.path.tree.models import Config as TreePath


class Config(Container, Identifier):

    def __init__(self, identifier=IDENTIFIER):
        Container.__init__(self)
        Identifier.__init__(self, identifier)

        paths = dict(
            default=os.path.join(
                TreePath().get("conf"),
                DEFAULT_DIRECTORY,
            ),
        )

        self.set_data(paths)

    def get_default(self):
        return self.get_data()["default"]

    def set_default(self, value):
        self.get_data()["default"] = value


if __name__ == '__main__':
    pass
