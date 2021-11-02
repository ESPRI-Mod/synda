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
import configparser

from synda.source.constants import get_env_folder

from synda.source.config.file.models import Config as Base

from synda.source.config.file.user.preferences.constants import DEFAULT_FULL_FILENAME
from synda.source.config.file.user.preferences.constants import IDENTIFIER
from synda.source.config.file.user.preferences.constants import DIRECTORY
from synda.source.config.file.user.preferences.constants import FILENAME
from synda.source.config.file.user.preferences.constants import DEFAULT_CONTENT

from synda.source.config.file.user.readers import overwrite_parser


class Config(Base):

    def __init__(self, full_filename=""):
        """
            Several sub command 'arguments' can be set with data given by this file
            for example : 'show advanced options', 'direct_http_timeout' or 'default_listing_size'
            So these data are always required, even if the sub command is 'help'...

            Consequently, a sdt.conf is stored as a resource. It contains default values,
            and it is used then User 'std.conf' can not be found in the User workspace
        """

        if not full_filename:
            # Looking for the 'sdt.conf' located into the User workspace
            full_filename = os.path.join(
                os.path.join(
                    get_env_folder(),
                    DIRECTORY,
                ),
                FILENAME,
            )
        Base.__init__(self, IDENTIFIER, full_filename)

        if not self.exists():
            # Use of the 'sdt.conf' located into the synda resource directory
            # print(ENV_NOT_FOUND)
            full_filename = DEFAULT_FULL_FILENAME

        default_parser = configparser.ConfigParser()

        default_parser.read_dict(
            DEFAULT_CONTENT,
        )

        self.set_data(overwrite_parser(full_filename, default_parser))

    # SECTION : CORE

    @property
    def core_security_dir_mode(self):
        return self.get_data().get('core', 'security_dir_mode')

    @property
    def core_metadata_server_type(self):
        """
        Only 'esgf_search_api' is allowed from synda version 3.14 upwards
        So this API name is enforced if necessary
        :return: requested API name
        """
        metadata_server_type = self.get_data().get('core', 'metadata_server_type')
        if metadata_server_type != "esgf_search_api":
            metadata_server_type = "esgf_search_api"

        return metadata_server_type

    @property
    def core_selection_path(self):
        return self.get_data().get('core', 'selection_path')

    @property
    def core_default_path(self):
        return self.get_data().get('core', 'default_path')

    @property
    def core_data_path(self):
        return self.get_data().get('core', 'data_path')

    @property
    def core_db_path(self):
        return self.get_data().get('core', 'db_path')

    @property
    def core_sandbox_path(self):
        return self.get_data().get('core', 'sandbox_path')

    # SECTION : BEHAVIOUR

    @property
    def behaviour_incorrect_checksum_action(self):
        return self.get_data().get('behaviour', 'incorrect_checksum_action')

    @property
    def behaviour_lfae_mode(self):
        return self.get_data().get('behaviour', 'lfae_mode')

    @property
    def behaviour_nearest_mode(self):
        return self.get_data().get('behaviour', 'nearest_mode')

    @property
    def is_behaviour_onemgf(self):
        return self.get_data().getboolean('behaviour', 'onemgf')

    @property
    def is_behaviour_nearest(self):
        return self.get_data().getboolean('behaviour', 'nearest')

    @property
    def behaviour_check_parameter(self):
        return self.get_data().getint('behaviour', 'check_parameter')

    @property
    def is_behaviour_ignorecase(self):
        return self.get_data().getboolean('behaviour', 'ignorecase')

    # SECTION : DOWNLOAD

    @property
    def is_download_hpss(self):
        return self.get_data().getboolean('download', 'hpss')

    @property
    def is_download_http_fallback(self):
        # if set to True, automatically switch to the next url if error occurs
        return self.get_data().getboolean('download', 'http_fallback')

    @property
    def is_incremental_mode_for_datasets(self):
        return self.get_data().getboolean('download', 'incremental_mode_for_datasets')

    @property
    def download_direct_http_timeout(self):
        return self.get_data().getint('download', 'direct_http_timeout')

    @property
    def download_async_http_timeout(self):
        return self.get_data().getint('download', 'async_http_timeout')

    @property
    def download_direct_db_timeout(self):
        return self.get_data().getint('download', 'direct_db_timeout')

    @property
    def download_async_db_timeout(self):
        return self.get_data().getint('download', 'async_db_timeout')

    @property
    def download_max_parallel_download(self):
        return self.get_data().getint('download', 'max_parallel_download')

    @property
    def download_max_parallel_download_per_datanode(self):
        return self.get_data().getint('download', 'max_parallel_download_per_datanode')

    @property
    def download_url_max_buffer_size(self):
        return self.get_data().getint('download', 'url_max_buffer_size')

    @property
    def download_streaming_chunk_size(self):
        value = self.get_data().get('download', 'streaming_chunk_size')
        try:
            validated = int(value)

        except ValueError:
            validated = 0

        return validated

    # SECTION : INDEX

    @property
    def index_indexes(self):
        return self.get_data().get('index', 'indexes')

    @property
    def index_default_index(self):
        return self.get_data().get('index', 'default_index')

    # SECTION : INTERFACE

    @property
    def interface_default_listing_size(self):
        return self.get_data().get('interface', 'default_listing_size')

    @property
    def is_interface_show_advanced_options(self):
        return self.get_data().getboolean('interface', 'show_advanced_options')

    @property
    def interface_dump_listing_limit_for_small_mode(self):
        return self.get_data().getint('interface', 'dump_listing_limit_for_small_mode')

    @property
    def interface_dump_listing_limit_for_medium_mode(self):
        return self.get_data().getint('interface', 'dump_listing_limit_for_medium_mode')

    @property
    def interface_dump_listing_limit_for_big_mode(self):
        return self.get_data().getint('interface', 'dump_listing_limit_for_big_mode')

    @property
    def interface_list_listing_limit_for_small_mode(self):
        return self.get_data().getint('interface', 'list_listing_limit_for_small_mode')

    @property
    def interface_list_listing_limit_for_medium_mode(self):
        return self.get_data().getint('interface', 'list_listing_limit_for_medium_mode')

    @property
    def interface_list_listing_limit_for_big_mode(self):
        return self.get_data().getint('interface', 'list_listing_limit_for_big_mode')

    @property
    def interface_search_listing_limit_for_small_mode(self):
        return self.get_data().getint('interface', 'search_listing_limit_for_small_mode')

    @property
    def interface_search_listing_limit_for_medium_mode(self):
        return self.get_data().getint('interface', 'search_listing_limit_for_medium_mode')

    @property
    def interface_search_listing_limit_for_big_mode(self):
        return self.get_data().getint('interface', 'search_listing_limit_for_big_mode')

    @property
    def interface_unicode_term(self):
        return self.get_data().get('interface', 'unicode_term')

    @property
    def is_interface_progress(self):
        if 'interface' in self.get_data().sections():
            res = self.get_data().getboolean('interface', 'progress')
        else:
            raise Exception(self.get_data().sections())
        return res

    # SECTION : LOCAL

    @property
    def locale_country(self):
        return self.get_data().get('locale', 'country')

    # SECTION : LOG

    @property
    def log_verbosity_level(self):
        return self.get_data().get('log', 'verbosity_level')

    @property
    def log_scheduler_profiling(self):
        return self.get_data().getboolean('log', 'scheduler_profiling')

    # SECTION : MODULE

    @property
    def is_module_download(self):
        return self.get_data().getboolean('module', 'download')

    # SECTION : API

    @property
    def api_esgf_search_chunksize(self):
        return self.get_data().getint('api', 'esgf_search_chunksize')

    @property
    def api_esgf_search_http_timeout(self):
        return self.get_data().getint('api', 'esgf_search_http_timeout')

    # SECTION : INSTALL

    @property
    def is_install_interactive(self):
        return self.get_data().getboolean('install', 'interactive')


if __name__ == '__main__':
    pass
