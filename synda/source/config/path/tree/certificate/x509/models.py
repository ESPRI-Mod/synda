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

from synda.sdt.sdexception import SDException
from synda.source.containers import Container
from synda.source.identifier import Identifier

from synda.source.config.file.certificate.x509.constants import IDENTIFIER

from synda.source.config.path.tree.default.models import Config as TreePath

from synda.source.config.file.certificate.x509.constants import FILENAME as X509_CERTIFICATE_FILENAME
from synda.source.config.path.tree.certificate.x509.constants import CERTIFICATES

from synda.source.config.path.tree.certificate.x509.constants import HOME
from synda.source.config.path.tree.certificate.x509.constants import TMP
from synda.source.config.path.tree.certificate.x509.constants import TMPUID
from synda.source.config.path.tree.certificate.x509.constants import MIXED

from synda.source.config.file.user.preferences.models import Config as Preferences


class Config(Container, Identifier):

    def __init__(self):
        Container.__init__(self)
        Identifier.__init__(self, IDENTIFIER)

        self.core_security_dir_mode = ""
        self.init()

    def init(self):

        self.core_security_dir_mode = Preferences().core_security_dir_mode

        if self.core_security_dir_mode == TMP:
            security = os.path.join(
                TreePath().get('tmp'),
                ".esg",
            )
        elif self.core_security_dir_mode == TMPUID:
            security = os.path.join(
                os.path.join(
                    TreePath().get('tmp'),
                    str(
                        os.getuid(),
                    ),
                ),
                ".esg",
            )
        elif self.core_security_dir_mode == HOME:
            if 'HOME' not in os.environ:
                raise SDException(
                    'SDCONFIG-120',
                    "HOME env. var. must be set when 'security_dir_mode' is set to {}".format(
                        HOME,
                    ),
                )
            security = os.path.join(
                os.environ['HOME'],
                ".esg",
            )

        elif self.core_security_dir_mode == MIXED:
            security = os.path.join(
                TreePath().get('tmp'),
                ".esg",
            )
        else:
            raise SDException(
                'SDCONFIG-020',
                "Incorrect value for security_dir_mode ({})".format(
                    self.core_security_dir_mode,
                ),
            )

        data = dict(
            security=security,
        )
        self.set_data(data)

    def get_core_security_dir_mode(self):
        return self.core_security_dir_mode

    def security_exists(self):
        return os.path.exists(
            self.get_security()
        )

    def get_certificates(self):
        return os.path.join(
            self.get_security(),
            CERTIFICATES,
        )

    def get_security(self):
        return self.get_data()['security']


if __name__ == '__main__':
    pass
