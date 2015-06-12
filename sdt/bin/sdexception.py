#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains exception classes.

Note
    This module doesn't use any other (Synda) module and thus can be used
    everywhere (even in 'sdapp' module) without circular dependency problem.
"""

class SDException(Exception):
    def __init__(self, code=None, msg=None):
        self.code=code
        self.msg=msg
    def __str__(self):
        return "code=%s,message=%s"%(self.code,self.msg)

class NoTransferWaitingException(SDException):
    pass
class FatalException(SDException):
    pass
class RemoteException(SDException):
    pass
class CertificateRenewalException(SDException):
    pass
