#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module is a plugin to handle Synda "varname:cmor_tblname" syntax.

Note
    sdvct means "SynDa Varname:Cmor_Tblname"
"""
import copy


def run(facets_groups):
    new_facets_groups = []
    for facets_group in facets_groups:
        if "variable" in facets_group:

            variables_with_cmortable = []
            variables_without_cmortable = []

            for v in facets_group['variable']:
                if ":" in v:
                    variables_with_cmortable.append(v)
                else:
                    variables_without_cmortable.append(v)

            del facets_group['variable']

            # create new query for each variable with cmortable
            for v in variables_with_cmortable:
                (varname, cmor_table) = v.split(':')
                f_cpy = copy.deepcopy(facets_group)

                f_cpy['variable'] = [varname]
                f_cpy['cmor_table'] = [cmor_table]

                new_facets_groups.append(f_cpy)

            # create one more query for all variable without cmortable
            if len(variables_without_cmortable) > 0:
                f_cpy = copy.deepcopy(facets_group)
                f_cpy['variable'] = variables_without_cmortable

                new_facets_groups.append(f_cpy)

        else:
            new_facets_groups.append(facets_group)

    return new_facets_groups
