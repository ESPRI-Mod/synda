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
from ConfigParser import SafeConfigParser

from synda.source.constants import get_env_folder
from synda.source.config.file.user.preferences.constants import FILENAME


def update_paths():
    root = get_env_folder()
    full_filename = os.path.join(
        os.path.join(
            root,
            "conf",
        ),
        FILENAME,
    )

    cfg = SafeConfigParser()
    cfg.read(full_filename)
    cfg.set('core', 'db_path', os.path.join(root, 'db'))
    cfg.set('core', 'selection_path', os.path.join(root, 'selection'))
    cfg.set('core', 'sandbox_path', os.path.join(root, 'sandbox'))
    cfg.set('core', 'default_path', os.path.join(*[root, 'conf', "default"]))

    with open(full_filename, "w+") as file_handler:
        cfg.write(file_handler)


if __name__ == '__main__':
    pass
