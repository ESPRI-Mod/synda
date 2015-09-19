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

def add_type_grp(parser):
    type_grp=parser.add_argument_group(None)
    type_grp.add_argument('-a','--aggregation',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)
    type_grp.add_argument('-d','--dataset',dest='type_',action='store_const',const=sdconst.SA_TYPE_DATASET)
    type_grp.add_argument('-f','--file',dest='type_',action='store_const',const=sdconst.SA_TYPE_FILE)
    type_grp.add_argument('-v','--variable',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)


def add_ni_option(parser):
    parser.add_argument('-N','--non_interactive',action='store_true',help='assume "yes" as answer to all prompts and run non-interactively (useful in cron jobs)')

def add_common_option(parser):
    parser.add_argument('-s','--selection',default=None)
    parser.add_argument('-n','--no_default',action='store_true',help='prevent loading default value')
    parser.add_argument('-y','--dry_run',action='store_true')

def add_parameter_argument(parser):
    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001) # we use PARAMETER and not FACET as is more generic (e.g. for title, id, etc..)

def add_dump_option(parser):
    parser.add_argument('-R','--raw_mode',action='store_true',help='dump original metadata')
    parser.add_argument('-C','--column',type=lambda s: s.split(','),default=[],help="set column(s) to be used with 'dump' action")
    parser.add_argument('-F','--format',choices=['raw','line','indent'],default='raw',help="set format to be used with 'dump' action")

def create_subparser(subparsers,action):
    subparser = subparsers.add_parser(action)
    add_common_option(subparser)
    return subparser

def run(subparsers):
    subparser=create_subparser(subparsers,'autoremove')

    subparser=create_subparser(subparsers,'cache')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'certificate')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'daemon')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'dump')
    add_parameter_argument(subparser)
    add_type_grp(subparser)
    add_dump_option(subparser)

    subparser=subparsers.add_parser('help')
    subparser.add_argument('topic',nargs='?')

    subparser=create_subparser(subparsers,'history')

    subparser=create_subparser(subparsers,'install')
    add_ni_option(subparser)
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'list')
    add_parameter_argument(subparser)
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'param')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'pexec')
    subparser.add_argument('order')
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'queue')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'remove')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'replica')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'reset')
    subparser=create_subparser(subparsers,'retry')

    subparser=create_subparser(subparsers,'search')
    add_parameter_argument(subparser)
    subparser.add_argument('-r','--replica',action='store_true',help='show replica')
    add_lsearch_option(subparser)
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'selection')

    subparser=create_subparser(subparsers,'show')
    add_parameter_argument(subparser)
    add_lsearch_option(subparser)
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'stat')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'test')
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'update')

    subparser=create_subparser(subparsers,'upgrade')
    add_parameter_argument(subparser)
    add_ni_option(subparser)

    subparser=create_subparser(subparsers,'version')
    add_parameter_argument(subparser)
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'watch')
