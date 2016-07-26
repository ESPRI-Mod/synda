#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains pagination mecanism to prevent using too much memory."""

import sdapp

class DBPagination():

    def __init__(self,table,columns,chunksize,conn):
        self.conn=conn
        self.table=table
        self.columns=columns
        self.pagination_offset=0
        self.pagination_limit=0
        self.pagination_block_size=chunksize

    def reset(self):
        self.pagination_limit=self.pagination_block_size
        self.pagination_offset=0

    def get_files(self):
        """
        This method is used to loop over all files (note that we use pagination here not to load all the rows in memory !!!)

        Note
          This method is like get_files_batch(), but use pagination instead of using yield
        """

        files=[]

        c = self.conn.cursor()
        q="select %s from %s limit %d offset %d" % (self.columns,self.table,self.pagination_limit,self.pagination_offset)
        c.execute(q)

        results = c.fetchall()

        for rs in results:
            files.append(FIXME)

        c.close()

        # move OFFSET for the next call
        self.pagination_offset+=self.pagination_block_size

        return files

# init.
