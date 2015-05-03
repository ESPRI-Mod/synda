#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains console common routines."""

import sddeferredafter
import sdsessionparam

class ConsoleUtils(object):
    """This class must be subclassed."""

    def complete_parameter(self):
        self.parameter.extend(sdsessionparam.get_serialized_session_facets()) # TODO: maybe set session facets as default parameter being overwrited by parameter

        sddeferredafter.add_default_parameter(self.parameter,'limit',sdsessionparam.get_value('limit'))
        sddeferredafter.add_default_parameter(self.parameter,'verbose',sdsessionparam.get_value('verbose'))
