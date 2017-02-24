#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains administration routines."""

import argparse
import sdapp
import sddeletefile
import sdlog
import sdhistorydao
import sdfiledao
import sdconst
import sddb

def delete_insertion_group(insertion_group_id):
    files=sdfiledao.get_files(insertion_group_id=insertion_group_id)
    files=[f for f in files] # exclude files already marked for deletion
    if len(files)>0:
        for f in files:
            sddeletefile.deferred_delete(f.file_functional_id)
            sdlog.info("SDINSGRP-001","File marked for deletion (%s)"%f.file_functional_id)
        sddb.conn.commit() # final commit (we do all update in one transaction).

        # deferred mode
        # if effective deletion is done by the daemon, uncomment this  line
        #print "%i file(s) marked for deletion"%len(files)

        # immediate mode
        sddeletefile.delete_transfers_lowmem()
        print "%i file(s) deleted"%len(files)

        sdhistorydao.add_history_line(sdconst.ACTION_DELETE,insertion_group_id=insertion_group_id)
    else:
        print "Nothing to delete"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action',choices=['delete'],required=True)
    parser.add_argument('-i', '--insertion_group_id')
    args = parser.parse_args()

    if args.insertion_group_id is not None:
        delete_insertion_group(args.insertion_group_id)
