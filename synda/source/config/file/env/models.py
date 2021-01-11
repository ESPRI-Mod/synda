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
from synda.source.config.file.models import Config as Base
from synda.source.config.file.env.constants import IDENTIFIER
from synda.source.config.file.env.constants import DEFAULT_FULL_FILENAME


class Config(Base):

    def __init__(self, full_filename=DEFAULT_FULL_FILENAME):
        Base.__init__(self, IDENTIFIER, full_filename)
