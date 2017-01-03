#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Parse selection buffer (and default files)."""

import sys
import os
import argparse
import re
import json
import sdapp
from sdtypes import Selection
from sdexception import SDException
import sdtools
import sdconfig
import sdbuffer
import sdconst
import sdprint
import sdi18n
import sdearlystreamutils

def build(buffer,load_default=None):
    """This func builds selection and set default values.

    Args:
        buffer (Buffer): selection buffer
        load_default (bool): specify if we need to load default values

    Note:
        Selection values overwrite project specific default values which in turn over overwrite multi-project default values.
    """
    assert buffer is not None
    assert isinstance(buffer.lines,list)

    # compute 'load_default' flag
    # (maybe this block can be removed, as it seems we always set load_default to non-None value (to be confirmed))
    if load_default is None:
        if buffer.filename==sdconst.SELECTION_FROM_CMDLINE:
            load_default=False # don't load default files if selection is from command args
        else:
            load_default=True # load default files if selection is from stdin or file

    # create buffer selection
    selection=Selection()

    # store outer attributes ('outer' means attributes not stored in selection file)
    selection.filename=buffer.filename
    selection.path=buffer.path

    # store inner attributes ('inner' means attributes stored in selection file)
    parse_buffer(buffer.lines,selection)

    # merge some outer attributes with inner attributes (else they are not returned by merge_facets() method)
    process_parameter("selection_filename=%s"%selection.filename,selection)
    process_parameter("selection_file=%s"%selection.path,selection)

    # load default (file containing default parameters for all projects)
    default_selection=load_default_file(sdconfig.default_selection_file,load_default)


    # NOTE
    #
    # For project level default file to be loaded, the following must be true
    #
    #   "project must be specified in cli parameter or in the selection file or 
    #   in the global default file" or inside an identifier (e.g. dataset_functional_id)


    # retrieve projects
    projects=get_projects(selection)

    # retrieve default projects
    default_projects=get_default_projects(default_selection)

    # 
    if len(projects)==0:
        # project not present in CLI nor in 'selection file'

        # let's try if project is set in default file
        if len(default_projects)==0:
            project=None # no project set
        elif len(default_projects)==1:
            project=default_projects[0]
        elif len(default_projects)>1:
            print_too_many_projects_set_warning(default_projects)
            project=None # too many project: do not load project level default value

    elif len(projects)>0:

        # When project(s) are present in CLI or 'selection file',
        # project(s) from default file are ignored.
        # (see #34 for more info)
        if len(default_projects)>0:
            del default_selection.facets['project']
            

        if len(projects)==1:
            project=projects[0]
        elif len(projects)>1:
            print_too_many_projects_set_warning(projects)
            project=None # too many project: do not load project level default value


    # load project default (file containing default parameters for the project)
    project_default_selection=load_default_file(sdconfig.get_project_default_selection_file(project),load_default)

    project_default_selection.childs.append(selection)         # add selection as child of project_default_selection
    selection.parent=project_default_selection                 # set project_default_selection as parent of selection

    default_selection.childs.append(project_default_selection) # add project_default_selection as child of default_selection
    project_default_selection.parent=default_selection         # set default_selection as parent of project_default_selection

    return selection

def print_too_many_projects_set_warning(projects):
    sdtools.print_stderr('WARNING: several projects set: project default values file not loaded %s'%str(projects))

def get_default_projects(default_selection):
    projects=[]
    if 'project' in default_selection.facets:
        projects+=default_selection.facets['project']
    return projects

def get_projects(selection):
    """This method returns project (standalone pending, standalone non-pending
    or as part of an identifier) from CLI parameter or selection file."""
    project=[]

    # project with keyname

    if 'project' in selection.facets:
        project+=selection.facets['project']


    # project without keyname

    # WARNING
    #
    # The code below uses sdinference and query the database to retrieve ESGF parameters.
    # Doing those things here may raise circular dependencies
    # as well as making the whole thing very complex.
    #
    # We do this to make this syntax work (i.e. project value without key)
    #   synda search GeoMIP
    #
    # Note that this syntax always works (i.e. load the project level default file), even without this code.
    #   synda search project=GeoMIP
    #
    #
    pending_projects=sdearlystreamutils.get_facet_values_early([selection.facets],'project',extract_item=True) # project without keyname or project as part of an identifier.

    li=pending_projects+project

    li=list(set(li)) # remove duplicate

    return li

def load_default_file(path,load_default):
    selection=Selection()
    if load_default:
        if path is not None:
            if os.path.isfile(path):
                parse_file(path,selection)
    return selection

def parse_buffer(buffer,selection):
    """
    Args:
        buffer (list of string)
    """
    for line in buffer:

        assert "\n" not in line # newline should have already been stripped at this step

        # pass comment line
        if(re.search('^#.*$', line)!=None):
            continue

        # pass blank line
        if(re.search('^ *$', line)!=None):
            continue

        process_parameter(line,selection)

def parse_file(path,selection):
    # used only for default file

    # set outer attributes
    selection.path=path # fullpath
    selection.filename=os.path.basename(path)

    # set inner attributes
    with open(path, 'r') as fh:

        lines=[line.rstrip(os.linesep) for line in fh.readlines()] # remove newline

        parse_buffer(lines,selection)

def process_parameter(parameter,selection):

    if is_sfg_parameter(parameter):
        if is_rfv_parameter(parameter):
            process_rfv_parameter(parameter,selection)
        elif is_ffv_parameter(parameter):
            process_ffv_parameter(parameter,selection)
        else:
            raise SDException("SDPARSER-012","incorrect parameter format (%s)"%parameter)
    else:
        if '=' not in parameter:

            # as '=' is missing, we consider it's the parameter name that is
            # not present.
            # we keep the parameter value and we will try to guess the
            # corresponding parameter name using 'sdinference' module in a
            # downstream step.

            # until then, we store all those pending parameters in a dedicated key
            param_name=sdconst.PENDING_PARAMETER
            param_value=[parameter]
        else:
            # key-value parameter

            (param_name,param_value)=parse_parameter(parameter)

        add_parameter(param_name,param_value,selection)

def parse_parameter(parameter):
    m=re.search('^([^=]+)="?([^"=]+)"?$',parameter)
    if(m!=None):
        param_name=m.group(1)
        param_value=sdtools.split_values(m.group(2))

        return (param_name,param_value)
    else:
        raise SDException("SDPARSER-001","incorrect format (%s)"%(parameter,))

def add_parameter(param_name,param_value,selection):
    if param_name in selection.facets:
        # if we are here, it means same facet is set several times

        # OLD WAY: replace previous value 
        #selection.facets[param_name]=param_value
        # NEW WAY: append new values to previous values
        selection.facets[param_name].extend(param_value)

    else:
        selection.facets[param_name]=param_value

def process_rfv_parameter(parameter,selection): # rfv means 'Realm Frequency n Variable'
    # note
    #  - "*" wildcard character is supported for realm and frequency and variable
    #
    # sample
    #  variable[atmos][*]=cl ta hus hur wap ua va zg clcalipso

    m=re.search('variables?\[(.+)\]\[(.+)\]="?([^"=]+)"?$', parameter)
    if(m!=None):
        realm=m.group(1)
        time_frequency=m.group(2)
        variables=sdtools.split_values(m.group(3))

        facets={}
        facets["realm"]=[realm]
        facets["time_frequency"]=[time_frequency]
        facets["variable"]=variables

        selection.childs.append(Selection(facets=facets,filename="rfvsp")) # add sub-selection ("rfvsp" means "Realm Frequency Variable Special Parameter")

    else:
        raise SDException("SDPARSER-002","incorrect parameter format (%s)"%parameter)

def is_sfg_parameter(parameter): # sfg means 'Structured Facet Group'
    if re.search("^variables?\[",parameter)!=None:
        return True
    else:
        return False

def is_rfv_parameter(parameter): # rfv means 'Realm Frequency n Variable'
    if parameter.count('[')==2:
        return True
    else:
        return False

def process_ffv_parameter(parameter,selection): # ffv means 'Free Facets n Variable'
    # sample
    #  variable[atmos rcp85 day]=cl ta hus hur wap ua va zg clcalipso

    m=re.search('variables?\[(.+)\]="?([^"=]+)"?$', parameter)
    if(m!=None):
        free_facets=m.group(1) # free facet syntax support currently only standalone values (i.e. key=value syntax is not supported inside the left member of a ffv block)
        variables=sdtools.split_values(m.group(2))

        facets={}
        facets[sdconst.PENDING_PARAMETER]=sdtools.split_values(free_facets)
        facets["variable"]=variables

        selection.childs.append(Selection(facets=facets,filename="ffvsp")) # add sub-selection ("ffvsp" means "Free Facets n Variable Special Parameter")
    else:
        raise SDException("SDPARSER-022","incorrect parameter format (%s)"%parameter)

def is_ffv_parameter(parameter): # ffv means 'Free Facets n Variable'
    if parameter.count('[')==1:
        return True
    else:
        return False

# module init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--file',default=None)
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-n','--no_default',action='store_true',help='This option prevent loading default values')
    args = parser.parse_args()

    buffer=sdbuffer.get_selection_file_buffer(path=args.file,parameter=args.parameter)
    selection=build(buffer,load_default=(not args.no_default))

    facets_groups=selection.merge_facets()
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
