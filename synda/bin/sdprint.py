#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains generic printing routines."""

import json
import sys
import argparse

def print_format(files,format,print_only_one_item=False,fh=sys.stdout):
    """Print files list with given format."""

    if print_only_one_item:
        files=[files[0]]
        format='indent' # force format to indent when displaying only one item

    if format == 'raw':
        fh.write("%s\n"%json.dumps(files))
    elif format == 'line':
        for f in files:
            fh.write("%s\n"%json.dumps(f))
    elif format == 'indent':
        fh.write("%s\n"%json.dumps(files,indent=4, separators=(',', ': ')))
    elif format == 'value':
        for f in files:
            for k,v in f.iteritems():
                if isinstance(v,dict):

                    # WARNING: breaks genericity
                    #
                    # dict type is not supported in this mode (so yes, it's not
                    # very regular as this mode cannot be used for some
                    # attributes e.g. 'attached_parameters', but there are not
                    # many option when you want to flatten a multilevel tree
                    # into a list..)
                    #
                    pass

                elif isinstance(v,list):
                    for item in v:
                        fh.write("%s\n"%item)
                elif isinstance(v,basestring):
                    fh.write("%s\n"%v)
                elif isinstance(v,int):
                    fh.write("%d\n"%v)
                elif isinstance(v,float):
                    fh.write("%f\n"%v)

formats=['raw','line','indent','value']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-F','--format',choices=formats,default='indent')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    print_format(files,args.format)
