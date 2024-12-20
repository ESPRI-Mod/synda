#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains application initialization code.

Note
    This module must be imported in every other scripts (daemon included)
"""

import os
from synda.sdt import sdapputils


os.umask(0o0002)

name = 'transfer'
version = '3.10'
sdapputils.set_exception_handler()
