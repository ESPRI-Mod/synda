# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.subcommand.exceptions import NotAuthorized
from synda.source.config.file.user.credentials.models import Config as Credentials

from synda.source.containers import Container
from synda.source.exceptions import MethodNotImplemented


class AbstractAuthority(Container):

    def __init__(self):
        super(AbstractAuthority, self).__init__()

    def is_authorized(self):
        raise MethodNotImplemented("is_authorized", self.__class__)


class Authority(AbstractAuthority):

    def __init__(self):
        super(Authority, self).__init__()
        self.add(Credentials())
        # self.control()

    def get_user_credentials(self):
        return self.get_data()[0]

    def check_error(self):
        credentials = self.get_user_credentials()
        openid = credentials.openid
        password = credentials.password
        from myproxy.client import MyProxyClientGetError
        from synda.sdt import sdlogon
        from synda.sdt.sdexception import OpenIDProcessingException
        try:
            sdlogon.renew_certificate(openid, password, force_renew_certificate=True)
            strerror = ""
        except MyProxyClientGetError as e:
            # invalid password
            strerror = str(e)
        except OpenIDProcessingException:
            # invalid openid
            strerror = "invalid openid"
        except Exception as e:
            strerror = str(e)
        return strerror

    def is_authorized(self):
        return self.check_error() == ""

    def control(self):
        checked_error = self.check_error()
        if checked_error != "":
            raise NotAuthorized(checked_error)
