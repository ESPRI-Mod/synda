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
import sdconst
import sdtools
from sdtools import print_stderr

def check_daemon():
    import sdconfig
    if sdconfig.prevent_daemon_and_modification:
        import sddaemon
        if sddaemon.is_running():
            print 'The daemon must be stopped before installing/removing dataset'
            sys.exit(3)

def get_stream(args):
        import sdbuffer, sdparse, sdstream, sdconfig, sddeferredbefore

        # hack
        if args.action=='list':
            args.no_default=True

        buffer=sdbuffer.get_selection_file_buffer(parameter=args.parameter,path=args.selection)
        selection=sdparse.build(buffer,load_default=(not args.no_default))
        stream=selection.to_stream()

        # Set default value for nearest here
        #
        # TODO: make it work with all actions (e.g. search) as it only working for 'install' action for now
        #
        #sddeferredbefore.add_default_parameter(stream,'nearest',True) # TODO: why this one is not working ?
        if sdconfig.config.getboolean('behaviour','nearest'):
            sdstream.set_scalar(stream,'nearest',True)

        # progress
        if sdconfig.config.getboolean('interface','progress'):
            sdstream.set_scalar(stream,'progress',True)

        return stream

def file_full_search(args):
    # this func systematically trigger full search (i.e. limit keyword cannot be used here)

    stream=get_stream(args)
    check_stream(stream)
    force_type(stream,sdconst.SA_TYPE_FILE) # type is always SA_TYPE_FILE when we are here
    import sdsearch
    files=sdsearch.run(stream=stream,dry_run=args.dry_run)

    return files

def check_stream(stream):
    import sdstream

    if sdstream.is_empty(stream):
        print 'No packages will be installed, upgraded, or removed.'
        sys.exit(0)

def force_type(stream,type_):
    import sddeferredbefore

    # we 'force' (i.e. we do not just set as 'default') the parameter here, so
    # to prevent user to set it
    sddeferredbefore.add_forced_parameter(stream,'type',type_)

def get_facet_early(orig_stream,name):
    """Get facets from a dqueries object at an early time (before any transformation of that object occured).

    Note
        Early means we want item from the dqueries just after it's creation
        (i.e. when no transformation (e.g. sdinference) occured yet).
        
    TODO
        Maybe find a proper way to do that
    """
    import sdstream, sdextractitem, sdinference, copy, sddeferredbefore, sddeferredafter

    assert name!='type' # type cannot be inferred using this func (use infer_type() func instead)

    stream=copy.deepcopy(orig_stream) # this is not to modify the original stream at this point

    stream=sddeferredbefore.run(stream)
    stream=sdinference.run(stream) # this is to resolve pending parameter
    stream=sddeferredafter.run(stream)
    stream=sdextractitem.run(stream,name) # we extract item from identifier if present

    li=sdstream.get_facet_values(stream,name)

    return li

def is_one_variable_per_dataset_project(args):
    """This func is a HACK.

    HACK description
        For some project, one dataset = one variable.
        For such cases, there is no point to display a variable list,
        so we change the route to display the dataset list.
    """

    # retrieve project from input
    project=get_facet_early(args.stream,'project')

    # check
    if len(project)==0:
        print_stderr("The project name must be specified in the search (mandatory when using 'variable/agreggation' type)")
        sys.exit(1)
    elif len(project)>1:
        print_stderr("Only one project name must be specified in the search (mandatory when using 'variable/agreggation' type)")
        sys.exit(1)

    if sdtools.intersect(project,sdconst.PROJECT_WITH_ONE_VARIABLE_PER_DATASET):
        return True
    else:
        return False

def strip_dataset_version(dataset_functional_id):
    import re
    return re.sub('\.[^.]+$','',dataset_functional_id)
