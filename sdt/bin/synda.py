#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""'synda' command (front-end to Synchro-data main commands).

Note
    - In this file, module import directives are moved near the calls,
      so to improve startup time (even for sdapp).
"""

import sys
import argparse
import sdconst
import sdi18n
from sdtools import DefaultHelpParser,print_stderr

if __name__ == '__main__':
    parser = DefaultHelpParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('action',help=sdi18n.m0015)

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

    parser.add_argument('-F','--format',choices=['raw','line','indent'],default='indent',help="set format to be used with 'dump' action")
    parser.add_argument('-l','--localsearch',action='store_true',help='search in local data repository (already installed dataset)')
    parser.add_argument('-n','--no_default',action='store_true',help='prevent loading default value')
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

    args = parser.parse_args()

    if args.version:
        import sdapp
        print sdapp.version

    # check type mutex
    #
    # There is no way to check mutex as 'dest' argparse feature is used. Maybe
    # use add_mutually_exclusive_group(), but currently, doing so makes the
    # help look ugly. So better leave it as is until argparse handle this case
    # smoothly.

    # check action
    if args.action not in ['autoremove','cache','certificate','daemon','dump','history','install','list','param','queue','remove','replica','reset','retry','search','show','stat','test','update','upgrade','version','watch']:
        print_stderr('Invalid operation %s'%args.action)   
        parser.print_help()
        sys.exit(2)

    if args.action in ['autoremove','cache','certificate','daemon','history','queue','replica','reset','retry','selection','test','upgrade','watch']:
        import sdtiaction
        sdtiaction.actions[args.action](args)
    elif args.action=='update':
        print_stderr('Not implemented yet.')   
    elif args.action=='param':
        import sdparam
        sdparam.main(args.parameter) # tricks to re-use sdparam CLI parser
    else:
        import sdbuffer, sdparse, sdstream, sdconfig, sddeferredbefore

        buffer=sdbuffer.get_selection_file_buffer(parameter=args.parameter,path=args.selection)
        selection=sdparse.build(buffer,load_default=(not args.no_default))
        stream=selection.to_stream()

        # Set default value for nearest here
        #
        # TODO: make it work with all actions (e.g. search) as it only working for 'install' action for now
        #
        #sddeferredbefore.add_default_parameter(stream,'nearest',True) # TODO: why this one is not working ?
        if sdconfig.config.getboolean('behaviour','nearest'):
            sdstream.set_scalar(stream,'nearest',True)

        # progress
        if sdconfig.config.getboolean('interface','progress'):
            sdstream.set_scalar(stream,'progress',True)

        if args.action in ['dump','list','search','show','version']:

            # Set default type
            if args.type_ is None:
                import sdtype
                args.type_=sdtype.infer_display_type(stream)

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
                sddeferredbefore.add_forced_parameter(stream,'type',sdconst.SA_TYPE_DATASET)
            elif args.type_ in (sdconst.SA_TYPE_FILE,):
                sddeferredbefore.add_forced_parameter(stream,'type',sdconst.SA_TYPE_FILE)
            else:
                from sdexception import SDException
                raise SDException('SDASYNDA-001','Unknown type (%s)'%args.type_)

            args.stream=stream # hack: pass 'stream' object downstream as a standalone argument (not inside args)

            import sdtsaction
            sdtsaction.actions[args.action](args)

        elif args.action in ['remove','install','stat']:
            # those actions systematically trigger full search (i.e. limit keyword cannot be used here)

            # check
            if sdconfig.prevent_daemon_and_modification:
                if args.action in ['remove','install']:
                    import sddaemon
                    if sddaemon.is_running():
                        print 'The daemon must be stopped before installing/removing dataset'
                        sys.exit(3)

            if sdstream.is_empty(stream):
                print 'No packages will be installed, upgraded, or removed.'
            else:

                # memo tuning: until this point, it go fast

                # Set the sdtream type.
                # Note that we 'force' (i.e. not 'default') the parameter here, so to prevent user to set it
                # (i.e. the type is always SA_TYPE_FILE when we are here).
                sddeferredbefore.add_forced_parameter(stream,'type',sdconst.SA_TYPE_FILE)

                import sdsearch
                files=sdsearch.run(stream=stream,dry_run=args.dry_run)

                for f in files:
                    import sdlog # do NOT import 'sdlog' at the beggining of this file, because in this case, it breaks the daemon startup (i.e. double-fork problem) !
                    sdlog.debug("SDASYNDA-002","%s"%f['url'],stdout=True)

                # note: do not put a dry_run test here
                #       (sdtiaction's funcs are called from other place too, so the dry_run test need to be done inside sdtiaction's funcs)

                import sdtiaction
                sdtiaction.actions[args.action](files,args)
        else:
            # we shouldn't be here

            assert False

