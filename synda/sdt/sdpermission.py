#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains permission related routines."""

from synda.sdt import sdtools
from synda.source.config.file.user.credentials.models import Config as CredentialsFile


def is_admin():
    """
    Notes
        - admin can be
            - root
            - normal user if part of 'synda' group
            - user used for source installation (files owner)
        - root is always considered admin, because of the side-effect that he
          have access to all files. Maybe use 'file owner' here instead to fix
          this.
    """
    # ie user must be admin if he can read passwd file (either root, in synda group or the install user)
    return sdtools.is_file_read_access_OK(
        CredentialsFile().get(),
    )


def is_regular_user():
    return not is_admin()
