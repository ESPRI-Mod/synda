# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.internal.models import Config as Internal

CHECKSUM_TYPE_MD5 = Internal().checksum_type_md5
CHECKSUM_TYPE_SHA256 = Internal().checksum_type_sha256

CHECKSUM_TYPES = [
    CHECKSUM_TYPE_MD5,
    CHECKSUM_TYPE_SHA256,
]

CHECKSUM = dict(
    type=dict(
        md5=CHECKSUM_TYPE_MD5,
        sha256=CHECKSUM_TYPE_SHA256,
    ),
    types=CHECKSUM_TYPES,
)
