# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
import os

from synda.source.containers import Container
from synda.source.identifier import Identifier

from synda.source.config.file.certificate.x509.constants import FILENAME as X509_CERTIFICATE_FILENAME

from synda.source.config.file.certificate.x509.constants import IDENTIFIER
from synda.source.config.path.tree.certificate.x509.models import Config as Path


class Config(Container, Identifier):

    def __init__(self):
        Container.__init__(self)
        Identifier.__init__(self, IDENTIFIER)
        self.init()

    def init(self):

        data = dict(
            credentials=os.path.join(
                Path().get_security(),
                X509_CERTIFICATE_FILENAME,
            ),
        )
        self.set_data(data)

    def credentials_exists(self):
        return os.path.exists(
            self.get_credentials(),
        )

    def get_credentials(self):
        return self.get_data()["credentials"]


if __name__ == '__main__':
    pass
