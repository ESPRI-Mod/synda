# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.subcommand.required.env.models import Process as Base
from synda.source.process.authority.models import Authority


class Process(Base):

    def __init__(self):
        super(Process, self).__init__(name="facet", authority=Authority())
