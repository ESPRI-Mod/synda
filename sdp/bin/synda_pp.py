#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""'synda_pp' command.
"""

import sys
import argparse
import spapp
import spsubparser
import sptools

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='subcommand',metavar='subcommand')
    parser.add_argument('-V','--version',action='version',version=sdapp.version)
    sdsubparser.run(subparsers)
    args = parser.parse_args()

    # -- subcommand routing -- #

    if args.subcommand=='help':

        if args.topic is None:
            parser.print_help()
        else:
            if args.topic in subparsers.choices:
                subparsers.choices[args.topic].print_help()
            else:
                sptools.print_stderr('Help topic not found (%s)'%args.topic)

        sys.exit(0)

    import sdtsaction
    if args.subcommand in spaction.actions.keys():
        sdtsaction.actions[args.subcommand](args)
        status=sdtiaction.actions[args.subcommand](args)

        # hack
        # TODO: review all return code in sdtiaction module
        if not isinstance(status,int):
            status=0 # arbitrary

        sys.exit(status)

    sptools.print_stderr('Invalid operation %s'%args.subcommand)   
    sptools.print_stderr("Use '--help' option for more info")
    sys.exit(2)
