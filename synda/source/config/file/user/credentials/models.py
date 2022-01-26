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
from synda.source.config.file.user.credentials.constants import get_fullfilename
from synda.source.config.file.user.readers import get_parser

DEFAULT_OPENID = 'https://esgf-node.ipsl.fr/esgf-idp/openid/foo'


def validate_openid(openid):
    is_set = False
    if openid:
        if openid.startswith("https://") and openid != DEFAULT_OPENID:
            is_set = True

    return is_set


class Config(Base):

    def __init__(self, full_filename=get_fullfilename()):
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
        return validate_openid(self.openid)

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
