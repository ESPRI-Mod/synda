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
                "#   This file contains advanced synda parameters",
            ),
            "{}\n".format(
                "# Documentation",
            ),
            "{}\n".format(
                "#   Parameters documentation can be found at",
            ),
            "{}\n".format(
                "#   https://github.com/Prodiguer/synda/tree/master/synda/doc/advanced_configuration_reference.md",
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

        config.add_section('logger')

        config.set('logger', 'feeder_name', 'feeder')
        config.set('logger', 'consumer_name', 'consumer')
        config.set('logger', 'domain_name', 'domain')
        config.set('logger', 'feeder_file', 'discovery.log')
        config.set('logger', 'consumer_file', 'transfer.log')
        config.set('logger', 'domain_file', 'domain.log')

        config.add_section('checksum')

        config.set('checksum', 'type_md5', 'md5')
        config.set('checksum', 'type_sha256', 'sha256')

        config.add_section('api')

        config.set('api', 'esgf_search_domain_name', 'IDXHOSTMARK')

        config.add_section('processes')

        config.set('processes', 'chunksize', '5000')
        config.set('processes', 'http_client', 'aiohttp')
        config.set('processes', 'transfer_protocol', 'http')
        config.set('processes', 'get_files_caching', 'true')

        config.add_section('hack')
        config.set('hack', 'projects_with_one_variable_per_dataset', 'CORDEX, CMIP6')

        with open(full_filename, 'w') as fh:
            for line in header:
                fh.write(line)
            config.write(fh)
