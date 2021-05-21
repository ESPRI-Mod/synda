# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.config.file.internal.constants import FILENAME as INTERNAL_FILENAME
from synda.tests.tests.constants import DATADIR as ROOT

FILENAMES = {
    'standard': os.path.join(
        *[
            ROOT,
            "file",
            "internal",
            INTERNAL_FILENAME,
        ]
    ),
    'get_files_caching': os.path.join(
        *[
            ROOT,
            "file",
            "internal",
            "get_files_caching",
            INTERNAL_FILENAME,
        ]
    ),
    'http_client': {
        "1": os.path.join(
            *[
                ROOT,
                "file",
                "internal",
                "http_client",
                "1",
                INTERNAL_FILENAME,
            ]
        ),
        "2": os.path.join(
            *[
                ROOT,
                "file",
                "internal",
                "http_client",
                "2",
                INTERNAL_FILENAME,
            ]
        ),
    },
    'transfer_protocol': {
        "1": os.path.join(
            *[
                ROOT,
                "file",
                "internal",
                "transfer_protocol",
                "1",
                INTERNAL_FILENAME,
            ]
        ),
        "2": os.path.join(
            *[
                ROOT,
                "file",
                "internal",
                "transfer_protocol",
                "2",
                INTERNAL_FILENAME,
            ]
        ),
        "3": os.path.join(
            *[
                ROOT,
                "file",
                "internal",
                "transfer_protocol",
                "3",
                INTERNAL_FILENAME,
            ]
        ),
    },
    'hack_projects': {
        "1": os.path.join(
            *[
                ROOT,
                "file",
                "internal",
                "hack_projects",
                "1",
                INTERNAL_FILENAME,
            ]
        ),
        "2": os.path.join(
            *[
                ROOT,
                "file",
                "internal",
                "hack_projects",
                "2",
                INTERNAL_FILENAME,
            ]
        ),
        "3": os.path.join(
            *[
                ROOT,
                "file",
                "internal",
                "hack_projects",
                "3",
                INTERNAL_FILENAME,
            ]
        ),
    },
}
