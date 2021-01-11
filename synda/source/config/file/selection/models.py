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

from synda.source.config.file.selection.constants import IDENTIFIER

from synda.source.config.file.selection.constants import DEFAULT
from synda.source.config.file.selection.constants import DEFAULT_PROJECT_TEMPLATE

from synda.source.config.path.tree.default.selection.models import Config as Path


class Config(Container, Identifier):

    def __init__(self):
        Container.__init__(self)
        Identifier.__init__(self, IDENTIFIER)

        default = dict(
            path=Path().get_default(),
            filename=DEFAULT,
            project=dict(
                filename_template=DEFAULT_PROJECT_TEMPLATE,
            ),
        )

        data = dict(
            default=default,
        )
        self.set_data(data)

    def exists(self, project=""):
        return os.path.exists(
            self.get_default(project)
        )

    def get_default(self, project=""):
        data = self.get_data()
        path = data["default"]['path']

        if project:
            filename = data["default"]['project']['filename_template'].format(project)
        else:
            filename = data["default"]['filename']
        return os.path.join(
            path,
            filename,
        )


if __name__ == '__main__':
    pass
