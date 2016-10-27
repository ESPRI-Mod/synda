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

class DBPagination():

    def __init__(self,table,columns,conn,chunksize=DEFAULT_CHUNKSIZE):
        self.conn=conn
        self.table=table
        self.columns=columns
        self.pagination_block_size=chunksize
        self.pagination_offset=0
        self.pagination_limit=0

        self.reset()

    def reset(self):
        self.pagination_offset=0
        self.pagination_limit=self.pagination_block_size

    def get_files(self):
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

        """
        Notes
            - if returning the resultset directly cause problem, try casting it to list
            - we may cast row to object here, but it makes the module less generic

        e.g.

        files=[]
        for rs in results:
            files.append(sdsqlutils.get_object_from_resultset(rs,File))
        return files
        """

        c.close()

        self.pagination_offset+=self.pagination_block_size # move OFFSET for the next call

        return results

# init.

DEFAULT_CHUNKSIZE=2500

if __name__ == '__main__': # test only
    import sddb, sdnormalize # do not move sddb at the top (this module is not currently but may be used by sddb module)

    parser = argparse.ArgumentParser()

    dbpagination=DBPagination('bla','foo',sddb.conn)

    files=dbpagination.get_files()
    while len(files)>0:
        for f in files:

            # PAYLOAD
            checksum_type=sdnormalize.normalize_checksum_type(f.checksum_type)
            sddb.conn.execute("update file set checksum_type=? where file_id=?",(checksum_type,f.file_id))

        conn.commit() # commit block
        files=dbpagination.get_files() # next block
        sdprogress.SDProgressDot.print_char(".")
