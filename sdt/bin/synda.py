#!/usr/bin/env python -W ignore
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
    - in this file, most module import directives are moved near the calls, so
      to improve startup time.
    - do not import 'sdlog' at the beginning of this file, because in this
      case, it breaks the daemon startup (i.e. double-fork problem) !
    - do not put a dry_run test here (sdtiaction's funcs are called from other
      place too, so the dry_run test need to be done inside sdtiaction's funcs)
    - remove '-W ignore' once only Python 2.7+. TAG5J43K
"""

import sys
import argparse
import sdapp
import sdconst
import sdi18n
import sdsubparser
import sdtools
import sdconfig
import sdpermission
import sdexception

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
    # Also note that we 'force' (i.e. not 'default') the parameter here, so to
    # prevent user to set it. We do this because if user use '-f' option and
    # type=Dataset, the display type will not fit the type of data fetched from
    # search-API).
    #
    if args.type_ in (sdconst.SA_TYPE_AGGREGATION,sdconst.SA_TYPE_DATASET):
        sddeferredbefore.add_forced_parameter(args.stream,'type',sdconst.SA_TYPE_DATASET)
    elif args.type_ in (sdconst.SA_TYPE_FILE,):
        sddeferredbefore.add_forced_parameter(args.stream,'type',sdconst.SA_TYPE_FILE)
    else:
        raise sdexception.SDException('SDASYNDA-001','Unknown type (%s)'%args.type_)

if __name__ == '__main__':

    # create the top-level parser
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    #parser = sdtools.DefaultHelpParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=sdi18n.m0016)

    subparsers = parser.add_subparsers(dest='subcommand',metavar='subcommand') # ,help=sdi18n.m0015

    parser.add_argument('-V','--version',action='version',version=sdapp.version) # beware: version exist both as option and as subcommand

    # create parser for sub-commands
    sdsubparser.run(subparsers)

    args = parser.parse_args()

    # check type mutex
    #
    # There is no way to check mutex as 'dest' argparse feature is used. Maybe
    # use add_mutually_exclusive_group(), but currently, doing so makes the
    # help looks ugly. So better leave it as is until argparse handle this case
    # smoothly.

    # -- permission check -- #

    if args.subcommand in (sdconst.ADMIN_SUBCOMMANDS):
        if not sdpermission.is_admin():
            sdtools.print_stderr(sdi18n.m0027)
            sys.exit(1)

    # -- subcommand routing -- #

    if args.subcommand=='help':

        if args.topic is None:
            parser.print_help()
        else:
            if args.topic in subparsers.choices:
                subparsers.choices[args.topic].print_help()
            else:
                sdtools.print_stderr('Help topic not found (%s)'%args.topic)

        sys.exit(0)


    import sdtsaction
    if args.subcommand in sdtsaction.actions.keys():
        import syndautils

        # hack to explode id in individual facets (experimental)
        if args.subcommand=='search':
            if args.explode:
                if len(args.parameter)>0:
                    id_=args.parameter[0]
                    id_=id_.split('=')[1] if '=' in id_ else id_ # if id_ is in the form 'k=v', we strip 'k='. We assume here that '=' character doesn't appear in key nor value.
                    delim='/' if '/' in id_ else '.'
                    li=id_.split(delim)+args.parameter[1:] # this allow to add other parameter after id e.g. 'synda search <master_id> <version>'
                    args.parameter=li

        stream=syndautils.get_stream(subcommand=args.subcommand,parameter=args.parameter,selection_file=args.selection_file,no_default=args.no_default)


        # hack for 'show' and 'version' subcommands.
        #
        # description
        #     this hack normalize 'show' and 'version' subcommands 'type_'
        #     attribute with other type_ sensitive subcommands. Without this
        #     hack, the next statement (i.e. "if args.type_ is None:") fails with
        #     "AttributeError: 'Namespace' object has no attribute 'type_'".
        #
        # notes
        #     - show and version subcommands type_ attribute is already strictly
        #       defined by the parameter argument (e.g. dataset identifier, file
        #       identifier, etc..), so we dont want the user to also be able to
        #       set type_ attribute using options. This is why type_ group is not
        #       present for show and version subcommands (see subparser module
        #       for details).
        #     - another way to normalize is to use "parser.set_defaults(type_=None)"
        #
        if args.subcommand in ('show','version'):
            args.type_=None


        # infer type if not set by user
        if args.type_ is None:
            import sdtype
            args.type_=sdtype.infer_display_type(stream)

        args.stream=stream # TODO: pass 'stream' object downstream as a standalone argument (not inside args)

        set_stream_type(args)

        status=sdtsaction.actions[args.subcommand](args)

        # hack
        # TODO: review all return code in sdtsaction module
        if not isinstance(status,int):
            status=0 # arbitrary

        sys.exit(status)

    import sdtiaction
    if args.subcommand in sdtiaction.actions.keys():
        status=sdtiaction.actions[args.subcommand](args)

        # hack
        # TODO: review all return code in sdtiaction module
        if not isinstance(status,int):
            status=0 # arbitrary

        sys.exit(status)

    sdtools.print_stderr('Invalid operation %s'%args.subcommand)   
    sdtools.print_stderr("Use '--help' option for more info")
    #parser.print_help()
    sys.exit(2)
