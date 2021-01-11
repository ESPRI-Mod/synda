# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.tests.context.models import Context as Base


class Context(Base):

    def __init__(self, api_type, arguments=None):
        Base.__init__(self, arguments=arguments)

        # initialization
        self.api_type = ""

        # settings
        self.api_type = api_type

    def get_api_type(self):
        return self.api_type

    def set_api_type(self, api_type):
        self.api_type = api_type
