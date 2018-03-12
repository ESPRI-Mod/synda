#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains metadata disk-based storage routines.

Note
    sdmts means 'SynDa Metadata Temporary Storage'
"""

import os
import json
import copy
import uuid
import sqlite3
import contextlib
import shutil
import sddbpagination
import sdconst
import sdconfig

# abstract class
class Storage():

    def get_chunks(self,io_mode):
        pass

    def merge(self,store):
        """Merge the store given in argument into the current store."""
        pass

    def copy(self):
        pass

    def delete(self):
        pass

    def get_one_file(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

class MemoryStorage(Storage):

    def __init__(self):
        self.files=[]

    def count(self):
        return len(self.files)

    def set_files(self,files):
        self.files=files

    def get_files(self):
        return self.files

    def get_chunks(self,io_mode): # io_mode is not used (but need to be present to respect Storage contract)
        chunksize=sdconst.PROCESSING_CHUNKSIZE

        for i in xrange(0, self.count(), chunksize):
            yield self.files[i:i+chunksize]

    def merge(self,store):
        self.files.extend(store.get_files())

    def append_files(self,files):
        self.files.extend(files)

    def delete(self):

        # This block can be removed as garbage collector manage the 'list' deletion (self.files) automatically.
        # Only kept to enforce symetry with DatabaseStorage.
        #
        if hasattr(self,'files'):
            del self.files

    def copy(self): # WARNING: calling this func triggers two lists in memory at the same time !
        cpy=MemoryStorage()
        cpy.files=copy.deepcopy(self.files)
        return cpy

    def get_one_file(self):
        assert self.count()>0
        return self.files[0]

class DatabaseStorage(Storage):

    def __init__(self,dbfile=None):
        if dbfile is None:
            self.dbfile=get_uniq_fullpath_db_filename()
            assert not os.path.isfile(self.dbfile) # dbfile shouldn't exist at this time

            self.connect()
            self.create_table()
        else:
            # this case is only to duplicate the object (see copy method)

            self.dbfile=dbfile
            self.connect()

    def create_table(self,name='data'):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("CREATE TABLE %s (%s)"%(name,columns_definition))
            self.conn.commit()

    def drop_table(self):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("DROP TABLE data")
            self.conn.commit()

    def count(self):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT COUNT(1) from data")
            res = int(c.fetchone()[0])
        return res

    def set_files(self,files):

        # WARNING: slow perf here. Maybe remove the dbfile.
        self.drop_table()
        self.create_table()

        self.append_files(files)

    def get_files(self):
        """WARNING: this func loads all the data in memory."""

        li=[]
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT %s from data"%columns)
            rs=c.fetchone()
            while rs is not None:


                # multicol table
                #
                #=rs[0]
                #=rs[1]
                #=rs[2]
                #attrs=json.loads(rs[3])
                #
                #tu=(rs[0],rs[1],rs[2],attrs)
                #li.append(tu)


                # monocol table
                attrs=json.loads(rs[0])
                li.append(attrs)

                rs=c.fetchone()
        return li

    def get_chunks(self,io_mode):
        if io_mode=='generator':
            return self.get_chunks_GENERATOR()
        elif io_mode=='pagination':
            return self.get_chunks_PAGINATION()
        else:
            assert False

    def get_chunks_GENERATOR(self):
        """This method is used to loop over all files using yield without consuming too much memory ('yield' based impl.)

        Note
            It is not possible to write anywhere in the db file between two yields !
        """
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("select %s from data"%columns)
            while True:
                results = c.fetchmany(sdconst.PROCESSING_CHUNKSIZE)
                if not results:
                    break

                # WARNING: two (sdconst.PROCESSING_CHUNKSIZE) list in memory at the same time
                li=[]
                for rs in results:
                
                    # multicol table
                    #attrs=json.loads(rs[3])

                    # monocol table
                    attrs=json.loads(rs[0])

                    li.append(attrs)

                yield li

    def get_chunks_PAGINATION(self):
        dbpagination=sddbpagination.DBPagination('bla','foo',self.conn)
        dbpagination.reset()

        files=dbpagination.get_files()
        while len(files)>0:
            for t in files:

                # <= PERFORM TASK HERE

                update_db(l__date,t.file_id)

            sddb._conn.commit() # commit block

            files=dbpagination.get_files()

    def merge(self,store):
        store.disconnect() # not sure if needed (more info => https://www.sqlite.org/lang_detach.html)

        self.conn.execute("ATTACH DATABASE '%s' AS incoming"%store.dbfile)
        self.conn.execute("insert into data select %s from incoming.data"%columns)
        self.conn.commit() # commit all attached databases (TBC)
        self.conn.execute("DETACH DATABASE incoming")

        store.connect() # not sure if needed

    def append_files(self,files):

        # WARNING: slow perf here. Maybe replace rown-by-row insert with array insert.
        with contextlib.closing(self.conn.cursor()) as c:
            for f in files:

                # multicol table
                #tu=(f['id'], f['size'], f['data_node'], json.dumps(f))
                #c.execute("INSERT INTO data (%s) VALUES (?, ?, ?, ?)"%columns, tu)

                # monocol table
                tu=(json.dumps(f),)
                c.execute("INSERT INTO data (%s) VALUES (?)"%columns, tu)

            self.conn.commit()

    def delete(self):
        self.disconnect()
        if os.path.isfile(self.dbfile):
            os.unlink(self.dbfile)

    def connect(self):
        self.conn = sqlite3.connect(self.dbfile, isolation_level='DEFERRED')

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def copy(self):

        # create new db file for the copy
        dbfile_cpy=get_uniq_fullpath_db_filename()
        assert not os.path.isfile(dbfile_cpy) # dbfile shouldn't exist at this time

        # temporariy close ori connection
        self.disconnect()

        # copy dbfile
        shutil.copy(self.dbfile,dbfile_cpy)

        # create new instance
        cpy=DatabaseStorage(dbfile=dbfile_cpy)

        # re-open ori connection
        self.connect()

        return cpy

    def get_one_file(self):
        assert self.count()>0
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT %s from data LIMIT 1"%columns)
            rs=c.fetchone()

            # multicol table
            #=rs[0]
            #=rs[1]
            #=rs[2]
            #=rs[3]

            # monocol table
            file_=json.loads(rs[0])

        return file_

def get_uniq_fullpath_db_filename():
    dbfilename='sdt_transient_storage_%s_%s.db'%(str(os.getpid()),str(uuid.uuid4()))
    dbfile=os.path.join(sdconfig.db_folder,dbfilename)
    return dbfile

def get_new_store(lowmem=False):
    if lowmem:
        return DatabaseStorage()
    else:
        return MemoryStorage()

# init.

#columns='id, size, data_node, attrs'
#columns_definition='id TEXT PRIMARY KEY, size INT, data_node TEXT, attrs TEXT'

columns='attrs'
columns_definition='attrs TEXT'
