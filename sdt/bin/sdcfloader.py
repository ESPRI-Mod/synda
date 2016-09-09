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

def load(configuration_file,credential_file,user_configuration_file,user_credential_file,special_user=True):

    config = ConfigParser.ConfigParser(default_options)

    # load system-wide options
    load_param(config,configuration_file)
    load_credential(config,credential_file,special_user)

    # per-user options override global options
    if not sdtools.is_daemon(): # daemon only use global options. Currently, there is only one daemon per machine, but this may change in the future (i.e. maybe remove sysv/systemd service and allow one daemon per user). TAG43J2K253J43
        load_user_param(config,user_configuration_file)

        if not special_user: # for now, with 'special user', 'machine-wide' credential cannot be overrided by 'per-user' credential. This may change in the future.
            load_user_credential(config,user_credential_file)

    return config

def load_param(config,f):
    config.read(f)

def load_credential(config,f,special_user):
    if special_user:
        config.read(f)

def load_user_param(config,f):
    if os.path.exists(f):
        config.read(f)

def load_user_credential(config,f):
    if os.path.exists(f):
        config.read(f)

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
                 'unicode_term':'0',
                 'progress':'1',
                 'onemgf':'false',
                 'ignorecase':'true',
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
