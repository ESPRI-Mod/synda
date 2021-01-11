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

from synda.source.config.file.models import Config as Base
from synda.source.config.file.user.credentials.constants import IDENTIFIER
from synda.source.config.file.user.credentials.constants import DEFAULT_OPTIONS
from synda.source.config.file.user.credentials.constants import DEFAULT_FULLFILENAME
from synda.source.config.file.user.readers import get_parser


class Config(Base):

    def __init__(self, full_filename=DEFAULT_FULLFILENAME):
        Base.__init__(self, IDENTIFIER, full_filename)
        self.default_openid = 'https://esgf-node.ipsl.fr/esgf-idp/openid/foo'
        if self.exists():
            self.set_data(get_parser(full_filename, DEFAULT_OPTIONS))

    @property
    def openid(self):
        return self.get_data().get('esgf_credential', 'openid')

    @property
    def password(self):
        return self.get_data().get('esgf_credential', 'password')

    def is_openid_set(self):
        is_set = False
        openid = self.openid
        if openid:
            if openid.startswith("https://") and openid != self.default_openid:
                is_set = True

        return is_set

    def is_read_access_allowed(self):
        try:
            open(self.full_filename)
            alllowed = True
        except IOError as err:
            alllowed = 'Permission denied' not in err.strerror
        return alllowed


if __name__ == '__main__':
    config = Config()
    config.is_read_access_allowed()
    pass
