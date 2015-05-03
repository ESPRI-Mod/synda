#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains func used to retrieve information from 'parameter' token list."""

import argparse
import sdpipeline
import sdstream
import sdi18n

def extract_values_from_parameter(parameter,name):
    facets_groups=sdpipeline.parse(parameter)
    values=sdstream.get_facet_values(facets_groups,name)
    return values

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)
    args = parser.parse_args()

    # test
    values=extract_values_from_parameter(args.parameter,'project')
    print values
