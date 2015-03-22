#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdconsoleutils.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
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
