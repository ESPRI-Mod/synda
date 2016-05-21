#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module displays data contained in a netcdf file.

Note
    This module is experimental. To use it you have to manually install the dependencies.

Dependencies
    pip install pexpect
    aptitude install grads
"""

import sys
import argparse
import json
import re
import pexpect
import sdapp

def extract_variable_name_from_filename(filename):
    rege=re.compile("^([^_]+)_.+$")

    rege_result=rege.match(filename) # sample => sfcWind_day_HadGEM2-ES_piControl_r1i1p1_19091201-19191130.nc
    if rege_result!=None:
        variable=rege_result.group(1) # sample => sfcWind
    else:
        assert False

    return variable

def open(filename):
    cmd='grads -l -g 1000x600+70+0'

    # open external viewer
    child = pexpect.spawn(cmd)

    # open file
    child.expect('ga-> ')
    child.sendline('sdfopen %s'%filename)

    # display variable
    variable_name=extract_variable_name_from_filename(filename)
    child.expect('ga-> ')
    child.sendline('d %s'%variable_name)

    child.interact()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename')
    args = parser.parse_args()

    open(args.filename)
