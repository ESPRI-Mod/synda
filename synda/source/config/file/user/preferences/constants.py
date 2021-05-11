# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os

from synda.source.constants import RESOURCES_DIR

IDENTIFIER = "preferences"

DIRECTORY = "conf"
FILENAME = "sdt.conf"

DEFAULT_FULL_FILENAME = os.path.join(*[RESOURCES_DIR, DIRECTORY, FILENAME])

DEFAULT_OPTIONS = dict(
    max_parallel_download="8",
    max_parallel_download_per_datanode="8",
    get_only_latest_version='true',
    user='',
    group='',
    hpss='0',
    download='true',
    post_processing='false',
    globustransfer='false',
    data_path='',
    sandbox_path='',
    db_path='',
    default_path='',
    selection_path='',
    security_dir_mode='tmpuid',
    metadata_server_type='esgf_search_api',
    unicode_term='0',
    progress='1',
    onemgf='false',
    ignorecase='true',
    default_listing_size='small',
    http_fallback='false',
    check_parameter='1',
    verbosity_level='info',
    scheduler_profiling='0',
    lfae_mode='abort',
    indexes='esgf-node.ipsl.fr,esgf-data.dkrz.de,esgf-index1.ceda.ac.uk',
    default_index='esgf-node.ipsl.fr',
    nearest='false',
    nearest_mode='geolocation',
    incorrect_checksum_action='remove',
    incremental_mode_for_datasets='false',
    continue_on_cert_errors='false',

    direct_http_timeout='30',
    async_http_timeout='120',

    direct_db_timeout="120",
    async_db_timeout="12000",

    dump_listing_limit_for_small_mode="50",
    dump_listing_limit_for_medium_mode='100',
    dump_listing_limit_for_big_mode="6000",

    list_listing_limit_for_small_mode="20",
    list_listing_limit_for_medium_mode="200",
    list_listing_limit_for_big_mode="20000",

    search_listing_limit_for_small_mode="100",
    search_listing_limit_for_medium_mode="1000",
    search_listing_limit_for_big_mode='6000',

    show_advanced_options="false",

    aesgf_search_chunksize="9000",
    esgf_search_http_timeout="300",

    big_file_size='795795708',
    big_file_chunksize='16384',
)
