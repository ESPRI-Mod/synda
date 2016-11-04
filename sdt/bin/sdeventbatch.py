#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains event batch routines."""

import argparse
import sdapp
from sdprogress import SDProgressDot
import sdlog
import sdtools
import sdutils
import sddao
import sdvariable
import sdfiledao
import sddb
import sdproduct
import sdevent
from sdexception import SDException

def file_():
    TODO
    f=sddao.get_file(file_functional_id=args.file_functional_id)
    file_complete_event(f)

def variable():
    """Artificially trigger event for all complete variable 
    (usually, events are triggered after each transfer completion).

    This func is used, for example, to trigger pipeline on already downloaded data.
    """

    li=sdvariable.get_complete_variables(project='CMIP5')

    # add the dataset_pattern (used in the next step to remove duplicates)
    for v in li:
        v.dataset_pattern=sdproduct.replace_output12_product_with_wildcard(v.dataset_path)

    # Remove duplicates
    #
    # Duplicate exist because of those two facts:
    #   - we have '*' in product in dataset pattern
    #   - there are cases when a variable exist on both product (output1 and output2)
    #
    di={}
    for v in li:
        di[(v.dataset_pattern,v.name)]=v

    # load
    for v in di.values():
        SDProgressDot.print_char(".")
        sdevent.variable_complete_output12_event(v.project,v.model,v.dataset_pattern,v.name,commit=False)
    sddb.conn.commit() # we do all insertion commit in one transaction

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode',choices=['file','variable'],required=True)
    args = parser.parse_args()

    if args.mode=='file':
        file_()
    elif args.mode=='variable':
        variable()
