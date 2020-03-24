#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright €œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reservedâ€
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module extracts an item from id.

Example
    input
        cordex.output.EUR-44i.HMS.ECMWF-ERAINT.evaluation.r1i1p1.ALADIN52.v1.fx.orog.v20140319
        model
    output
        ALADIN52
"""

from sdt.bin.commons.param import sdparam
from sdt.bin.commons.param import sddquery
from sdt.bin.commons.utils import sdprint


def run(facets_groups, key):
    for facets_group in facets_groups:
        if key not in facets_group:
            li = get_functional_identifiers(facets_group)

            for identifier in li:
                process_item(facets_group, identifier, key)

    return facets_groups


def param_values(key):
    if key == 'model':
        # this case is specific, because we want normalized model here, not non-normalized ones

        return sdparam.models.keys()
    else:
        return sdparam.params[key]


def extract_item(identifier, key):
    """Extract item from functional identifier."""
    li = param_values(key)
    for param_value in li:
        assert param_value is not None
        if match(param_value, identifier):
            return param_value

    return None


def match(param_value, identifier):
    delimiter = '.'  # TAG54543

    assert param_value is not None

    # prepare value
    # tricks to prevent nested matches
    # (e.g. when searching for 'HadGEM2-AO' model, 'HadGEM2-A' model is returned instead..)

    value_ = delimiter + param_value + delimiter
    # prepare identifier
    # add missing delimiter for the first and last item
    # (i.e. we need first and last item to also have both left and right delimiter)
    identifier_ = delimiter + identifier + delimiter
    # ignore case is required, as we have, for example, 'CMIP5' in search-API parameter, and 'cmip5' in metadata..
    if value_.lower() in identifier_.lower():
        return True
    else:
        return False


def get_functional_identifiers(facets_group):
    """
    Return functional identifiers list, if any.
    """
    # 'local_path' is currently not supported. To add it, just be sure to use '/' instead of '.' in TAG54543.
    functional_identifiers = ['dataset_id', 'title',
                              'instance_id']

    li = []
    for id_ in functional_identifiers:
        if id_ in facets_group:
            values = sddquery.get_list(facets_group, id_, default=[])
            li.extend(values)

    return li


def extract_variable_name_from_filename(filename):
    """
    Not used
    """

    rege = re.compile("^([^_]+)_.+$")

    rege_result = rege.match(filename)  # sample => sfcWind_day_HadGEM2-ES_piControl_r1i1p1_19091201-19191130.nc
    if rege_result is not None:
        variable = rege_result.group(1)  # sample => sfcWind
    else:
        assert False

    return variable


def process_item(facets_group, identifier, key):
    value = extract_item(identifier, key)

    if value is None:
        # We come here for example with osb4MIPs project,
        # as model doesn't exist for Obs
        # (e.g. synda search obs4MIPs.PCMDI.CloudSat.mon.v1.cfadDbze94_obs4MIPs_CloudSat_L3_V2.0_20081101_20081130.nc -y)

        # print 'Cannot extract %s from functional identifier'%key
        pass

    else:
        if key not in facets_group:
            facets_group[key] = [value]
        else:
            facets_group[key].append(value)
