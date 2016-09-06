#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contain selections group helper routines."""

import re
import os
import glob
import argparse
import sdapp
from sdexception import SDException
import sdconfig
import sdparse
import sdbuffer
import sdstream
import sdlog

def projects_match(filter_projects,selection_projects):
    """
    This func test if the selection match the projects filter.
    """

    if len(selection_projects)==0:
        # selection has no project set (i.e. match all projects)

        return True

    if len(filter_projects)==0:
        # no filter set

        return True

    lists_intersect=any(i in selection_projects for i in filter_projects)

    return lists_intersect # bool

def project_filter(selections,project):
    """Keep only selections with the given projects."""
    li=[]
    for s in selections:
        facets_groups=s.merge_facets()
        if projects_match(project,sdstream.get_facet_values(facets_groups,'project')):
            li.append(s)
    return li

def filename_filter(selections,filename_pattern):
    """Keep only selections with the given pattern in the filename."""
    li=[]

    for s in selections:
        if filename_pattern in s.filename:
            li.append(s)
    return li

def is_default_file(fullpath_file):
    """Check if file is a default special selection."""

    filename=os.path.basename(fullpath_file)
    if filename.startswith('default'):
        return True
    else:
        return False

def build_selection_file_list():
    """Return full path files list."""
    files=[]
    
    for file in glob.glob( os.path.join(sdconfig.selection_folder, '*') ):
        if not os.path.isdir(file): # exclude sub-dirs
            if not is_default_file(file): # exclude default special selections
                files.append(file)

    files=sorted(files)

    return files

def build_selection_list():
    """
    Return:
        selections list.
    """
    selections=[]

    files=build_selection_file_list() # contains selection files path list (fullpath)
    for file in files:
        try:
            buffer=sdbuffer.get_selection_file_buffer(path=file)
            selection=sdparse.build(buffer)
            selections.append(selection)
        except Exception, e:
            sdlog.error("SDSELGPU-001","Exception occured (%s)"%str(e))

            raise SDException("SDSELGPU-001","Error occured while loading '%s' selection file. See log for details."%file)

    return selections

def reset_selections_status():
    """Switch new and modified selections to normal.

    DEV.
    """
    for u_s in get_selections():
        if u_s.get_status() in (sdconst.SELECTION_STATUS_NEW,sdconst.SELECTION_STATUS_MODIFIED):
            u_s.set_status(sdconst.SELECTION_STATUS_NORMAL)
            update_selection(u_s)

# module init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
