#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains messages printed on stdxxx.

Note
    Message contained in this module can include stdxxx output from other
    function/module (which is not possible for message contained in sdi18n
    module (in a simple way, without grabbing stdout from the command)).
"""

import sdparam

def m1001():
    print
    print "You need to specify a project when using 'search' action"
    print
    print "Project list:"
    print
    sdparam.main(['project','--columns=3'])
    print
    print 'Example:'
    print '    synda search obs4MIPs'
    print
