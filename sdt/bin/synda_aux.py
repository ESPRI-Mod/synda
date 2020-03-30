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

import argparse
import importlib
from sdt.bin.commons.utils import sdconst, sdi18n, syndautils
from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.utils import sdexception

# TODO These imports are probably deprecated.
from sdt.bin.commons.param import sddeferredbefore


def set_stream_type(args):
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
    # (dataset, file) for the listing type asked by user (i.e.We
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
    if args.type_ in (sdconst.SA_TYPE_AGGREGATION, sdconst.SA_TYPE_DATASET):
        sddeferredbefore.add_forced_parameter(args.stream, 'type', sdconst.SA_TYPE_DATASET)
    elif args.type_ in (sdconst.SA_TYPE_FILE,):
        sddeferredbefore.add_forced_parameter(args.stream, 'type', sdconst.SA_TYPE_FILE)
    else:
        raise sdexception.SDException('SDASYNDA-001', 'Unknown type (%s)' % args.type_)


def run():
    # creating the top-level parser
    main_parser = argparse.ArgumentParser(prog="synda",
                                          formatter_class=argparse.RawDescriptionHelpFormatter,
                                          add_help=False,
                                          description='ESGF downloader CLI tool.')
    main_parser.add_argument('-h', '--help',
                             action='help',
                             help="HELP TODO")
    main_parser.add_argument('-v', '--version',
                             action='version',
                             version='Synda {}'.format(sdconst.SYNDA_VERSION),
                             help='Current software version.')

    # Parent parser for subparsers that need selection.
    selection_parser = argparse.ArgumentParser(add_help=False)
    selection_parser.add_argument('-s', '--selection_file',
                                  metavar='TXT',
                                  default=None)

    # Parent parser for subparsers that need dry run option.
    dry_run_parser = argparse.ArgumentParser(add_help=False)
    dry_run_parser.add_argument('-z', '--dry-run', action='store_true')

    # Parent parser for autoremove flag remove_all that helps remove files from filesystem as well as the db.
    remove_all_parser = argparse.ArgumentParser(add_help=False)
    remove_all_parser.add_argument('--remove-all', action='store_true', default=False)

    # Parent parser for subparsers that need no default option.
    no_default_parser = argparse.ArgumentParser(add_help=False)
    no_default_parser.add_argument('-n', '--no_default',
                                   action='store_true',
                                   help='prevent loading default value')

    # Parent parser for subparsers that need non-interactive option.
    no_prompt_parser = argparse.ArgumentParser(add_help=False)
    no_prompt_parser.add_argument('-y', '--yes',
                                  action='store_true',
                                  help='assume "yes" as answer to all prompts and run non-interactively')

    # Parent parser for other parameters of the subparsers (i.e., facets, etc.).
    parameters_parser = argparse.ArgumentParser(add_help=False)
    parameters_parser.add_argument('parameters',
                                   nargs='*',
                                   default=[],
                                   help=sdi18n.m0001)

    parameter_parser = argparse.ArgumentParser(add_help=False)
    parameter_parser.add_argument('parameter',
                                  nargs='*',
                                  default=[],
                                  help=sdi18n.m0001)

    # Parent parser for other parameters of the subparsers (i.e., facets, etc.).
    time_period_parser = argparse.ArgumentParser(add_help=False)
    time_period_parser.add_argument('-L', '--timestamp_left_boundary',
                                    help='timestamp left limit')
    time_period_parser.add_argument('-R', '--timestamp_right_boundary',
                                    help='timestamp right limit')

    # Parent parser for subparsers that need incremental behavior (i.e., limit actions since last run).
    # TODO: investigate the feature, is it useful?
    incremental_parser = argparse.ArgumentParser(add_help=False)
    incremental_parser.add_argument('-i', '--incremental',
                                    action='store_true',
                                    help='Limit actions since last run')

    # Parent parser for subparsers that need playback or record option.
    playback_parser = argparse.ArgumentParser(add_help=False)

    # Parent parser for subcommand action:
    cert_action_parser = argparse.ArgumentParser(add_help=False)
    cert_action_parser.add_argument('action', choices=['renew', 'info', 'print'])

    cert_action_parser.add_argument('-d', '--debug', action='store_true', help='Display debug message')
    cert_action_parser.add_argument('-o', '--openid', help='ESGF openid')
    cert_action_parser.add_argument('-p', '--password', help='ESGF password')
    cert_action_parser.add_argument('-x', '--force_renew_ca_certificates', action='store_true',
                                    help='Force renew CA certificates')

    check_action_parser = argparse.ArgumentParser(add_help=False)
    check_action_parser.add_argument('action', choices=['selection', 'file_variable', 'dataset_version'])
    check_action_parser.add_argument('-F', '--output_format', help='Set output format', default='text',
                                     choices=['text', 'pdf'])
    check_action_parser.add_argument('-o', '--outfile', default='/tmp/dataset_version_report.pdf')

    daemon_action_parser = argparse.ArgumentParser(add_help=False)
    daemon_action_parser.add_argument('action', choices=['start', 'status', 'stop'])

    get_action_parser = argparse.ArgumentParser(add_help=False)
    get_action_parser.add_argument('--verify_checksum', '-c', action='store_true',
                                   help='Compare remote and local checksum')
    get_action_parser.add_argument('--dest_folder', '-d', default=sdconfig.files_dest_folder_for_get_subcommand,
                                   help='Destination folder')
    get_action_parser.add_argument('--force', '-f', action='store_true', help='Overwrite local file if exists')
    get_action_parser.add_argument('--network_bandwidth_test', '-n', action='store_true',
                                   help='Prevent disk I/O to measure network throughput. '
                                        'When this option is used, local file is set to /dev/null.')
    get_action_parser.add_argument('--openid', '-o', help='ESGF openid')
    get_action_parser.add_argument('--password', '-p', help='ESGF password')
    get_action_parser.add_argument('--quiet', '-q', action='store_true')
    get_action_parser.add_argument('--timeout', '-t',
                                   type=int,
                                   default=sdconst.DIRECT_DOWNLOAD_HTTP_TIMEOUT,
                                   help='HTTP timeout')
    get_action_parser.add_argument('--requests',
                                   '-req',
                                   action='store_true',
                                   help='Use requests instead of wget as HTTP client')
    get_action_parser.add_argument('--verbosity', '-v', action='count', default=1)
    get_action_parser.add_argument('--hpss', dest='hpss', action='store_true', help="Enable 'hpss' flag")
    get_action_parser.add_argument('--no-hpss', dest='hpss', action='store_false', help="Disable 'hpss' flag (Default)")
    get_action_parser.set_defaults(hpss=False)

    group = playback_parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-p', '--playback',
                       help='Read metadata from file',
                       metavar='FILE')
    group.add_argument('-r', '--record',
                       help='Write metadata to file',
                       metavar='FILE')

    # Instanciate subparsers.
    subparsers = main_parser.add_subparsers(dest='subcommand',
                                            metavar='subcommand',
                                            help='Synda subcommand list')

    # Subparser for install subcommand.
    install = subparsers.add_parser('install',
                                    help='Download dataset (async)',
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    parents=[selection_parser,
                                             dry_run_parser,
                                             no_default_parser,
                                             no_prompt_parser,
                                             incremental_parser,
                                             parameters_parser,
                                             time_period_parser,
                                             playback_parser])
    # Subparser for the intro subcommand
    intro = subparsers.add_parser('intro',
                                  help='Prints an introduction to the synda command line toolbox.')

    # Subparser for the autoremove subcommand
    autoremove = subparsers.add_parser('autoremove',
                                       help='Remove old versions for datasets',
                                       parents=[selection_parser,
                                                no_default_parser,
                                                dry_run_parser,
                                                remove_all_parser,
                                                ])
    # Subparser for the certificate subcommand
    certificate = subparsers.add_parser('certificate',
                                        help='Renews certificate if needed, prints certificate or shows information',
                                        parents=[cert_action_parser])

    # Subparser for the check subcommand
    check = subparsers.add_parser('check',
                                  help='Checks correctness and consistency of dataset version numbers in all '
                                       'dataset versions( or, if search parameters are given, '
                                       'those that match those parameters).',
                                  parents=[check_action_parser,
                                           parameters_parser,
                                           dry_run_parser])
    # Subparser for the contact subcommand
    contact = subparsers.add_parser('contact', help='Prints contact information')

    # Subparser for the config subcommand
    config = subparsers.add_parser('config', help='Prints configuration')

    # Subparser for the retry subcommand
    retry = subparsers.add_parser('retry', help='Prints configuration')

    # Subparser for the watch subcommand
    watch = subparsers.add_parser('watch', help='Shows the daemon ongoing downloads')

    # Subparser for the queue subcommand
    queue = subparsers.add_parser('queue', help='Shows the queue in its current state')
    queue.add_argument('project', help='Specific project queue', default=None, nargs='?')

    # Subparser for the daemon subcommand
    daemon = subparsers.add_parser('daemon',
                                   help=sdi18n.m0023,
                                   parents=[daemon_action_parser])

    # Subparser for the facet subcommand
    facet = subparsers.add_parser('facet', help='Facet discovery')
    facet.add_argument('facet_name', help='Facet name')

    # Subparser for the get subcommand
    get = subparsers.add_parser('get',
                                help='Download data synchronously',
                                parents=[get_action_parser,
                                         parameter_parser,
                                         selection_parser,
                                         dry_run_parser])
    # Subparser for the history subcommand
    subparser = subparsers.add_parser('history', help='Shows history')

    # Subparser for the metric subcommand
    subparser = create_subparser('metric', selection=False, no_default=False,
                                 help='Display performance and disk usage metrics')
    subparser.add_argument('--groupby', '-g', choices=['data_node', 'project', 'model'], default='data_node',
                           help='Group-by clause')
    subparser.add_argument('--metric', '-m', choices=['rate', 'size'], default='rate', help='Metric name')
    subparser.add_argument('--project', '-p', default='CMIP5',
                           help="Project name (must be used with '--groupby=model' else ignored)")

    args = main_parser.parse_args()

    # Start processing user subcommands
    if args.subcommand == sdconst.SUBCOMMANDS['setup']:
        print('Setting up environment...')

        # -- permission check -- #
        # TODO: check is it still necessary?
        #   if args.subcommand in (sdconst.ADMIN_SUBCOMMANDS):
        #       if not sdpermission.is_admin():
        #           sdtools.print_stderr(sdi18n.m0028)
        #           sys.exit(1)

        # -- subcommand routing -- #
        # TODO shift this code to the help in the main parser
        # if args.subcommand == 'help':
        #
        #     if args.topic is None:
        #         parser.print_help()
        #     else:
        #         if args.topic in subparsers.choices:
        #             subparsers.choices[args.topic].print_help()
        #         else:
        #             sdtools.print_stderr('Help topic not found ({})'.format(args.topic))
        #
        #     sys.exit(0)

        # TODO Check parameter.expolde treatment
        # hack to explode id in individual facets (experimental)
        # if args.subcommand == 'search':
        #     if args.explode:
        #         if len(args.parameter) > 0:
        #             id_ = args.parameter[0]
        #             id_ = id_.split('=')[
        #                 1] if '=' in id_ else id_  # if id_ is in the form 'k=v', we strip 'k='. We assume here that '=' character doesn't appear in key nor value.
        #             delim = '/' if '/' in id_ else '.'
        #             li = id_.split(delim) + args.parameter[
        #                                     1:]  # this allow to add other parameter after id e.g. 'synda search <master_id> <version>'
        #             args.parameter = li

        # TODO: check to instanciate stream when necessary only
        stream = syndautils.get_stream(subcommand=args.subcommand,
                                       parameter=args.parameters,
                                       selection_file=args.selection_file,
                                       no_default=args.no_default)

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
        if args.subcommand in ('show', 'version'):
            args.type_ = None

        # infer type if not set by user
        if args.type_ is None:
            args.type_ = sdtype.infer_display_type(stream)

        args.stream = stream  # TODO: pass 'stream' object downstream as a standalone argument (not inside args)

        set_stream_type(args)

    mod = importlib.import_module('actions.{}'.format(args.subcommand))
    mod.run(args)


if __name__ == '__main__':
    run()
