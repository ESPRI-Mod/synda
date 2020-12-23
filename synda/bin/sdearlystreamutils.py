#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains early stream routines.

Notes
    - In this file, module import directives are moved near the calls, so to improve startup time.
"""

import sys
import sdconst
import sdtools
from sdtools import print_stderr
import sdexception

def test_facet_value_early(orig_stream,name,value,extract_item=False):
    """
    Notes
        - If the parameter is not present, this func return False
        - This func is intended to retrieve only singleton parameters (i.e.
          parameters which can appear only once in the Sfile)
    """
    actual_val=get_facet_value_early(orig_stream,name,extract_item)

    if actual_val is None:
        return False
    else:
        if actual_val==value:
            return True
        else:
            return False

def get_facet_value_early(orig_stream,name,extract_item=False):
    """
    Notes
        - This func is intended to retrieve only singleton parameters (i.e.
          parameters which can appear only once in the Sfile)
        - For clarity, you may prefer to use get_facet_values_early() function
          and process each case using else/if block (as in
          "is_one_variable_per_dataset_project" or in "dataset_version")
    """
    li=get_facet_values_early(orig_stream,name,extract_item)

    if len(li)==0:
        return None
    elif len(li)==1:
        return li[0]
    else:
        raise sdexception.TooMuchValueException(code='SDEARLSU-001',msg=name)

def exists_facet_value_early(orig_stream,name,extract_item=False):
    li=get_facet_values_early(orig_stream,name,extract_item)

    if len(li)==0:
        return False
    else:
        return True

def get_facet_values_early(orig_stream,name,extract_item=False):
    """Get facet values from a dqueries object at an early time (before any transformation of that object occured).

    Note
        Early means we want item from the dqueries just after it's creation
        (i.e. when no transformation (e.g. sdinference) occured yet).
        
    TODO
        Maybe find a proper way to do that
    """
    import sdstream, sdextractitem, sdignorecase, sdinference, copy, sddeferredbefore, sddeferredafter

    assert name!='type' # type cannot be inferred using this func (use infer_type() func instead)


    stream=copy.deepcopy(orig_stream) # this is not to modify the original stream at this point

    # note that A and B block order is important here
    # (if B is done before A, pending identifiers (e.g. dataset_functional_id)
    # will not be scanned by sdextractitem).

    # A
    stream=sddeferredbefore.run(stream)
    stream=sdignorecase.run(stream)
    stream=sdinference.run(stream) # this is to resolve pending parameter
    stream=sddeferredafter.run(stream)

    # B
    if extract_item:
        stream=sdextractitem.run(stream,name) # we extract item from identifier if present

    li=sdstream.get_facet_values(stream,name)

    return li

def is_one_variable_per_dataset_project(stream):
    """This func is a HACK.

    HACK description
        For some project, one dataset = one variable.
        For such cases, there is no point to display a variable list,
        so we change the route to display the dataset list.
    """

    # retrieve project from input
    project=get_facet_values_early(stream,'project',extract_item=True)

    # check
    if len(project)==0:
        print_stderr("The project name must be specified (mandatory when using 'variable/agreggation' type)")
        sys.exit(1)
    elif len(project)>1:
        print_stderr("Only one project name must be specified (mandatory when using 'variable/agreggation' type)")
        sys.exit(1)

    if sdtools.intersect(project,sdconst.PROJECT_WITH_ONE_VARIABLE_PER_DATASET):
        return True
    else:
        return False
