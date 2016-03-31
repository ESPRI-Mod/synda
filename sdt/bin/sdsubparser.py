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

import argparse
import sdi18n
import sdcliex
import sdconst
import sdprint

def add_lsearch_option(parser):
    parser.add_argument('-l','--localsearch',action='store_true',help='search in local data repository (already installed dataset)')

def add_verbose_option(parser):
    parser.add_argument('--verbose',action='store_true',help='verbose mode')

def add_type_grp(parser):
    type_grp=parser.add_mutually_exclusive_group(required=False)
    type_grp.add_argument('-a','--aggregation',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)
    type_grp.add_argument('-d','--dataset',dest='type_',action='store_const',const=sdconst.SA_TYPE_DATASET)
    type_grp.add_argument('-f','--file',dest='type_',action='store_const',const=sdconst.SA_TYPE_FILE)
    type_grp.add_argument('-v','--variable',dest='type_',action='store_const',const=sdconst.SA_TYPE_AGGREGATION)


def add_ni_option(parser):
    parser.add_argument('-y','--yes',action='store_true',help='assume "yes" as answer to all prompts and run non-interactively')

def add_common_option(parser,**kw):

    dry_run=kw.get('dry_run',True)
    selection=kw.get('selection',True)
    no_default=kw.get('no_default',True)

    if selection:
        parser.add_argument('-s','--selection_file',default=None) # to only show FILE instead of SELECTION_FILE in the help msg, add metavar='FILE'

    if no_default:
        parser.add_argument('-n','--no_default',action='store_true',help='prevent loading default value')

    if dry_run:
        parser.add_argument('-z','--dry_run',action='store_true')

def add_parameter_argument(parser):
    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001) # we use PARAMETER and not FACET as is more generic (e.g. for title, id, etc..)

def add_action_argument(parser,choices=None):
    parser.add_argument('action',nargs='?',default=None,choices=choices,help=sdi18n.m0017)

def add_dump_option(parser):
    parser.add_argument('-A','--all',action='store_true',help='Show all attributes')
    parser.add_argument('-R','--raw_mode',action='store_true',help='dump original metadata')
    parser.add_argument('-C','--column',type=lambda s: s.split(','),default=[],help="set column(s) to be used with 'dump' action")
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw',help="set format to be used with 'dump' action")

def create_subparser(subparsers,subcommand,**kw):

    # prepare example
    #
    # note
    #     currently, 'epilog' is only used to display 'example' section, but other section may be added there too
    #
    example=kw.get('example',None)
    if example is not None:
        epilog="""examples\n%s\n"""%example
    else:
        epilog=None


    subparser = subparsers.add_parser(subcommand,help=kw.get('help'),epilog=epilog,formatter_class=argparse.RawTextHelpFormatter)

    if kw.get('common_option',True):
        add_common_option(subparser,**kw)

    return subparser

def run(subparsers):
    subparser=create_subparser(subparsers,'autoremove',selection=False,no_default=False,help='Remove old datasets versions')

    subparser=create_subparser(subparsers,'cache',common_option=False,help='Manage cache')
    add_action_argument(subparser,choices=['init'])

    subparser=create_subparser(subparsers,'certificate',common_option=False,help='Manage X509 certificate')
    add_action_argument(subparser,choices=['renew','print'])
    subparser.add_argument('-x','--force_renew_ca_certificates',action='store_true',help='Force renew CA certificates')

    subparser=create_subparser(subparsers,'contact',common_option=False,help='Print contact information')

    subparser=create_subparser(subparsers,'daemon',common_option=False,help='Daemon management')
    add_action_argument(subparser,choices=['start','stop','status'])

    subparser=create_subparser(subparsers,'dump',help='Display raw metadata')
    add_parameter_argument(subparser)
    add_type_grp(subparser)
    add_dump_option(subparser)

    subparser=create_subparser(subparsers,'facet',selection=False,no_default=False,help='Facet discovery')
    subparser.add_argument('facet_name',help='Facet name')
    add_parameter_argument(subparser)

    subparser=subparsers.add_parser('help',help='Show help')
    subparser.add_argument('topic',nargs='?')

    subparser=create_subparser(subparsers,'history',common_option=False,help='Show history')

    subparser=create_subparser(subparsers,'install',help='Install dataset')
    add_ni_option(subparser)
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'intro',common_option=False,help='Print introduction to synda command')

    subparser=create_subparser(subparsers,'list',help='List installed dataset')
    add_parameter_argument(subparser)
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'metric',common_option=False,help='Display performance and disk usage metrics')
    subparser.add_argument('--groupby','-g',choices=['data_node','project','model'],default='data_node',help='Group-by clause')
    subparser.add_argument('--metric','-m',choices=['rate','size'],default='rate',help='Metric name')
    subparser.add_argument('--project','-p',default='CMIP5',help="Project name (must be used with '--groupby=model' else ignored)")

    subparser=create_subparser(subparsers,'param',common_option=False,help='Display ESGF parameters')
    subparser.add_argument('pattern1',nargs='?',default=None,help='Parameter name')
    subparser.add_argument('pattern2',nargs='?',default=None,help='Filter')
    subparser.add_argument('-c','--columns',type=int,default=1)

    subparser=create_subparser(subparsers,'pexec',help='Execute post-processing task')
    subparser.add_argument('order_name',help='Order name')
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'queue',common_option=False,help='Display download queue status',example=sdcliex.queue())
    subparser.add_argument('project',nargs='?',default=None,help='ESGF project (e.g. CMIP5)')

    subparser=create_subparser(subparsers,'remove',help='Remove dataset',example=sdcliex.remove())
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'replica',selection=False,no_default=False,help='Move to next replica',example=sdcliex.replica())
    add_action_argument(subparser,choices=['next'])
    subparser.add_argument('file_id',nargs='?',help='File identifier (ESGF instance_id)')

    subparser=create_subparser(subparsers,'reset',common_option=False,help="Remove all 'waiting' and 'error' transfers")
    subparser=create_subparser(subparsers,'retry',common_option=False,help='Retry transfer (switch error status to waiting)')

    subparser=create_subparser(subparsers,'search',help='Search dataset',example=sdcliex.search('synda search'))
    add_parameter_argument(subparser)
    subparser.add_argument('-r','--replica',action='store_true',help='show replica')
    add_type_grp(subparser)

    subparser=create_subparser(subparsers,'selection',common_option=False,help='List selection files')

    subparser=create_subparser(subparsers,'show',help='Display detailed information about dataset',example=sdcliex.show())
    add_parameter_argument(subparser)
    add_lsearch_option(subparser)
    #add_type_grp(subparser) # disabled as type depend on user input (e.g. file_functional_id, dataset_functional_id, etc..)
    add_verbose_option(subparser)

    subparser=create_subparser(subparsers,'stat',help='Display summary information about dataset',example=sdcliex.stat())
    add_parameter_argument(subparser)

    subparser=create_subparser(subparsers,'test',common_option=False,help='Test file download',example=sdcliex.test())
    subparser.add_argument('file_url',help='file url')

    subparser=create_subparser(subparsers,'update',common_option=False,help='Update ESGF parameter local cache')
    subparser.add_argument('-i','--index_host',help='Retrieve parameters from the specified index')
    subparser.add_argument('-p','--project',help='Retrieve project specific parameters for the specified project')

    subparser=create_subparser(subparsers,'upgrade',selection=False,no_default=False,help='Perform an upgrade (retrieve new version for all selection files)')
    add_parameter_argument(subparser)
    add_ni_option(subparser)

    subparser=create_subparser(subparsers,'version',help='List all versions of a dataset',example=sdcliex.version())
    add_parameter_argument(subparser)
    #add_type_grp(subparser) # disabled as type depend on user input (e.g. file_functional_id, dataset_functional_id, etc..)

    subparser=create_subparser(subparsers,'watch',common_option=False,help='Display running transfer')
