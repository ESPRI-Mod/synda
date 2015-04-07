#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains shortcuts used in console mode.

Note
    This class must be subclassed.
"""

import sdsessionparam
import sdi18n

class Shortcut(object):

    def do_d(self,arg):
        localsearch=sdsessionparam.get_value('dry_run')
        if not localsearch:
            sdsessionparam.set('dry_run','true')

    def do_h(self,arg):
        print """
d => toogle 'dry_run' flag
h => print shortcuts table
l => toogle 'localsearch' flag
q => print last search-api query
t => toggle 'type' flag
"""

    def do_l(self,arg):
        localsearch=sdsessionparam.get_value('localsearch')
        if not localsearch:
            sdsessionparam.set('localsearch','true')
            print 'Local search enabled'
        else:
            sdsessionparam.set('localsearch','false')
            print 'Local search disabled'

    def do_q(self,arg):
        sdsessionparam.print_session_param('last_query')

    def do_t(self,arg):

        type_=sdsessionparam.get_value('type')

        if type_=='Dataset':
            sdsessionparam.set('type','File')
            print "Type set to 'File'"
        elif type_=='File':
            sdsessionparam.set('type','Dataset')
            print "Type set to 'Dataset'"

    """
    def help_q(self):
        print sdi18n.m0006('q','Print last search-api query')
    """
