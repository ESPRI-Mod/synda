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
from synda.source.manager import Manager as Base

from synda.source.config.path.tree.default.models import Config as Paths

from synda.source.config.file.user.credentials.models import Config as Credentials
from synda.source.config.file.user.credentials.constants import IDENTIFIER as USER_CREDENTIALS_IDENTIFIER
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.log.models import Config as LogFiles

from synda.source.config.file.user.preferences.constants import IDENTIFIER as USER_PREFERENCES_IDENTIFIER

from synda.source.config.file.log.constants import IDENTIFIER as LOG_FILES_IDENTIFIER

from synda.source.config.path.tree.constants import IDENTIFIER as PATHS_IDENTIFIER


class Manager(Base):

    def __init__(self, checked):
        super(Manager, self).__init__()
        self.add(
            Credentials(),
        )
        self.add(
            Preferences(),
        )
        if checked:
            self.add(
                LogFiles(),
            )
            self.add(
                Paths(),
            )

    def get_user_credentials(self):
        return self.get_item(USER_CREDENTIALS_IDENTIFIER)

    def get_user_preferences(self):
        return self.get_item(USER_PREFERENCES_IDENTIFIER)

    def get_paths(self):
        return self.get_item(PATHS_IDENTIFIER)

    def get_log_files(self):
        return self.get_item(LOG_FILES_IDENTIFIER)


if __name__ == '__main__':
    pass
