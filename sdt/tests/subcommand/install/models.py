# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.tests.subcommand.models import SubCommand as Base
from sdt.tests.exceptions import MethodNotImplemented


class SubCommand(Base):

    def __init__(self, context, exceptions_codes=None, description=""):
        super(SubCommand, self).__init__(
            "install",
            context,
            exceptions_codes=exceptions_codes,
            description=description,
        )

    def configure(self, **kwargs):
        raise MethodNotImplemented("configure", self.__class__)
