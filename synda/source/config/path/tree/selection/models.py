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

from synda.source.config.path.tree.selection.constants import IDENTIFIER
from synda.source.config.path.tree.default.selection.models import Config as Base

from synda.source.config.file.user.preferences.models import Config as Preferences


class Config(Base):

    def __init__(self):
        Base.__init__(self, IDENTIFIER)

        self.overwriting()

    def overwriting(self):
        """
        The tree paths default values are overwritten by user preferences values
        """

        preferences = Preferences()

        path = preferences.core_default_path
        if os.path.exists(path):
            self.set_default(path)


if __name__ == '__main__':
    pass
