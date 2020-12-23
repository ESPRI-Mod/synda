#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'upgrade' routines."""

import os
import sdsearch
import sdinstall
import sdexception
import sdlog
from sdtools import print_stderr

def run(selections,args):

    # BEWARE: tricky statement
    #
    # 'upgrade' is a multi-selections 'subcommand' which do the same as the
    # mono-selection 'install' subcommand, but for many selections.  What we do
    # here is replace 'upgrade' subcommand with 'install' subcommand, so that we can,
    # now that we are in 'upgrade' func/context, 
    # come back to the existing mono-selection func,
    # for each selection, with 'install' subcommand.
    #
    args.subcommand='install'

    # force non-interactive mode
    args.yes=True

    exclude_selection_files=get_exclude(args)

    for selection in selections:

        if selection.filename in exclude_selection_files:
            continue

        try:
            sdlog.info("SDUPGRAD-003","Process %s.."%selection.filename,stdout=True)
            install(args,selection)
        except sdexception.IncorrectParameterException,e:
            sdlog.error("SDUPGRAD-004","Error occurs while processing %s (%s)"%(selection.filename,str(e)),stderr=True)
        except sdexception.SDException,e:
            sdlog.error("SDUPGRAD-008","Error occurs while processing %s (%s)"%(selection.filename,str(e)),stderr=True)

    sdlog.info("SDUPGRAD-020","Upgrade completed successfully")

def install(args,selection):

    # TODO: maybe force type=file here, in case the selection file have 'type=Dataset'

    if not args.dry_run:
        sdlog.info("SDUPGRAD-001","Retrieve metadata from ESGF..")
        metadata=sdsearch.run(selection=selection)
        sdlog.info("SDUPGRAD-002","Install files..")
        (status,newly_installed_files_count)=sdinstall.run(args,metadata)

def get_exclude(args):
    li=[]

    if args.exclude_from is None:
        return []

    if not os.path.isfile(args.exclude_from):
        raise sdexception.SDException('SDUPGRAD-108','exclude-from file not found (%s)'%args.exclude_from)

    with open(args.exclude_from) as f:
        li = [line.rstrip('\r\n') for line in f]

    return li

# init.

