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
    aptitude install grads | yum install grads
"""

import sys
import argparse
import json
import re
import pexpect
import sdapp

def open_(file_path,variable,geometry='1000x600+70+0'):
    cmd='grads -l -g %s'%geometry

    # open external viewer
    child = pexpect.spawn(cmd)

    # open file
    child.expect('ga-> ')
    child.sendline('sdfopen %s'%file_path)

    # display variable
    child.expect('ga->')
    child.sendline('d %s'%variable)

    child.interact()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file')
    parser.add_argument('-v','--variable')
    args = parser.parse_args()

    open_(args.file,args.variable)
