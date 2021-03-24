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
from synda.source.constants import RESOURCES_DIR

IDENTIFIER = "internal"

DIRECTORY = "conf"
FILENAME = "internal.conf"

DEFAULT_FULL_FILENAME = os.path.join(*[TreePath().get(DIRECTORY), FILENAME])
FULL_FILENAME_USED_IF_INIT_ENV_NOT_FOUND = os.path.join(*[RESOURCES_DIR, DIRECTORY, FILENAME])

DEFAULT_OPTIONS = dict(

    # loggers

    feeder="feeder",
    consumer="consumer",
    domain="domain",

    # filenames

    checksum_type_md5="md5",
    checksum_type_sha256="sha256",

    feeder_logfile='discovery.log',
    consumer_logfile='transfer.log',
    domain_logfile='domain.log',

    # api

    esgf_search_domain_name='IDXHOSTMARK',

    # processes

    chunksize='5000',
    http_clients='wget, urllib',
    transfer_protocols='http, gridftp',
    get_files_caching='true',

    # hack

    projects_with_one_variable_per_dataset='CORDEX, CMIP6',
)
