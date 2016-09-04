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
import argparse
from subprocess import call
import sdapp
import sdlog
import sdtools
import sdutils
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
    path="%s/%s"%(sdconfig.selection_folder,filename)
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
    l__file_checksum=sdutils.compute_checksum(us.get_selection_file_full_path())

    if not exists_selection(us):
        # add selection in database if missing

        us.set_checksum(l__file_checksum)
        us.set_status(sdconst.SELECTION_STATUS_NEW)
        us.set_fullscan(True)

        insertSelection(us) # warning: this modify us object (set PK)

    else:
        # selection already in database

        from_db_us=fetch_selection(us.get_filename()) # retrieve us from DB
        us.set_selection_id(from_db_us.get_selection_id())                  # copy DB id

        # check if same checksums
        if l__file_checksum==from_db_us.get_checksum():
            # same checksum

            # retrieve status
            us.set_status(from_db_us.get_status())
            us.set_checksum(from_db_us.get_checksum())

            if us.get_status()==sdconst.SELECTION_STATUS_NORMAL:

                # nothing to do here (let (a) and (b) decide if we need fullscan)
                pass

            elif us.get_status()==sdconst.SELECTION_STATUS_MODIFIED:

                us.set_fullscan(True)

            elif us.get_status()==sdconst.SELECTION_STATUS_NEW:

                us.set_fullscan(True)

            else:

                raise SDException("SYNDATSEL-071","unknown status")

        else:
            # same checksum
            # checksum differ

            sdlog.info("SYNDASEL-197","%s selection has been modified (marked for fullscan)"%us.get_filename())


            us.set_checksum(l__file_checksum)                  # update checksum
            us.set_status(sdconst.SELECTION_STATUS_MODIFIED) # update status

            update_selection(us)

    # add selection in selection list
    # TODO
    _selections[us.get_filename()]=us

def bind_file_to_selection():
    # update junction table

    try:
        sddao.insert_selection_transfer_junction(file,self._conn)
    except Exception,e:
        self.log("SYNDATF-044","fatal error (selection_id=%s,transfer_id=%i)"%(u_s.get_selection_id(),file.get_transfer_id()))
        raise

def set_selection(selection_filenames):
    """Load selections."""

    if selection_filenames is not None:
        # load selections specified on CLI (using "-t" option)
        
        for filename in selection_filenames:
            us=selection_builder(filename)
            add_selection(us)

    else:
        # load all selections

        for filename in get_selection_file_list():
            us=selection_builder(filename)

            if us.group==sdconst.DEFAULT_GROUP: # without "-t" option we only add default group us (i.e. currently, you have to use "-t" option to process selection which are not in the default group)
                add_selection(us)

def selection_builder(filename):
    """Dev."""

    # check if file exists in "selection" folder
    fullpath_file="%s/%s"%(g__selection_folder,filename)
    if not os.path.exists(fullpath_file):
        raise SDException("SYNDATSEL-099","file not found: %s (use \"-l\" option to list available selections)"%fullpath_file)

    # create selection object (from file)
    us=Selection(filename=filename,logger=get_logger())

    return us

def is_dataset_inside_selections(very_light_dataset_id):
    for us in _selections.values():
        if us.is_dataset_inside_selection(very_light_dataset_id):
            return True # found it

    return False # not found in any selections

def reset():
    """Mark all selections as done (aka "normal", "complete"..) and set the checksum."""
    for filename in get_selection_file_list():
        us=Selection(filename=filename,logger=get_logger())
        us.set_status(sdconst.SELECTION_STATUS_NORMAL)
        cs=sdutils.compute_checksum(us.get_selection_file_full_path())
        us.set_checksum(cs)
        update_selection(us)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
