# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.config.path.tree.default.models import Config as TreePath


FILENAME = "credentials.conf"


def get_fullfilename():
    return os.path.join(
        TreePath().get("conf"),
        FILENAME,
    )


IDENTIFIER = "credentials"

DEFAULT_FULLFILENAME = os.path.join(
    TreePath().get("conf"),
    FILENAME,
)

DEFAULT_OPTIONS = dict(
    openid='https://esgf-node.ipsl.fr/esgf-idp/openid/foo',
    password='foobar',
)
