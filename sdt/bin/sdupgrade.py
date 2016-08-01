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

import sdsearch
import sdinstall
import sdexception
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

    for selection in selections:
        try:
            print_stderr("Process %s.."%selection.filename)
            install(args,selection)
        except sdexception.UnknownParameterException,e:
            print_stderr("Error occurs while processing %s (str(e))"%selection.filename)

def install(args,selection):

    # TODO: maybe force type=file here, in case the selection file have 'type=Dataset'

    if not args.dry_run:
        metadata=sdsearch.run(selection=selection)
        args.yes=True
        (status,newly_installed_files_count)=sdinstall.run(args,metadata)
