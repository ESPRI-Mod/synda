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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    create_credential_file_sample('/tmp/test_sdt_cred.ini')
