#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains actions specific parsers used by 'synda' script."""

import argparse
from synda.sdt import sdi18n
from synda.sdt import sdcliex
from synda.sdt import sdprint
from synda.sdt import sdcommonarg
from synda.sdt import sddescription

from synda.source.config.subcommand.argument.constants import DEFAULT_DEST_FOLDER_PARSER_ARGUMENT

from synda.source.config.subcommand.constants import get_default_limit


def add_lsearch_option(parser):
    parser.add_argument(
        '-l',
        '--localsearch',
        action='store_true',
        help='search in local data repository (already installed dataset)',
    )


def add_verbose_option(parser):
    # TODO: use this => parser.add_argument('--verbosity','-v', action='count', default=0)
    # '-v' not used to prevent collision
    parser.add_argument(
        '--verbose', action='store_true', help='verbose mode')


# 'ni' means 'Non-Interactive'

def add_ni_option(parser):
    parser.add_argument(
        '-y',
        '--yes',
        action='store_true',
        help='assume "yes" as answer to all prompts and run non-interactively',
    )


def add_incremental_mode_argument(parser, subc):
    if subc == 'stat':
        msg = 'Limit action on files which appeared since last run (experimental)'
    else:
        msg = 'Install files which appeared since last run (experimental)'

    parser.add_argument(
        '-i', '--incremental', action='store_true', help=msg,
    )


def add_timestamp_boundaries(parser, show_advanced_options, hidden=True):

    # default is to hide everything (advanced options are not shown by default)
    left_limit_help_msg = argparse.SUPPRESS
    right_limit_help_msg = argparse.SUPPRESS

    if not hidden:
        if show_advanced_options:
            left_limit_help_msg = "'timestamp' left limit"
            right_limit_help_msg = "'timestamp' right limit"

    # redundant with 'to' and 'from' search-api parameters, but useful when debugging a 'selection_file'
    # (no need to edit the 'selection_file')

    parser.add_argument(
        '-L', '--timestamp_left_boundary', help=left_limit_help_msg,
    )

    parser.add_argument(
        '-R', '--timestamp_right_boundary', help=right_limit_help_msg,
    )


def add_common_option(parser, **kw):

    dry_run = kw.get('dry_run', True)
    selection = kw.get('selection', True)
    no_default = kw.get('no_default', True)

    if selection:
        # to only show FILE instead of SELECTION_FILE in the help msg, add metavar='FILE'
        parser.add_argument(
            '-s', '--selection_file', default=None,
        )

    if no_default:
        parser.add_argument(
            '-n', '--no_default', action='store_true', help='prevent loading default value',
        )

    if dry_run:
        parser.add_argument(
            '-z', '--dry_run', action='store_true',
        )


def add_parameter_argument(parser):

    # we use PARAMETER and not FACET as is more generic (e.g. for title, id, etc..)

    parser.add_argument(
        'parameter', nargs='*', default=[], help=sdi18n.m0001,
    )


def add_action_argument(parser, choices=None, default=None):
    parser.add_argument(
        'action', nargs='?', default=default, choices=choices, help=sdi18n.m0017,
    )


def build_epilog_section(title, body):

    if body is not None:
        return """%s\n%s\n""" % (title, body)
    else:
        return None


def build_epilog(kw):
    """This func build sections used in argparse 'epilog' feature."""
    li = []

    description = kw.get('description', None)
    example = kw.get('example', None)
    note = kw.get('note', None)

    if description:
        li.append(build_epilog_section('description', description))

    if example:
        li.append(build_epilog_section('examples', example))

    if note:
        li.append(build_epilog_section('notes', note))

    return '\n'.join(li)


def add_dump_option(parser):

    parser.add_argument(
        '-A', '--all', action='store_true', help='Show all attributes',
    )

    parser.add_argument(
        '-R', '--raw_mode', action='store_true', help='dump original metadata',
    )

    parser.add_argument(
        '-C',
        '--column',
        type=lambda s: s.split(','),
        default=[],
        help="set column(s) to be used with 'dump' action",
    )

    parser.add_argument(
        '-F',
        '--format',
        choices=sdprint.formats,
        default='raw',
        help="set format to be used with 'dump' action",
    )


def add_parser(subparsers, subcommand, **kw):

    epilog = build_epilog(kw)
    parser = subparsers.add_parser(
        subcommand,
        usage=kw.get('usage', None),
        help=kw.get('help'),
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    if kw.get('common_option', True):
        add_common_option(parser, **kw)

    return parser


def run(subparsers, config):

    show_advanced_options = config["show_advanced_options"]

    # autoremove

    add_parser(
        subparsers,
        'autoremove',
        selection=False,
        no_default=False,
        help='Remove old datasets versions',
    )

    # certificate

    subparser = add_parser(
        subparsers,
        'certificate',
        common_option=False,
        help='Manage X509 certificate',
        example=sdcliex.certificate(),
    )

    add_action_argument(
        subparser,
        choices=['renew', 'info', 'print'],
    )

    subparser.add_argument(
        '-d', '--debug', action='store_true', help='Display debug message',
    )
    subparser.add_argument(
        '-o', '--openid', help='ESGF openid',
    )
    subparser.add_argument(
        '-p', '--password', help='ESGF password',
    )
    subparser.add_argument(
        '-x', '--force_renew_ca_certificates', action='store_true', help='Force renew CA certificates',
    )

    # check

    subparser = add_parser(
        subparsers,
        'check',
        no_default=False,
        help='Perform check over ESGF metadata',
        example=sdcliex.check(),
        description=sddescription.check(),
    )

    sdcommonarg.add_playback_record_options(subparser)
    add_action_argument(
        subparser,
        choices=['dataset_version', 'file_variable', 'selection'],
    )

    add_parameter_argument(subparser)

    subparser.add_argument(
        '-F', '--output_format', help='Set output format', default='text', choices=['text', 'pdf'],
    )

    subparser.add_argument(
        '-o', '--outfile', default='/tmp/dataset_version_report.pdf',
    )

    # subparser = create_subparser(
    #     subparsers,
    #     'config',
    #     common_option=False,
    #     help='Print configuration information',
    #     example=sdcliex.config(),
    # )
    # subparser.add_argument(
    #     '-n',
    #     '--name',
    #     default=None,
    #     help='Name of the parameter to be displayed (if not set, all parameters are displayed)',
    # )

    # contact

    add_parser(
        subparsers,
        'contact',
        common_option=False,
        help='Print contact information',
    )

    # count

    subparser = add_parser(
        subparsers,
        'count',
        help='Count file / dataset',
        example=sdcliex.count(),
    )

    subparser.add_argument(
        '-i', '--index_host', help='Retrieve parameters from the specified index',
    )

    add_parameter_argument(subparser)
    add_timestamp_boundaries(subparser, show_advanced_options, hidden=False)
    sdcommonarg.add_type_grp(subparser)

    # daemon

    subparser = add_parser(
        subparsers,
        'daemon',
        common_option=False,
        help='Daemon management',
        note=sdi18n.m0023,
    )

    add_action_argument(
        subparser,
        choices=['start', 'stop', 'status'],
    )

    # dump

    subparser = add_parser(
        subparsers,
        'dump',
        help='Display raw metadata',
        example=sdcliex.dump(),
    )

    add_parameter_argument(subparser)
    sdcommonarg.add_type_grp(subparser)
    add_dump_option(subparser)

    # facet

    subparser = add_parser(
        subparsers,
        'facet',
        no_default=False,
        help='Facet discovery',
        example=sdcliex.facet(),
    )

    subparser.add_argument(
        'facet_name', help='Facet name',
    )

    add_parameter_argument(subparser)

    # get

    subparser = add_parser(
        subparsers,
        'get',
        no_default=False,
        help='Download dataset (sync)',
        example=sdcliex.get(),
    )

    subparser.add_argument(
        '--verify_checksum', '-c', action='store_true', help='Compare remote and local checksum',
    )

    subparser.add_argument(
        '--dest_folder', '-d', default=DEFAULT_DEST_FOLDER_PARSER_ARGUMENT, help='Destination folder',
    )

    subparser.add_argument(
        '--force', '-f', action='store_true', help='Overwrite local file if exists',
    )

    subparser.add_argument(
        '--network_bandwidth_test',
        '-n',
        action='store_true',
        help='Prevent disk I/O to measure network throughput. '
             'When this option is used, local file is set to /dev/null.',
    )

    subparser.add_argument(
        '--openid', '-o', help='ESGF openid',
    )

    subparser.add_argument(
        '--password', '-p', help='ESGF password',
    )

    subparser.add_argument(
        '--quiet', '-q', action='store_true',
    )

    subparser.add_argument(
        '--timeout',
        '-t',
        type=int,
        default=config["direct_http_timeout"],
        help='HTTP timeout',
    )

    subparser.add_argument(
        '--urllib', '-u', action='store_true', help='Use urllib instead of wget as HTTP client',
    )

    #  TAG43534FSFS.
    # As default verbosity is 1, the only way to disable verbosity (i.e. set it to 0) is to use '--quiet' option.
    # Also note that as default is 1 for an argparse 'count' option, '-v' triggers the value 2, not 1, and
    # '-vv' triggers the value 3, not 2: this is normal. To summarize, what we do here is map 'unset' to 1,
    # map [-vvvvvvv...] to the range [2-N], and add '--quiet' option to trigger verbosity level 0.

    subparser.add_argument(
        '--verbosity', '-v', action='count', default=1,
    )

    subparser.add_argument(
        '--hpss', dest='hpss', action='store_true', help="Enable 'hpss' flag",
    )

    subparser.add_argument(
        '--no-hpss', dest='hpss', action='store_false', help="Disable 'hpss' flag (Default)",
    )

    # maybe use preferences.is_download_hpss as default
    subparser.set_defaults(hpss=False)

    add_parameter_argument(subparser)

    # help

    subparser = subparsers.add_parser(
        'help', help='Show help',
    )

    subparser.add_argument(
        'topic', nargs='?',
    )

    # check-env

    add_parser(
        subparsers,
        'check-env',
        help='Checks install environment.',
    )

    add_parser(
        subparsers,
        'init-env',
        help='Initializes install environment.',
    )

    # history

    add_parser(
        subparsers,
        'history',
        common_option=False,
        help='Show history',
    )

    # install

    subparser = add_parser(
        subparsers,
        'install',
        help='Download dataset (async)',
        note=sdi18n.m0022,
        example=sdcliex.install(),
    )

    add_ni_option(subparser)
    add_parameter_argument(subparser)
    add_incremental_mode_argument(subparser, 'install')
    # hidden option mainly used for test and debug
    add_timestamp_boundaries(subparser, show_advanced_options, hidden=True)
    sdcommonarg.add_playback_record_options(subparser, hidden=False)

    # intro

    add_parser(
        subparsers,
        'intro',
        common_option=False,
        help='Print introduction to synda command',
    )

    # list

    # here no_default is a flag to decide if we show no_default option or not
    subparser = add_parser(
        subparsers,
        'list',
        no_default=False,
        help='List installed dataset',
        example=sdcliex.list(),
    )

    # here no_default is the real option
    subparser.set_defaults(no_default=True)

    add_parameter_argument(subparser)
    sdcommonarg.add_type_grp(subparser)

    # metric

    subparser = add_parser(
        subparsers,
        'metric',
        selection=False,
        no_default=False,
        help='Display performance and disk usage metrics',
        example=sdcliex.metric(),
    )

    subparser.add_argument(
        '--groupby', '-g', choices=['data_node', 'project', 'model'], default='data_node', help='Group-by clause',
    )

    subparser.add_argument(
        '--metric', '-m', choices=['rate', 'size'], default='rate', help='Metric name',
    )

    subparser.add_argument(
        '--project', '-p', default='CMIP5', help="Project name (must be used with '--groupby=model' else ignored)",
    )

    # param

    subparser = add_parser(
        subparsers,
        'param',
        common_option=False,
        help='Print ESGF facets',
        example=sdcliex.param(),
    )

    subparser.add_argument(
        'pattern1', nargs='?', default=None, help='Parameter name',
    )

    subparser.add_argument(
        'pattern2', nargs='?', default=None, help='Filter',
    )

    subparser.add_argument(
        '-c', '--columns', type=int, default=1,
    )

    # queue

    subparser = add_parser(
        subparsers,
        'queue',
        common_option=False,
        help='Display download queue status',
        example=sdcliex.queue(),
    )

    subparser.add_argument(
        'project', nargs='?', default=None, help='ESGF project (e.g. CMIP5)',
    )

    # remove

    subparser = add_parser(
        subparsers,
        'remove',
        help='Remove dataset',
        example=sdcliex.remove(),
    )

    add_parameter_argument(subparser)
    add_ni_option(subparser)
    add_verbose_option(subparser)
    subparser.add_argument(
        '-m', '--keep_data', action='store_true', help='Remove only metadata',
    )

    # replica

    subparser = add_parser(
        subparsers,
        'replica',
        selection=False,
        no_default=False,
        help='Move to next replica',
        example=sdcliex.replica(),
    )

    add_action_argument(
        subparser,
        choices=['next'],
    )

    subparser.add_argument(
        'file_id', nargs='?', help='File identifier (ESGF instance_id)',
    )

    # reset

    add_parser(
        subparsers,
        'reset',
        common_option=False,
        help="Remove all 'waiting' and 'error' transfers",
    )

    # retry

    subparser = add_parser(
        subparsers,
        'retry',
        common_option=False,
        help='Retry transfer (switch status from error to waiting)',
    )

    subparser.add_argument(
        '-w',
        '--where',
        default=None,
        help="Restrict the retry to one data_node, e.g. 'esgf3.dkrz.de' or 'dkrz'.  Spaces are not allowed.",
    )

    # ...fairly arbitrary SQL expressions are also allowed, but not documented here because
    # they are prone to user error

    # search

    subparser = add_parser(
        subparsers,
        'search',
        help='Search dataset',
        example=sdcliex.search('synda search'),
    )

    add_parameter_argument(subparser)

    # explode id into individual facets (hidden option mainly used for debug)
    subparser.add_argument(
        '-e', '--explode', action='store_true', help=argparse.SUPPRESS,
    )

    default_limits_mode = config["default_listing_size"]

    default = get_default_limit(default_limits_mode, 'search')

    subparser.add_argument(
        '-l', '--limit', type=int, default=default, help=sdi18n.m0024,
    )

    subparser.add_argument(
        '-r', '--replica', action='store_true', help='show replica',
    )

    add_timestamp_boundaries(subparser, show_advanced_options, hidden=False)
    sdcommonarg.add_type_grp(subparser)

    # selection

    add_parser(
        subparsers,
        'selection',
        common_option=False,
        help='List selection files',
    )

    # show

    subparser = add_parser(
        subparsers,
        'show',
        help='Display detailed information about dataset',
        example=sdcliex.show(),
    )

    add_parameter_argument(subparser)
    add_lsearch_option(subparser)

    # sdcommonarg.add_type_grp(subparser)
    # disabled as type depend on user input (e.g. file_functional_id, dataset_functional_id, etc..)
    add_verbose_option(subparser)

    # stat

    subparser = add_parser(
        subparsers,
        'stat',
        help='Display summary information about dataset',
        example=sdcliex.stat(),
    )

    add_parameter_argument(subparser)
    add_incremental_mode_argument(subparser, 'stat')
    # hidden option mainly used for test and debug
    add_timestamp_boundaries(subparser, show_advanced_options, hidden=True)

    # update

    subparser = add_parser(
        subparsers,
        'update',
        common_option=False,
        help='Update ESGF parameter local cache',
    )

    subparser.add_argument(
        '-i', '--index_host', help='Retrieve parameters from the specified index',
    )

    subparser.add_argument(
        '-p', '--project', help='Retrieve project specific parameters for the specified project',
    )

    # upgrade

    subparser = add_parser(
        subparsers,
        'upgrade',
        selection=False,
        no_default=False,
        help="Run 'install' command on all selection files",
    )

    add_parameter_argument(subparser)
    add_ni_option(subparser)
    add_incremental_mode_argument(subparser, 'upgrade')
    # hidden option mainly used for test and debug
    add_timestamp_boundaries(subparser, show_advanced_options, hidden=True)

    subparser.add_argument(
        '-e', '--exclude_from', metavar='FILE', help='Read exclude selection-file from FILE',
    )

    # variable

    subparser = add_parser(
        subparsers,
        'variable',
        selection=False,
        no_default=False,
        help='Print variable',
        example=sdcliex.variable(),
    )

    add_parameter_argument(subparser)

    subparser.add_argument(
        '-l', '--long_name', action='store_true',
    )

    subparser.add_argument(
        '-s', '--short_name', action='store_true',
    )

    subparser.add_argument(
        '-S', '--standard_name', action='store_true',
    )

    # version

    subparser = add_parser(
        subparsers,
        'version',
        help='List all versions of a dataset',
        example=sdcliex.version(),
    )

    add_parameter_argument(subparser)

    # sdcommonarg.add_type_grp(subparser)
    #  disabled as type depend on user input (e.g. file_functional_id, dataset_functional_id, etc..)

    # watch

    add_parser(
        subparsers,
        'watch',
        common_option=False,
        help='Display running transfer',
    )
