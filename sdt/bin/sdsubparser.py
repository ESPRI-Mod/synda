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

def add_type_grp(parser):
    type_grp=parser.add_argument_group(None)
    type_grp.add_argument('-a','--aggregation',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)
    type_grp.add_argument('-d','--dataset',dest='type_',action='store_const',const=sdconst.SA_TYPE_DATASET)
    type_grp.add_argument('-f','--file',dest='type_',action='store_const',const=sdconst.SA_TYPE_FILE)
    type_grp.add_argument('-v','--variable',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)

def add_parameter(parser):
    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

def basic(subparsers,action):
    subparser = subparsers.add_parser(action)
    add_parameter(subparser)
    add_type_grp(subparser)

def run(subparsers):
    basic(subparsers,'autoremove')
    basic(subparsers,'cache')
    basic(subparsers,'certificate')
    basic(subparsers,'daemon')
    basic(subparsers,'dump')

    subparser = subparsers.add_parser('help')
    subparser.add_argument('topic',nargs='?')

    basic(subparsers,'history')
    basic(subparsers,'install')
    basic(subparsers,'list')
    basic(subparsers,'param')

    subparser = subparsers.add_parser('pexec')
    subparser.add_argument('order')
    add_type_grp(subparser)

    basic(subparsers,'queue')
    basic(subparsers,'remove')
    basic(subparsers,'replica')
    basic(subparsers,'reset')
    basic(subparsers,'retry')
    basic(subparsers,'search')
    basic(subparsers,'selection')
    basic(subparsers,'show')
    basic(subparsers,'stat')
    basic(subparsers,'test')
    basic(subparsers,'update')
    basic(subparsers,'upgrade')
    basic(subparsers,'version')
    basic(subparsers,'watch')
