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
from synda.source.exceptions import MethodNotImplemented


class Config(Container, Identifier):

    def __init__(self, identifier, full_filename):
        Container.__init__(self)
        Identifier.__init__(self, identifier)
        self.full_filename = full_filename

    @property
    def filename(self):
        return os.path.basename(self.full_filename)

    @property
    def location(self):
        return os.path.dirname(self.full_filename)

    def exists(self):
        return os.path.exists(
            self.get()
        )

    def get(self):
        return self.full_filename

    def is_read_access_allowed(self):
        raise MethodNotImplemented("is_read_access_allowed", self.__class__)
