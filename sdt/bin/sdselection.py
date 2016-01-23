#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains selection related functions."""

import os
import glob
import sdlog
import argparse
from subprocess import call
import sdapp
import sdtools
from sdexception import SDException
import sdconfig

def cat_selection(filename):
    buf=read_selection(filename)
    for line in buf:
        print line

def print_selection(filename):
    title='Filename: %s'%filename

    sdtools.print_stderr()
    sdtools.print_stderr(title)
    sdtools.print_stderr('='*len(title))
    sdtools.print_stderr()
    cat_selection(filename)
    sdtools.print_stderr()

def read_selection(filename):
    path="%s/%s"%(sdconfig.selections_folder,filename)
    with open(path, 'r') as fh:
        buf=fh.readlines()

    buf=[line.rstrip('\n') for line in buf] # strip line break

    return buf

def edit_selection(file):
    EDITOR = os.environ.get('EDITOR','vim')
    li=[EDITOR, file]
    call(li)

def add_selection(us):
    # compute selection checksum from scratch
    l__file_checksum=computechecksum(us.getselectionfilefullpath())

    if not existsSelection(us):
        # add selection in database if missing

        us.setChecksum(l__file_checksum)
        us.setStatus(sdconst.SELECTION_STATUS_NEW)
        us.setFullScan(True)

        insertSelection(us) # warning: this modify us object (set PK)

    else:
        # selection already in database

        from_db_us=fetchselection(us.getFilename()) # retrieve us from DB
        us.setSelectionID(from_db_us.getSelectionID())                  # copy DB id

        # check if same checksums
        if l__file_checksum==from_db_us.getChecksum():
            # same checksum

            # retrieve status
            us.setStatus(from_db_us.getStatus())
            us.setChecksum(from_db_us.getChecksum())

            if us.getStatus()==sdconst.SELECTION_STATUS_NORMAL:

                # nothing to do here (let (a) and (b) decide if we need fullscan)
                pass

            elif us.getStatus()==sdconst.SELECTION_STATUS_MODIFIED:

                us.setFullScan(True)

            elif us.getStatus()==sdconst.SELECTION_STATUS_NEW:

                us.setFullScan(True)

            else:

                raise SDException("SYNDATSEL-ERR071","unknown status")

        else:
            # same checksum
            # checksum differ

            sdlog.info("SYNDASEL-197","%s selection has been modified (marked for fullscan)"%us.getFilename())


            us.setChecksum(l__file_checksum)                  # update checksum
            us.setStatus(sdconst.SELECTION_STATUS_MODIFIED) # update status

            updateselection(us)

    # add selection in selection list
    # TODO
    _selections[us.getFilename()]=us

def bind_file_to_selection():
    # update junction table

    try:
        sddao.insertselectiontransferjunction(file,self._conn)
    except Exception,e:
        self.log("SYNDATF-ERR044","fatal error (selection_id=%s,transfer_id=%i)"%(u_s.getSelectionID(),file.getTransferID()))
        raise

def set_selection(selection_filenames):
    """Load selections."""

    if selection_filenames<>None:
        # load selections specified on CLI (using "-t" option)
        
        for filename in selection_filenames:
            us=selection_builder(filename)
            add_selection(us)

    else:
        # load all selections

        for filename in getselectionfilelist():
            us=selection_builder(filename)

            if us.group==sdconst.DEFAULT_GROUP: # without "-t" option we only add default group us (i.e. currently, you have to use "-t" option to process selection which are not in the default group)
                add_selection(us)

def selection_builder(filename):
    """Dev."""

    # check if file exists in "selection" folder
    fullpath_file="%s/%s"%(g__selection_folder,filename)
    if not os.path.exists(fullpath_file):
        raise SDException("SYNDATSEL-ERR099","file not found: %s (use \"-l\" option to list available selections)"%fullpath_file)

    # create selection object (from file)
    us=Selection(filename=filename,logger=getLogger())

    return us

def is_dataset_inside_selections(verylightdatasetid):
    for us in _selections.values():
        if us.is_dataset_inside_selection(verylightdatasetid):
            return True # found it

    return False # not found in any selections

def PROC0012():
    """Mark all selections as done (aka "normal", "complete"..) and set the checksum."""
    for filename in getselectionfilelist():
        us=Selection(filename=filename,logger=getLogger())
        us.setStatus(sdconst.SELECTION_STATUS_NORMAL)
        l__checksum=compute_checksum(us.getSelectionFileFullPath())
        us.setChecksum(l__checksum)
        updateselection(us)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
