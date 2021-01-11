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
import ConfigParser


def get_parser(fullfilename, default_options):
    parser = ConfigParser.ConfigParser(default_options)
    if os.path.isfile(fullfilename):
        parser.read(fullfilename)
    return parser


if __name__ == '__main__':
    pass
