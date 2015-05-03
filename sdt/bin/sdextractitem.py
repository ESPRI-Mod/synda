#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
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

import sdapp
import sdparam
import sddquery
import sdprint

def run(facets_groups,key):
    for facets_group in facets_groups:
        if key not in facets_group:
            li=get_functional_identifiers(facets_group)

            if len(li)==0:
                # nothing to extract

                pass

            elif len(li)==1:

                identifier=li[0]

                value=extract_item(identifier,key)

                if value is None:
                    # We come here for example with osb4MIPs project,
                    # as model doesn't exist for Obs
                    # (e.g. synda search obs4MIPs.PCMDI.CloudSat.mon.v1.cfadDbze94_obs4MIPs_CloudSat_L3_V2.0_20081101_20081130.nc -y)

                    #print 'Cannot extract %s from functional identifier'%key
                    pass

                else:
                    facets_group[key]=[value]

            elif len(li)>1:
                # this case is not supported yet

                pass

    return facets_groups

def param_values(key):
    if key=='model':
        # this case is specific, because we want normalized model here, not non-normalized ones

        return sdparam.models.keys()
    else:
        return sdparam.params[key]

def extract_item(identifier,key):
    """Extract item from functional identifier."""
    for param_value in param_values(key):
        if match(param_value,identifier):
            return param_value

    return None

def match(param_value,identifier):
    delimiter='.' # TAG54543

    # prepare value
    value_=delimiter+param_value+delimiter # tricks to prevent nested matches (e.g. when searching for 'HadGEM2-AO' model, 'HadGEM2-A' model is returned instead..)

    # prepare identifier
    identifier_=delimiter+identifier+delimiter # add missing delimiter for the first and last item (i.e. we need first and last item to also have both left and right delimiter)

    if value_.lower() in identifier_.lower(): # ignore case is required, as we have, for example, 'CMIP5' in search-API parameter, and 'cmip5' in metadata..
        return True
    else:
        return False

def get_functional_identifiers(facets_group):
    """
    Return functional identifiers list, if any.
    """
    functional_identifiers=['dataset_id','title','instance_id'] # 'local_path' is currently not supported. To add it, just be sure to use '/' instead of '.' in TAG54543.

    li=[]
    for id_ in functional_identifiers:
        if id_ in facets_group:
            v=sddquery.get_scalar(facets_group,id_)
            li.append(v)

    return li

# module init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load( sys.stdin )
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
