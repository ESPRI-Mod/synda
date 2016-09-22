#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains type inference engine.

Notes
    - This module do the same kind of job as sdinference, but for the type only.
    - You CAN'T use sdinference here because sdinference needs to know the
      'type' to do it's job.

TODO
    group this module and sdinference together (add an option to have two
    behaviour: with and without type).
"""

import sdconst
import sddquery
import sdconfig

def _infer_from_unnamed_facet(pvalue):
    if pvalue==sdconst.SA_TYPE_FILE:
        type_=sdconst.SA_TYPE_FILE
    elif pvalue==sdconst.SA_TYPE_AGGREGATION:
        type_=sdconst.SA_TYPE_AGGREGATION
    elif pvalue=='Variable': # Alias
        type_=sdconst.SA_TYPE_AGGREGATION
    elif pvalue==sdconst.SA_TYPE_DATASET:
        type_=sdconst.SA_TYPE_DATASET
    else:
        type_=None

    return type_

def _infer_from_unnamed_identifier(pvalue):
    import sdidtest

    if sdidtest.is_filename(pvalue):
        type_=sdconst.SA_TYPE_FILE
    elif sdidtest.is_dataset_functional_id(pvalue):
        type_=sdconst.SA_TYPE_DATASET
    # TODO: test below is a bit tricky as for some project, dataset==variable, and for other, dataset!=variable.
    #elif sdidtest.is_variable_functional_id(pvalue):
    #    type_=sdconst.SA_TYPE_AGGREGATION
    elif sdidtest.is_file_functional_id(pvalue):
        type_=sdconst.SA_TYPE_FILE
    elif sdidtest.is_dataset_local_path(pvalue):
        type_=sdconst.SA_TYPE_DATASET
    # TODO: test below is a bit tricky as for some project, dataset==variable, and for other, dataset!=variable.
    #elif sdidtest.is_variable_local_path(pvalue):
    #    type_=sdconst.SA_TYPE_AGGREGATION
    elif sdidtest.is_file_local_path(pvalue):
        type_=sdconst.SA_TYPE_FILE
    else:
        type_=None

    return type_

def _infer_from_pending_parameter(pending_parameters):
    type_=None

    for pvalue in pending_parameters:

        type_=_infer_from_unnamed_facet(pvalue) # if user set search-api type, we also switch the display type
        if type_ is not None:
            break

        type_=_infer_from_unnamed_identifier(pvalue) # switch display type based on identifier
        if type_ is not None:
            break

    return type_

def _named_to_unnamed(dquery):
    transformed_parameters=[]

    for k,v in dquery.iteritems():
        if k!=sdconst.PENDING_PARAMETER:
            if len(v)==0:
                pass
            elif len(v)==1:
                transformed_parameters.append(v[0])
            if len(v)>1:
                # this is when we have for example
                # dataset_id=id1,id2,id3
                # This case si not supported (i.e. we do not infere type from a list of value).
                pass

    return transformed_parameters

def _infer_from_dquery(dquery):
    """
    TODO
        hacky func: improve this.
    """
    type_=None

    # handle named identifier (e.g. name=value)
    transformed_parameters=_named_to_unnamed(sddquery.search_api_parameters(dquery)) # HACK: transform named to unnamed so to reuse the same solver
    type_=_infer_from_pending_parameter(transformed_parameters)

    # handle unnamed identifier (e.g. value)
    if type_ is None:
        if sdconst.PENDING_PARAMETER in dquery:
            pending_parameters=dquery[sdconst.PENDING_PARAMETER]
            type_=_infer_from_pending_parameter(pending_parameters)

    return type_

def infer_display_type(stream):
    """Set type depending on user input (e.g. ID, named FACET, unnamed FACET)."""

    type_=None

    if len(stream)==1:
        dquery=stream[0]
        type_=_infer_from_dquery(dquery)

    if type_ is None:
        type_=sdconfig.sdtsaction_type_default

    return type_
