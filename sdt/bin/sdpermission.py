#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains permission related routines."""

import sdtools
import sdconfig

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
    return sdtools.is_file_read_access_OK(sdconfig.credential_file) # ie user must be admin if he can read passwd file (either root, in synda group or the install user)

def is_regular_user():
    return not is_admin()
