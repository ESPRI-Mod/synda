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

def add_parameter(parser):
    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

def basic(subparsers,action):
    subparser = subparsers.add_parser(action)
    add_parameter(subparser):

def run(subparsers):
    basic(subparsers,'autoremove')
    basic(subparsers,'cache')
    basic(subparsers,'certificate')
    basic(subparsers,'daemon')
    basic(subparsers,'dump')
    basic(subparsers,'help')
    basic(subparsers,'history')
    basic(subparsers,'install')
    basic(subparsers,'list')
    basic(subparsers,'param')
    basic(subparsers,'pexec')
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
