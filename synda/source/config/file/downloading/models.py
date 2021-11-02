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
import psutil

from synda.source.utils import remove_local_path
from synda.source.containers import Container
from synda.source.identifier import Identifier
from synda.source.config.file.downloading.constants import IDENTIFIER
from synda.source.config.file.downloading.constants import DEFAULT
from synda.source.config.path.tree.downloading.models import Config as Path


class Config(Container, Identifier):

    def __init__(self, path=Path().get_default()):
        Container.__init__(self)
        Identifier.__init__(self, IDENTIFIER)

        default = dict(
            path=path,
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

    def set_content(self, content):
        f = open(self.default, 'w')
        f.write(
            content,
        )

    def get_content(self):
        f = open(self.default, 'r')
        return f.read()

    def get_pid(self):
        pid = 0
        if self.exists():
            content = self.get_content()
            try:
                pid = int(content)
            except ValueError:
                pass
        return pid

    def process_is_active(self, simulation=False):
        pid = self.get_pid()
        if simulation:
            res = True if pid else False
        else:
            res = psutil.pid_exists(pid) if pid else False
        return res

    def delete(self):
        return remove_local_path(self.default)

    @property
    def default(self):
        data = self.get_data()
        return os.path.join(
            data["default"]['path'],
            data["default"]['filename'],
        )


if __name__ == '__main__':
    pass
