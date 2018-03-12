#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains configuration files WRITE routines.

Note
    'sdcfbuilder' means 'SynDa Configuration Files BUILDER'
"""

import os
import argparse
import ConfigParser

def create_credential_file_sample(path):

    config = ConfigParser.ConfigParser()

    config.add_section('esgf_credential')
    config.set('esgf_credential', '#openid', 'https://esgf-node.ipsl.fr/esgf-idp/openid/foo')
    config.set('esgf_credential', '#password', 'foobar')

    with open(path, 'w') as fh:
        config.write(fh)

def create_configuration_file_sample(path):

    config = ConfigParser.ConfigParser()

    config.add_section('daemon')
    config.set('daemon', 'user', '')
    config.set('daemon', 'group', '')

    config.add_section('module')
    config.set('module', 'download', 'true')
    config.set('module', 'post_processing', 'false')
    config.set('module', 'globustransfer', 'false')

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
    config.set('download', 'hpss', '1')
    config.set('download', 'http_fallback', 'false')
    config.set('download', 'gridftp_opt', '')

    config.add_section('post_processing')
    config.set('post_processing', 'host', 'localhost')
    config.set('post_processing', 'port', '18290')

    config.add_section('globustransfer')
    config.set('globustransfer', 'esgf_endpoints', '/esg/config/esgf_endpoints.xml')
    config.set('globustransfer', 'destination_endpoint', 'destination#endpoint')

    with open(path, 'w') as fh:
        config.write(fh)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    create_credential_file_sample('/tmp/test_sdt_cred.ini')
