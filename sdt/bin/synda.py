#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""'synda' command (front-end to Synda main commands).

Notes
    - in this file, most module import directives are moved near the calls, so to improve startup time (even for sdapp).
    - do not import 'sdlog' at the beggining of this file, because in this case, it breaks the daemon startup (i.e. double-fork problem) !
    - do not put a dry_run test here (sdtiaction's funcs are called from other place too, so the dry_run test need to be done inside sdtiaction's funcs)
"""

import sys
import argparse
import sdconst
import sdi18n
#import sdaction
#import sdsubparser
from sdtools import DefaultHelpParser,print_stderr

"""
def exec_action(args):
    method = getattr(sdaction, args.subparser_name)
    result = method()
"""

def set_stream_type(args):
    import sddeferredbefore

    # Set the sdtream type (aka search-API 'type').
    #
    # Note that arg.type_ is NOT the same thing as the stream type (aka
    # search-API type). arg.type_ is only used locally to format the
    # listing presented to user, while the stream type is the one sent
    # to the ESGF service to retrieve data. For example,
    # SA_TYPE_AGGREGATION is used by arg.type_ to make some change in
    # the output, but search-API don't know about this type (i.e. for
    # most project, you can't list anything by using this type). Also
    # most modules of Synda behave the same way as search-API: they
    # don't know about SA_TYPE_AGGREGATION. SA_TYPE_AGGREGATION is ONLY
    # used in Synda upstream code to make some local display
    # modifications.
    #
    # So what we do here is choose which is the search-API type we need
    # (dataset, file) for the listing type asked by user (i.e.
    # variable, dataset, file)
    #
    # But note that in most case, search-API 'type' will be overrided
    # later anyway as it is forced in dedicated modules (e.g. in
    # sdrdataset, sdrfile, etc..).
    #
    # Also note that we 'force' (i.e. not 'default') the parameter
    # here, so to prevent user to set it. We do this because if user
    # use '-f' option and type=Dataset, it will not do as the display
    # type will not fit the type of data fetched from search-API).
    #
    if args.type_ in (sdconst.SA_TYPE_AGGREGATION,sdconst.SA_TYPE_DATASET):
        sddeferredbefore.add_forced_parameter(args.stream,'type',sdconst.SA_TYPE_DATASET)
    elif args.type_ in (sdconst.SA_TYPE_FILE,):
        sddeferredbefore.add_forced_parameter(args.stream,'type',sdconst.SA_TYPE_FILE)
    else:
        from sdexception import SDException
        raise SDException('SDASYNDA-001','Unknown type (%s)'%args.type_)

if __name__ == '__main__':

    # create the top-level parser
    parser = DefaultHelpParser(formatter_class=argparse.RawTextHelpFormatter)

    # NEW WAY
    #subparsers = parser.add_subparsers(dest='subparser_name')

    parser.add_argument('action',nargs='?',help=sdi18n.m0015)

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

    parser.add_argument('-C','--column',type=lambda s: s.split(','),default=[],help="set column(s) to be used with 'dump' action")
    parser.add_argument('-F','--format',choices=['raw','line','indent'],default='raw',help="set format to be used with 'dump' action")
    parser.add_argument('-l','--localsearch',action='store_true',help='search in local data repository (already installed dataset)')
    parser.add_argument('-n','--no_default',action='store_true',help='prevent loading default value')
    parser.add_argument('-N','--non_interactive',action='store_true',help='assume "yes" as answer to all prompts and run non-interactively (useful in cron jobs)')
    parser.add_argument('-r','--replica',action='store_true',help='show replica')
    parser.add_argument('-R','--raw_mode',action='store_true',help='dump original metadata')
    parser.add_argument('-s','--selection',default=None)
    parser.add_argument('-V','--version',action='store_true') # beware: version exist both as option and as action
    parser.add_argument('-y','--dry_run',action='store_true')

    type_grp=parser.add_argument_group(None)
    type_grp.add_argument('-a','--aggregation',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)
    type_grp.add_argument('-d','--dataset',dest='type_',action='store_const',const=sdconst.SA_TYPE_DATASET)
    type_grp.add_argument('-f','--file',dest='type_',action='store_const',const=sdconst.SA_TYPE_FILE)
    type_grp.add_argument('-v','--variable',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)

    # NEW WAY
    # create parser for sub-commands
    #sdsubparser.run(subparsers)

    args = parser.parse_args()

    if args.version:
        import sdapp
        print sdapp.version
        sys.exit(0)

    # check type mutex
    #
    # There is no way to check mutex as 'dest' argparse feature is used. Maybe
    # use add_mutually_exclusive_group(), but currently, doing so makes the
    # help look ugly. So better leave it as is until argparse handle this case
    # smoothly.

    # NEW WAY
    #import sdtiaction
    #sdtiaction.actions[args.action](args)
    #exec_action(args)

    if args.action in ['autoremove','cache','certificate','daemon','history','param','queue','replica','reset','retry','selection','test','update','upgrade','watch']:
        import sdtiaction
        sdtiaction.actions[args.action](args)
    elif args.action=='help':
        parser.print_help()
    elif args.action in ['dump','list','search','show','version']:
        import syndautils

        stream=syndautils.get_stream(args)

        # set default type
        if args.type_ is None:
            import sdtype
            args.type_=sdtype.infer_display_type(stream)

        args.stream=stream # hack: pass 'stream' object downstream as a standalone argument (not inside args)

        set_stream_type(args)

        import sdtsaction
        sdtsaction.actions[args.action](args)

    elif args.action in ['remove','install','stat']:
        import sdstream, sddeferredbefore, syndautils

        stream=syndautils.get_stream(args)

        # those actions systematically trigger full search (i.e. limit keyword cannot be used here)

        if args.action in ['remove','install']:
            syndautils.check_daemon()

        if sdstream.is_empty(stream):
            print 'No packages will be installed, upgraded, or removed.'
            sys.exit(0)

        # Set the sdtream type.
        # Note that we 'force' (i.e. not 'default') the parameter here, so to prevent user to set it
        # (i.e. the type is always SA_TYPE_FILE when we are here).
        sddeferredbefore.add_forced_parameter(stream,'type',sdconst.SA_TYPE_FILE)

        import sdsearch
        files=sdsearch.run(stream=stream,dry_run=args.dry_run)

        import sdtiaction
        sdtiaction.actions[args.action](files,args)
    else:
        print_stderr('Invalid operation %s'%args.action)   
        print_stderr("Use '--help' option for more info")
        #parser.print_help()
        sys.exit(2)
