#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains actions specific parsers used by 'synda' script."""

import sdi18n
import sdconst

def add_lsearch_option(parser):
    parser.add_argument('-l','--localsearch',action='store_true',help='search in local data repository (already installed dataset)')

def add_verbose_option(parser):
    parser.add_argument('--verbose',action='store_true',help='verbose mode')

def add_type_grp(parser):
    type_grp=parser.add_argument_group(None)
    type_grp.add_argument('-a','--aggregation',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)
    type_grp.add_argument('-d','--dataset',dest='type_',action='store_const',const=sdconst.SA_TYPE_DATASET)
    type_grp.add_argument('-f','--file',dest='type_',action='store_const',const=sdconst.SA_TYPE_FILE)
    type_grp.add_argument('-v','--variable',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)


def add_ni_option(parser):
    parser.add_argument('-N','--non_interactive',action='store_true',help='assume "yes" as answer to all prompts and run non-interactively (useful in cron jobs)')

def add_common_option(parser,**kw):

    dry_run=kw.get('dry_run',True)
    selection=kw.get('selection',True)
    no_default=kw.get('no_default',True)

    if selection:
        parser.add_argument('-s','--selection',default=None)

    if no_default:
        parser.add_argument('-n','--no_default',action='store_true',help='prevent loading default value')

    if dry_run:
        parser.add_argument('-y','--dry_run',action='store_true')

def add_parameter_argument(parser):
    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001) # we use PARAMETER and not FACET as is more generic (e.g. for title, id, etc..)

def add_action_argument(parser):
    parser.add_argument('action',nargs='?',default=None,help=sdi18n.m0017)

def add_dump_option(parser):
    parser.add_argument('-R','--raw_mode',action='store_true',help='dump original metadata')
    parser.add_argument('-C','--column',type=lambda s: s.split(','),default=[],help="set column(s) to be used with 'dump' action")
    parser.add_argument('-F','--format',choices=['raw','line','indent'],default='raw',help="set format to be used with 'dump' action")

def create_subparser(subparsers,subcommand,**kw):
    subparser = subparsers.add_parser(subcommand,help=kw.get('help'))

    if kw.get('common_option',True):
        add_common_option(subparser,**kw)

    return subparser

def run(subparsers):
    subparser=create_subparser(subparsers,'autoremove',help='Remove old datasets versions')

    subparser=create_subparser(subparsers,'cache',help='Manage cache')
    add_action_argument(subparser)

    subparser=create_subparser(subparsers,'certificate',help='Manage X509 certificate')
    add_action_argument(subparser,common_option=False)

    subparser=create_subparser(subparsers,'daemon',help='Start/stop the daemon (download background process)')
    add_action_argument(subparser)

    subparser=create_subparser(subparsers,'dump',help='Display raw metadata')
    add_parameter_argument(subparser)
    add_type_grp(subparser)
    add_dump_option(subparser)

    subparser=create_subparser(subparsers,'facet',help='Facet discovery')
    subparser.add_argument('facet_name')
    add_parameter_argument(subparser)

    subparser=subparsers.add_parser('help',help='Show help')
    subparser.add_argument('topic',nargs='?')

    subparser=create_subparser(subparsers,'history',help='Show history')

    subparser=create_subparser(subparsers,'install',help='Install dataset')
    add_ni_option(subparser)
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'list',help='List installed dataset')
    add_parameter_argument(subparser)
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'param',help='Display ESGF parameters')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'pexec',help='Execute post-processing task')
    subparser.add_argument('order')
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'queue',help='Display download queue status')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'remove',help='Remove dataset')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'replica',help='Change replica')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'reset',help="Remove all 'waiting' and 'error' transfers")
    subparser=create_subparser(subparsers,'retry',help='Retry transfer')

    subparser=create_subparser(subparsers,'search',help='Search dataset')
    add_parameter_argument(subparser)
    subparser.add_argument('-r','--replica',action='store_true',help='show replica')
    add_lsearch_option(subparser)
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'selection',help='Manage selection')

    subparser=create_subparser(subparsers,'show',help='Display detailed information about dataset')
    add_parameter_argument(subparser)
    add_lsearch_option(subparser)
    add_type_grp(subparser)
    add_verbose_option(subparser)

    subparser=create_subparser(subparsers,'stat',help='Display summary information about dataset')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'test',help='Test file download')
    subparser.add_argument('file_url',help='file url')

    subparser=create_subparser(subparsers,'update',help='Update ESGF parameter local cache')

    subparser=create_subparser(subparsers,'upgrade',help='Perform an upgrade (retrieve new version for already installed datasets)')
    add_parameter_argument(subparser)
    add_ni_option(subparser)

    subparser=create_subparser(subparsers,'version',help='List all versions of a dataset')
    add_parameter_argument(subparser)
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'watch',help='Display running transfer')
