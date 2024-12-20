#!/usr/bin/python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contain selections group helper routines."""
import os
import glob
import argparse
from synda.sdt import sdapp
from synda.sdt.sdexception import SDException
from synda.sdt import sdparse
from synda.sdt import sdbuffer
from synda.sdt import sdstream
from synda.sdt import sdlog

from synda.source.config.path.tree.models import Config as TreePath


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
    selection_folder = TreePath().get("selection")
    for file in glob.glob( os.path.join(selection_folder, '*') ):
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
        except Exception as e:
            sdlog.error("SDSELGPU-001","Exception occured (%s)"%str(e))

            raise SDException("SDSELGPU-001","Error occured while loading '%s' selection file. See log for details."%file)

    return selections


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
