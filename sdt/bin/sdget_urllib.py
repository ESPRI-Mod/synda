#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains urllib based download routine."""

import os
import sys
import json
import argparse
import sdapp
import sdnetutils

def download_file(url,full_local_path,checksum_type):
    (status,local_checksum)=sdnetutils.download_file(url,full_local_path,checksum_type)

    return (status,local_checksum)

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    sys.exit(0)
