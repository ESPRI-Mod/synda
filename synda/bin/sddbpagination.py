#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains pagination mecanism to prevent using too much memory.

Note
  It is possible to update records along the way with this module.

Also see
    sdlargequery
"""

import argparse
import sdapp
import sdprogress

# make a light version of this module without the four imports below for sddb / sddbversion use
import sddb
import sdtypes
import sdsqlutils
import sdnormalize

class DBPagination():
    DEFAULT_CHUNKSIZE=2500

    def __init__(self,table='file',columns='*',conn=sddb.conn,chunksize=DEFAULT_CHUNKSIZE):
        self.conn=conn
        self.table=table
        self.columns=columns
        self.pagination_block_size=chunksize
        self.pagination_offset=0
        self.pagination_limit=self.pagination_block_size

    def reset(self):
        self.pagination_offset=0
        self.pagination_limit=self.pagination_block_size

    def get_items(self):
        """
        This method is used to loop over all files (note that we use pagination here not to load all the rows in memory)

        Note
          This method is like get_files_batch(), but use pagination instead of using yield
        """
        c = self.conn.cursor()

        q="select %s from %s limit %d offset %d" % (self.columns,self.table,self.pagination_limit,self.pagination_offset)
        #q="select * from file order by file_id ASC"

        # debug
        #print q

        c.execute(q)
        results = c.fetchall()


        c.close()

        self.pagination_offset+=self.pagination_block_size # move OFFSET for the next call

        return results

    def get_files(self):
        files=[]
        results=self.get_items()
        for rs in results:
            f=sdsqlutils.get_object_from_resultset(rs,sdtypes.File)
            files.append(f)
        return files

# init.

if __name__ == '__main__': # test only
    parser = argparse.ArgumentParser()

    dbpagination=DBPagination('bla','foo')

    files=dbpagination.get_files()
    while len(files)>0:
        for f in files:

            # PAYLOAD
            checksum_type=sdnormalize.normalize_checksum_type(f.checksum_type)
            sddb.conn.execute("update file set checksum_type=? where file_id=?",(checksum_type,f.file_id))

        conn.commit() # commit block
        files=dbpagination.get_files() # next block
        sdprogress.SDProgressDot.print_char(".")
