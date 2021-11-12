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
import configparser


class Create(object):

    def __init__(self, full_filename):

        header = [
            "{}\n".format(
                "# Description",
            ),
            "{}\n".format(
                "#   This file contains synda parameters",
            ),
            "{}\n".format(
                "# Documentation",
            ),
            "{}\n".format(
                "#   Parameters documentation can be found at",
            ),
            "{}\n".format(
                "#   https://github.com/Prodiguer/synda/tree/master/synda/doc/configuration_parameter_reference.md",
            ),
            "{}\n".format(
                "# Notes",
            ),
            "{}\n".format(
                "#   - Line comments using leading '#' or ';' are supported in this file",
            ),
            "{}\n".format(
                "#   - Trailing comment are not supported in this file",
            ),
            "{}\n".format(
                "",
            ),
        ]

        config = configparser.ConfigParser()

        config.add_section('daemon')
        config.set('daemon', 'user', '')
        config.set('daemon', 'group', '')

        config.add_section('module')
        config.set('module', 'download', 'true')

        config.add_section('log')
        config.set('log', 'verbosity_level', 'info')
        config.set('log', 'scheduler_profiling', '0')

        config.add_section('core')
        config.set('core', 'security_dir_mode', 'tmpuid')
        config.set('core', 'metadata_server_type', 'esgf_search_api')
        config.set('core', 'selection_path', '')
        config.set('core', 'default_path', '')
        config.set('core', 'data_path', '')
        config.set('core', 'db_path', '')
        config.set('core', 'sandbox_path', '')

        config.add_section('interface')
        config.set('interface', 'unicode_term', '0')
        config.set('interface', 'progress', '0')
        config.set('interface', 'default_listing_size', 'small')

        config.set('interface', 'dump_listing_limit_for_small_mode', '50')
        config.set('interface', 'dump_listing_limit_for_medium_mode', '100')
        config.set('interface', 'dump_listing_limit_for_big_mode', '6000')

        config.set('interface', 'list_listing_limit_for_small_mode', '20')
        config.set('interface', 'list_listing_limit_for_medium_mode', '200')
        config.set('interface', 'list_listing_limit_for_big_mode', '20000')

        config.set('interface', 'search_listing_limit_for_small_mode', '100')
        config.set('interface', 'search_listing_limit_for_medium_mode', '1000')
        config.set('interface', 'search_listing_limit_for_big_mode', '6000')

        config.set('interface', 'show_advanced_options', 'false')

        config.add_section('behaviour')
        config.set('behaviour', 'onemgf', 'false')
        config.set('behaviour', 'check_parameter', '0')
        config.set('behaviour', 'ignorecase', 'true')
        config.set('behaviour', 'nearest', 'false')
        config.set('behaviour', 'nearest_mode', 'geolocation')
        config.set('behaviour', 'lfae_mode', 'abort')
        config.set('behaviour', 'incorrect_checksum_action', 'remove')

        config.add_section('index')
        config.set('index', 'indexes', 'esgf-data.dkrz.de')
        config.set('index', 'default_index', 'esgf-data.dkrz.de')

        config.add_section('locale')
        config.set('locale', 'country', '')

        config.add_section('download')
        config.set('download', 'max_parallel_download', '8')
        # config.set('download', 'max_parallel_download_per_datanode', '8')
        # config.set('download', 'get_only_latest_version', 'true')
        config.set('download', 'hpss', '1')
        config.set('download', 'http_fallback', 'false')
        config.set('download', 'gridftp_opt', '')
        # config.set('download', 'incremental_mode_for_datasets', 'false')
        config.set('download', 'continue_on_cert_errors', 'false')
        config.set('download', 'url_max_buffer_size', '3500')

        # nouvelles variables

        config.set('download', 'direct_http_timeout', '30')
        config.set('download', 'async_http_timeout', '120')

        # 2 mn
        config.set('download', 'direct_db_timeout', '120')
        # 200mn # TODO maybe use 86400 / 24h here
        config.set('download', 'async_db_timeout', '12000')

        config.add_section('api')

        # Maximum files number returned by one search-api call.
        #
        # Normally, max is 10000 so it should be set to 10000.
        # But in some case, when set to 10000, the following strange behaviour occurs:
        # the url below
        # http://esgf-data.dkrz.de/esg-search/search?fields=instance_id,timestamp&replica=false&type=Dataset&format=application%2Fsolr%2Bxml&limit=10000&offset=8900
        # gives this
        # <result name="response" numFound="11782" start="8900" maxScore="1.0">
        # instead of this
        # <result name="response" numFound="314345" start="8900" maxScore="1.0">
        # It seems to be of bug on the server side.
        #
        # So from now, it's set to 9000
        config.set('api', 'esgf_search_chunksize', '9000')
        # HTTP timeout (time to wait for HTTP response)
        config.set('api', 'esgf_search_http_timeout', '300')

        with open(full_filename, 'w') as fh:
            for line in header:
                fh.write(line)
            config.write(fh)
