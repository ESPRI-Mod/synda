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

from synda.source.config.file.scripts.constants import IDENTIFIER
from synda.source.config.file.scripts.constants import STRUCTURE

from synda.source.config.path.tree.default.models import Config as Path


class Config(Container, Identifier):

    def __init__(self):
        Container.__init__(self)
        Identifier.__init__(self, IDENTIFIER)

        path = Path().get("bin")
        data = dict()
        for identifier in STRUCTURE.keys():
            filename = STRUCTURE[identifier]
            data[identifier] = os.path.join(
                path,
                filename,
            )

        self.set_data(data)

    def get_filenames_identifiers(self):
        return self.get_data().keys()

    def provides(self, identifier):
        return True if identifier in self.get_filenames_identifiers() else False

    def exists(self, identifier):
        return os.path.exists(
            self.get(identifier)
        )

    def get(self, identifier):
        return self.get_data()[identifier]


if __name__ == '__main__':
    pass
