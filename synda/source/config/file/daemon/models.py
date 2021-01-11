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

from synda.source.config.file.daemon.constants import IDENTIFIER

from synda.source.config.file.daemon.constants import DEFAULT

from synda.source.config.path.tree.daemon.models import Config as Path


class Config(Container, Identifier):

    def __init__(self):
        Container.__init__(self)
        Identifier.__init__(self, IDENTIFIER)

        default = dict(
            path=Path().get_default(),
            filename=DEFAULT,
        )

        data = dict(
            default=default,
        )
        self.set_data(data)

    def exists(self):
        return os.path.exists(
            self.default,
        )

    @property
    def default(self):
        data = self.get_data()
        return os.path.join(
            data["default"]['path'],
            data["default"]['filename'],
        )


if __name__ == '__main__':
    pass
