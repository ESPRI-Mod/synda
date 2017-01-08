#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""This module contains actions specific parsers used by 'synda' script."""

import argparse
import spcliex

def build_epilog_section(title,body):

    if body is not None:
        return """%s\n%s\n"""%(title,body)
    else:
        return None

def build_epilog(kw):
    """This func build sections used in argparse 'epilog' feature."""
    li=[]

    example=kw.get('example',None)
    note=kw.get('note',None)

    if example:
        li.append(build_epilog_section('examples',example))

    if note:
        li.append(build_epilog_section('notes',note))

    return '\n'.join(li)

def create_subparser(subparsers,subcommand,**kw):

    epilog=build_epilog(kw)

    subparser = subparsers.add_parser(subcommand,usage=kw.get('usage',None),help=kw.get('help'),epilog=epilog,formatter_class=argparse.RawTextHelpFormatter)

    if kw.get('common_option',True):
        add_common_option(subparser,**kw)

    return subparser

def run(subparsers):
    subparser=subparsers.add_parser('help',help='Show help')
    subparser.add_argument('topic',nargs='?')

    subparser=create_subparser(subparsers,'queue',common_option=False,help='Display download queue status',example=spcliex.queue())
    subparser.add_argument('project',nargs='?',default=None,help='ESGF project (e.g. CMIP5)')

    subparser=create_subparser(subparsers,'daemon',common_option=False,help='Daemon management',example=spcliex.daemon())
    subparser.add_argument('action',nargs='?',default='status',choices=['status','start','stop'])
