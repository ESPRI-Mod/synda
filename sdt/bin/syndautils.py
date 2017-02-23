#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains startup helper.

Notes
    - In this file, module import directives are moved near the calls, so to improve startup time.
"""

import sys
import os
import sdconst

def check_daemon():
    import sdconfig
    if sdconfig.prevent_daemon_and_modification:
        import sddaemon
        if sddaemon.is_running():
            print 'The daemon must be stopped before installing/removing dataset'
            sys.exit(3)

def get_stream(subcommand=None,parameter=None,selection_file=None,no_default=True,raise_exception_if_empty=False):
    """
    TODO: merge me with sdstreamutils.get_stream
    """
    import sdbuffer, sdparse, sdstream, sdconfig, sddeferredbefore, sdexception

    if parameter is None:
        parameter=[]

    buffer=sdbuffer.get_selection_file_buffer(parameter=parameter,path=selection_file)


    if len(buffer.lines)==0:
        # we come here when user selected nothing (neither from stdin neither from selection file neither from arg)

        if raise_exception_if_empty:
            raise sdexception.EmptySelectionException()


    selection=sdparse.build(buffer,load_default=(not no_default))
    stream=selection.to_stream()

    # Set default value for nearest here
    #
    # TODO: make it work with all actions (e.g. search) as it only working for 'install' action for now
    #
    if sdconfig.config.getboolean('behaviour','nearest'):
        #sddeferredbefore.add_default_parameter(stream,'nearest',True) # TODO: why this one is not working ?
        sdstream.set_scalar(stream,'nearest',True)

    # progress
    if sdconfig.config.getboolean('interface','progress'):
        sdstream.set_scalar(stream,'progress',True)

    sdstream.set_scalar(stream,'action',subcommand) # from the synda engine perspective, 'action' is more meaningful than 'subcommand'

    return stream # aka facets_groups

def file_full_search(args,stream=None):
    """This func systematically triggers full search (i.e. limit keyword cannot be used here).

    This func is currently being used in the following modules:
        - sdinstall
        - sdremove
        - sdstat
    """
    import sdsearch,sdlog,sdhistory,sdstream,sdtime,sdselectionfileutils

    if stream is None:
        stream=get_stream(subcommand=args.subcommand,parameter=args.parameter,selection_file=args.selection_file,no_default=args.no_default,raise_exception_if_empty=True)

    force_type(stream,sdconst.SA_TYPE_FILE) # type is always SA_TYPE_FILE when we are here



    # incremental mode management

    if args.subcommand in ('install','stat'): # prevent incremental mode for 'remove' subcommand

        if args.timestamp_left_boundary and args.incremental:
            raise sdexception.SDException('SYNUTILS-003',"Incorrect argument: 'timestamp_left_boundary' and 'incremental' are mutually exclusive options")

        # those filters are mainly used to test 'incremental mode' feature
        if args.timestamp_left_boundary is not None:
            sdstream.set_scalar(stream,'from',args.timestamp_left_boundary)
        if args.timestamp_right_boundary is not None:
            sdstream.set_scalar(stream,'to',args.timestamp_right_boundary)


        if args.incremental:

            sdlog.info('SYNUTILS-002','Starting file discovery (incremental mode enabled)')

            selection_file=sdselectionfileutils.find_selection_file(args.selection_file)

            selection_filename=os.path.basename(selection_file)

            if sdhistory.previous_run_exists(selection_filename,'add'):
                sdlog.info('SYNUTILS-004','Previous run exists')

                if not sdhistory.file_changed_since_last_run(selection_file,sdconst.ACTION_ADD):
                    sdlog.info('SYNUTILS-006',"Selection file hasn't changed since last run")

                    previous_run=sdhistory.get_previous_run(selection_filename,'add')
                    dt=previous_run['crea_date']


                    # to prevent UTC vs localtime time issue
                    # (history.crea_date is in localtime while search-api timestamp is in UTC time)
                    # we systematically substract 72 hours to the left boundary
                    #
                    dt=sdtime.substract_hour(dt,72)


                    # convert datetime format
                    search_api_datetime=sdtime.sqlite_datetime_format_to_search_api_datetime_format(dt)


                    # add incremental mode filters
                    #
                    # sample
                    #     from='2015-10-19T22:00:00Z'
                    #
                    # note
                    #     'from' and 'to' filters refer to 'timestamp' attribute
                    #
                    # more info
                    #     https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API
                    #
                    sdstream.set_scalar(stream,'from',search_api_datetime)

                else:
                    sdlog.info('SYNUTILS-007',"Selection file has changed since last run")

            else:
                sdlog.info('SYNUTILS-008','No previous run found')



    metadata=sdsearch.run(stream=stream,dry_run=args.dry_run)

    return metadata

def force_type(stream,type_):
    import sddeferredbefore

    # we 'force' (i.e. we do not just set as 'default') the parameter here, so
    # to prevent user to set it
    sddeferredbefore.add_forced_parameter(stream,'type',type_)

def strip_dataset_version(dataset_functional_id):
    import re
    return re.sub('\.[^.]+$','',dataset_functional_id)
