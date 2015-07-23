#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains actions used by 'synda' script."""

def autoremove(args):
    pass

def cache(args):
    pass

def certificate(args):
    pass

def daemon(args):
    pass

def dump(args):
    pass

def help(args):
    pass

def history(args):
    pass

def install(args):
    pass

def list(args):
    pass

def param(args):
    pass

def queue(args):
    pass

def remove(args):
    pass

def replica(args):
    pass

def reset(args):
    pass

def retry(args):
    pass

def search(args):
    pass

def selection(args):
    pass

def show(args):
    pass

def stat(args):
    pass

def test(args):
    pass

def upgrade(args):
    pass

def update(args):
    pass

def version(args):
    pass

def watch(args):
    pass

if __name__ == '__main__':
    li=[]

    # retrieve module methods
    for k,v in locals().items():
        if '__' not in k: # prevent display of python system variables
            if k!='li':   # prevent display of this list
                li.append(k)

    for v in sorted(li):
        print v
