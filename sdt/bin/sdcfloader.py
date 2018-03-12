#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains configuration files READ routines.

Note
    'sdcfloader' means 'SynDa Configuration Files LOADER'
"""

import os
import argparse
import ConfigParser
import sdtools

def load(configuration_file,credential_file):

    config = ConfigParser.ConfigParser(default_options)

    config.read(configuration_file)
    config.read(credential_file)

    return config

# init.

# TODO: replace default options DICTIONNARY below with a default options FILE
# (pb with options below is that they are available in all sections)
default_options={'max_parallel_download':'8',
                 'user':'',
                 'group':'',
                 'hpss':'0',
                 'download':'true',
                 'post_processing':'false',
                 'globustransfer':'false',
                 'data_path':'',
                 'sandbox_path':'',
                 'db_path':'',
                 'default_path':'',
                 'selection_path':'',
                 'security_dir_mode':'tmpuid',
                 'metadata_server_type':'esgf_search_api',
                 'unicode_term':'0',
                 'progress':'1',
                 'onemgf':'false',
                 'ignorecase':'true',
                 'default_listing_size':'small',
                 'http_fallback':'false',
                 'gridftp_opt':'',
                 'check_parameter':'1',
                 'verbosity_level':'info',
                 'scheduler_profiling':'0',
                 'lfae_mode':'abort',
                 'indexes':'esgf-node.ipsl.fr,esgf-data.dkrz.de,esgf-index1.ceda.ac.uk',
                 'default_index':'esgf-node.ipsl.fr',
                 'nearest':'false',
                 'nearest_mode':'geolocation',
                 'openid':'https://esgf-node.ipsl.fr/esgf-idp/openid/foo',
                 'password':'foobar',
                 'incorrect_checksum_action':'remove'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ini_file','-i',help='Test ConfigParser')
    args = parser.parse_args()

    config = ConfigParser.ConfigParser(default_options)
    config.read(args.ini_file)

    print config.get('post_processing','username')
