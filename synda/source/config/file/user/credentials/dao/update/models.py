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
from configparser import ConfigParser

from synda.source.constants import get_env_folder
from synda.source.config.file.user.credentials.constants import FILENAME


def update(openid, password):

    root = get_env_folder()
    full_filename = os.path.join(
        os.path.join(
            root,
            "conf",
        ),
        FILENAME,
    )

    cred = ConfigParser()
    cred.read(full_filename)
    cred.set('esgf_credential', 'openid', openid)
    cred.set('esgf_credential', 'password', password)
    with open(full_filename, 'w+') as file_handler:
        cred.write(file_handler)


if __name__ == '__main__':
    pass
