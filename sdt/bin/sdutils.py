#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains generic functions.

Also see
    sdtools
"""

import sys
import os
import datetime
import json
import hashlib
from functools import partial
import subprocess
import argparse
import sdapp
import sdconst
from sdexception import SDException,FileNotFoundException

def get_transfer_protocol(url):
    if url.startswith('http://'):
        return sdconst.TRANSFER_PROTOCOL_HTTP
    elif url.startswith('https://'):
        return sdconst.TRANSFER_PROTOCOL_HTTP
    elif url.startswith('gsiftp://'):
        return sdconst.TRANSFER_PROTOCOL_GRIDFTP
    else:
        assert False

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    Args:
        - "question" is a string that is presented to the user.
        - "default" is the presumed answer if the user just hits <Enter>.

    Returns:
        - True if answer is yes
        - False if answer is no
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def get_status_output(args, **kwargs):
    """
    Args:
        args (list): command + arguments

    Notes
        - handle exit status conversion and raise exception if child didn't complete normally
        - as 'commands' module is deprecated, use this func as replacement
        - also note that with this func, stderr and stdout are retrieved separately
          (was not the case in 'commands' module)
        - also note that there is a 'getstatusoutput' func in subprocess
          maybe better to use it directly
          (more info https://docs.python.org/3.3/library/subprocess.html#legacy-shell-invocation-functions)
    """

    kwargs['stdout']=subprocess.PIPE
    kwargs['stderr']=subprocess.PIPE
    kwargs['universal_newlines']=False

    p = subprocess.Popen(args, **kwargs)

    stdout, stderr = p.communicate()

    return p.returncode, stdout, stderr

def get_last_access_date(self,t):
    """
    return value example
      "2011-08-19 11:19:29.675221"
    """
    l__epoch=0

    try:
        l__epoch=os.path.getatime(t.get_full_local_path())
        l__date_str=datetime.datetime.fromtimestamp(l__epoch).strftime('%Y-%m-%d %H:%M:%S.%f')
        return l__date_str
    except OSError, e:
        if e.errno == errno.ENOENT: # errno.ENOENT = no such file or directory
            raise FileNotFoundException("%s"%str(e)) # cast exception to Synda exception
        else:
            raise SDException("SYDUTILS-632","fatal I/O error (%s)"%str(e))

def replace_product(path,new_product):
    for product in ['output','output1','output2']: # doesn't work if product is on the first or on the last position
        path=path.replace('/'+product+'/','/'+new_product+'/')
    return path

def compute_checksum(file_fullpath,checksum_type="md5"):
    with open(file_fullpath, mode='rb') as f:

        d=None
        if checksum_type=="md5":
            d = hashlib.md5()
        elif checksum_type=="MD5":
            d = hashlib.md5()
        elif checksum_type=="sha256":
            d = hashlib.sha256()
        else:
            raise SDException("SYDUTILS-422","incorrect checksum_type (%s,%s)"%(file_fullpath,checksum_type))

        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

def cast(value,dest_type_):
    """Cast value to the given destination type.
    
    Notes
        - BEWARE when doing string2bool cast, because bool('false') DO NOT returns false !
        - Currently, typing is not formally defined in Synda.
          Basically, you have a mix of losely typed attribute (i.e. string) and strongely typed attribute (Python type).
          So, some bool parameter are stored as Python bool and some are stored as Python string.
          Also, some int are stored as Python int, and some are stored as string.
          In most cases, strongely typed are Synda attributes and losely typed are Search-API attributes.
          This func is used to make this mess transparent as much as possible.
        - TODO: in the future, maybe switch all to 'strongely typed' or all to
          'losely typed' (i.e. mix of both is kind of a mess). Maybe 'strongely typed' is better,
          because in this case, no need to cast for each non-string attribute, only need to
          have a final to_string method when serializing (e.g. for the search-api call).
    """

    # if None, return None without any cast
    if value is None:
        return None

    # if dest_type_ has not been set, return value as is (i.e. do not cast)
    if dest_type_ is None:
        return value

    src_type=type(value)

    # Special case when casting string to bool
    if dest_type_==bool:
        if src_type==str:

            # we only accept 'true' and 'false' format for bool stored as string

            if value=='true':
                casted_value=True
            elif value=='false':
                casted_value=False
            else:
                raise SDException("SYDUTILS-400","Incorrect bool value (%s)"%value)
        else:
            casted_value=dest_type_(value)
    else:
        casted_value=dest_type_(value)

    return casted_value

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    res=query_yes_no('test ?', default="yes")
    print res
