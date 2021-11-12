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
from synda.source.config.file.user.preferences.constants import FILENAME


def print_check_paths_error(path):
    error_msg = \
        f"   sdt.conf file / [core] Section / The following Path has not been Found : '{path}'."
    print(error_msg)


def check_default_path(root, config):
    checked = True
    directory = "default"
    path = config.get('core', f'{directory}_path')
    if path:
        if not os.path.exists(path):
            checked = False
            print_check_paths_error(path)
    else:
        # If not set by User, path is set by default under $ST_HOME root
        config.set(
            'core',
            f'{directory}_path',
            os.path.join(
                os.path.join(root, "conf"),
                directory,
            ),
        )

    return checked


def check_path(root, config, directory):
    checked = True
    path = config.get('core', f'{directory}_path')
    if path:
        if not os.path.exists(path):
            checked = False
            print_check_paths_error(path)
    else:
        # If not set by User, path is set by default under $ST_HOME root
        config.set('core', f'{directory}_path', os.path.join(root, directory))

    return checked


def check_paths():
    root = get_env_folder()
    full_filename = os.path.join(
        os.path.join(
            root,
            "conf",
        ),
        FILENAME,
    )
    config = ConfigParser()
    config.read(full_filename)

    checked = check_path(root, config, "db")
    if checked:
        checked = check_path(root, config, "selection")
    if checked:
        checked = check_path(root, config, "data")
    if checked:
        checked = check_default_path(root, config)
    if checked:
        checked = check_path(root, config, "sandbox")

    if checked:
        with open(full_filename, 'w') as configfile:
            config.write(configfile)

    return checked


if __name__ == '__main__':
    pass
