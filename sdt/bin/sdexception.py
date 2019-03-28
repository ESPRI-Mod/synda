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

class FileNotFoundException(SDException):
    pass
class HttpUrlNotFoundException(SDException):
    pass
class NoTransferWaitingException(SDException):
    pass
class FatalException(SDException):
    pass
class RemoteException(SDException):
    pass
class CertificateRenewalException(SDException):
    pass
class MissingDatasetTimestampUrlException(SDException):
    pass
class MissingTimestampException(SDException):
    pass
class EmptySelectionException(SDException):
    pass
class TooMuchValueException(SDException):
    pass
class PasswordNotSetException(SDException):
    pass
class UsernameNotSetException(SDException):
    pass
class MixedVersionFormatException(SDException):
    pass
class IncorrectVTCException(SDException): # VTC means 'Version Timestamp Correlation'
    pass
class IncorrectVersionFormatException(SDException):
    pass
class IncorrectParameterException(SDException):
    pass
class UnknownChecksumType(SDException):
    pass
#
class UnknownParameterNameException(IncorrectParameterException):
    pass
class UnknownParameterValueException(IncorrectParameterException):
    pass
#
class InvalidCertificateException(CertificateRenewalException):
    pass
class MissingCertificateException(CertificateRenewalException):
    pass
class OpenIDProcessingException(CertificateRenewalException):
    pass
class OpenIDIncorrectFormatException(CertificateRenewalException):
    pass
class OpenIDNotSetException(CertificateRenewalException):
    pass
#
class MissingDatasetUrlException(SDException):
    pass
