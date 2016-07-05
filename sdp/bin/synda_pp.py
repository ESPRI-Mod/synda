#!/usr/bin/env python -W ignore
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""'synda_pp' command.

Note
    Remove '-W ignore' once only Python 2.7+. TAG5J43K
"""

import sys
import argparse
import spapp
import spsubparser
import sptools
import spsubcommand

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='subcommand',metavar='subcommand')
    parser.add_argument('-V','--version',action='version',version=spapp.version)
    spsubparser.run(subparsers)
    args = parser.parse_args()

    if args.subcommand=='help':

        if args.topic is None:
            parser.print_help()
        else:
            if args.topic in subparsers.choices:
                subparsers.choices[args.topic].print_help()
            else:
                sptools.print_stderr('Help topic not found (%s)'%args.topic)

        sys.exit(0)

    if args.subcommand in spsubcommand.subcommands.keys():
        status=spsubcommand.subcommands[args.subcommand](args)
        sys.exit(status)

    sptools.print_stderr('Invalid operation %s'%args.subcommand)   
    sptools.print_stderr("Use '--help' option for more info")
    sys.exit(2)
