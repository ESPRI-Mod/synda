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
    url_max_buffer_size="3500",
    max_parallel_download="8",
    max_parallel_download_per_datanode="8",
    get_only_latest_version='true',
    hpss='0',
    download='true',
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

    esgf_search_chunksize="9000",
    esgf_search_http_timeout="300",

    streaming_chunk_size='0',
    install_interactive="true",
    country="",
)

DEFAULT_CONTENT = {
    'module': {
        'download': DEFAULT_OPTIONS["download"],
    },
    'log': {
        'verbosity_level': DEFAULT_OPTIONS["verbosity_level"],
        'scheduler_profiling': DEFAULT_OPTIONS["scheduler_profiling"],
    },
    'core': {
        'security_dir_mode': DEFAULT_OPTIONS["security_dir_mode"],
        'metadata_server_type': DEFAULT_OPTIONS["metadata_server_type"],
        'selection_path': DEFAULT_OPTIONS["selection_path"],
        'default_path': DEFAULT_OPTIONS["default_path"],
        'data_path': DEFAULT_OPTIONS["data_path"],
        'db_path': DEFAULT_OPTIONS["db_path"],
        'sandbox_path': DEFAULT_OPTIONS["sandbox_path"],
    },
    'interface': {
        'show_advanced_options': DEFAULT_OPTIONS["show_advanced_options"],

        'dump_listing_limit_for_small_mode': DEFAULT_OPTIONS["dump_listing_limit_for_small_mode"],
        'dump_listing_limit_for_medium_mode': DEFAULT_OPTIONS["dump_listing_limit_for_medium_mode"],
        'dump_listing_limit_for_big_mode': DEFAULT_OPTIONS["dump_listing_limit_for_big_mode"],

        'list_listing_limit_for_small_mode': DEFAULT_OPTIONS["list_listing_limit_for_small_mode"],
        'list_listing_limit_for_medium_mode': DEFAULT_OPTIONS["list_listing_limit_for_medium_mode"],
        'list_listing_limit_for_big_mode': DEFAULT_OPTIONS["list_listing_limit_for_big_mode"],

        'search_listing_limit_for_big_mode': DEFAULT_OPTIONS["search_listing_limit_for_big_mode"],
        'search_listing_limit_for_medium_mode': DEFAULT_OPTIONS["search_listing_limit_for_medium_mode"],
        'search_listing_limit_for_small_mode': DEFAULT_OPTIONS["search_listing_limit_for_small_mode"],

        'default_listing_size': DEFAULT_OPTIONS["default_listing_size"],
        'progress': DEFAULT_OPTIONS["progress"],
        'unicode_term': DEFAULT_OPTIONS["unicode_term"],
    },
    'behaviour': {
        'onemgf': DEFAULT_OPTIONS["onemgf"],
        'check_parameter': DEFAULT_OPTIONS["check_parameter"],
        'ignorecase': DEFAULT_OPTIONS["ignorecase"],
        'nearest': DEFAULT_OPTIONS["nearest"],
        'nearest_mode': DEFAULT_OPTIONS["nearest_mode"],
        'lfae_mode': DEFAULT_OPTIONS["lfae_mode"],
        'incorrect_checksum_action': DEFAULT_OPTIONS["incorrect_checksum_action"],
    },
    'api': {
        'esgf_search_chunksize': DEFAULT_OPTIONS["esgf_search_chunksize"],
        'esgf_search_http_timeout': DEFAULT_OPTIONS["esgf_search_http_timeout"],
    },
    'download': {
        'url_max_buffer_size': DEFAULT_OPTIONS["url_max_buffer_size"],
        'incremental_mode_for_datasets': DEFAULT_OPTIONS["incremental_mode_for_datasets"],
        'max_parallel_download': DEFAULT_OPTIONS["max_parallel_download"],
        'max_parallel_download_per_datanode': DEFAULT_OPTIONS["max_parallel_download_per_datanode"],
        'hpss': DEFAULT_OPTIONS["hpss"],
        'http_fallback': DEFAULT_OPTIONS["http_fallback"],
        'direct_http_timeout': DEFAULT_OPTIONS["direct_http_timeout"],
        'async_http_timeout': DEFAULT_OPTIONS["async_http_timeout"],
        'direct_db_timeout': DEFAULT_OPTIONS["direct_db_timeout"],
        'async_db_timeout': DEFAULT_OPTIONS["async_db_timeout"],
        'streaming_chunk_size': DEFAULT_OPTIONS["streaming_chunk_size"],
    },
    'local': {
        'country': DEFAULT_OPTIONS["country"],
    },
    'install': {
        'interactive': DEFAULT_OPTIONS["install_interactive"],
    },
    'index': {
        'indexes': DEFAULT_OPTIONS["indexes"],
        'default_index': DEFAULT_OPTIONS["default_index"],
    },
}
