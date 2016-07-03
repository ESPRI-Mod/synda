#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains helper routines."""

import sys
import os
import re

def is_root():
    if os.geteuid() == 0:
        return True
    else:
        return False

def print_module_variables(variables):
    """Func used when using a python module to store configuration parameters."""
    li=[]
    for k,v in variables.items():
        if '__' not in k: # prevent display of python system variables
            if k!='li':   # prevent display of this list
                if isinstance(v, (str,int,basestring,float,bool,list, tuple)):
                    li.append("%s=%s"%(k,v))
    li=sorted(li)

    for v in li:
        print v

def url_contains_limit_keyword(url):
    """Check if limit is set."""
    if 'limit=' in url:
        return True
    else:
        return False

def grep(li,pattern):

    if pattern is None:
        return li
    else:
        expr = re.compile(pattern)
        return filter(expr.search,li)

def grep_light(li,pattern):

    if pattern is None:
        return li
    else:
        new_li=[v for v in li if pattern in v]
        return new_li

def print_stdout(msg):
    print msg

def print_stderr(msg=""):
    sys.stderr.write("%s\n"%msg)

def multi_columns_listing(li):
    for a,b,c in zip(li[::3],li[1::3],li[2::3]):
        print '{0:<30}{1:<30}{2:<}'.format(a,b,c)

def union(a, b):
    """Return the union of two lists (and remove duplicate).

    Not used.
    """
    if a==None and b<>None:
        return list(set(b))
    if a<>None and b==None:
        return list(set(a))
    if a==None and b==None:
        return []
    if a<>None and b<>None:
        return list(set(a) | set(b))

def extract_digit(li):
    """This fonction separates pure digit value(s) from 'alum' items.

    Args:
        li (list)

    Not used.
    """
    alum=[]
    digit=[]

    for token in li:
        if token.isdigit():
            digit.append(int(token)) # change the type from string to int
        else:
            alum.append(token)
    
    return (alum,digit)

def split_values(values):
    if ',' in values:
        # delimiter is ','

        r = re.compile('\s*,\s*')
    else:
        # delimiter is ' '

        r = re.compile('\s+')

    return r.split(values)

def compute_rate(size,duration):
    """Unit: bytes / seconds.

    Not used.
    """
    if duration==0:
        return 0
    else:
        return size / duration
