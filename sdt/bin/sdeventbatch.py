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
import sdlog
import sdtools
import sdutils
import sddao
import sdvariable
import sdfiledao
import sddb
import sdproduct
import sdmodifyquery
import sdevent
from sdexception import SDException
from sdprogress import SDProgressDot

def file_():

    # check that only files with 'done' status exist
    TODO

    # reset files status from done to waiting
    sdmodifyquery.change_status(sdconst.TRANSFER_STATUS_DONE,sdconst.TRANSFER_STATUS_WAITING)

    # reset dataset status to empty, and dataset latest flag to false
    sdmodifyquery.wipeout_datasets_flags(status=sdconst.DATASET_STATUS_EMPTY)

    # mimic end of transfer
    TODO
    dbpagination=DBPagination()
    files=dbpagination.get_files()
    while len(files)>0:
        for f in files:

            # PAYLOAD
            sddb.conn.execute("update file set checksum_type=? where file_id=?",(checksum_type,f.file_id))
            sdfiledao.update_file(tr) # set status to done
            file_complete_event(f) # trigger end of transfer file event for all files

        conn.commit() # commit block
        files=dbpagination.get_files() # next block
        sdprogress.SDProgressDot.print_char(".")

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
