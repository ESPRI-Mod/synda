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
import copy
import sdconfig
import uuid
import sddbpagination
import sdconst

class MemoryStorage():

    def __init__(self):
        self.files=[]

    def count(self):
        return len(self.files)

    def set_files(self,files):
        self.files=files

    def get_files(self):
        return self.files

    def get_chunks(self,**kw):
        chunksize=kw.get('chunksize',sdconst.PROCESSING_CHUNKSIZE)

        for i in xrange(0, self.count(), chunksize):
            yield sef.files[i:i+chunksize]

    def append_files(self,files):
        self.files.extend(files)

    def add_attached_parameters(self,attached_parameters):
        for f in self.files:
            assert 'attached_parameters' not in f
            f['attached_parameters']=copy.deepcopy(attached_parameters)

    def delete(self):
        del self.files

class DatabaseStorage():

    def __init__(self):
        self.dbfilename='sdt_transient_storage_%s.db'%str(uuid.uuid4())
        self.dbfile=os.path.join(sdconfig.db_folder,dbfilename)

        assert not os.path.isfile(self.dbfile) # dbfile shouldn't exist at this time

        self.conn = sqlite3.connect(self.dbfile, isolation_level='DEFERRED')

        self.create_table()

    def create_table(self,name='data'):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("CREATE TABLE %s (id TEXT PRIMARY KEY, size INT, data_node TEXT, attrs TEXT)"%name)
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
        """WARNING: this func doesn't work on lowmem machine (<64Go RAM)."""

        li=[]
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT %s from data"%columns)
            rs=c.fetchone()
            while rs is not None:
                #li.append((rs[0],rs[1],rs[2],rs[3]))
                li.append(json.loads(rs[3]))
                rs=c.fetchone()
        return li

    def get_chunks(self,**kw):
        mode=kw.get('mode','generator')
        chunksize=kw.get('chunksize',sdconst.PROCESSING_CHUNKSIZE)

        if mode=='generator':
            return self.get_chunks_GENERATOR(chunksize=chunksize)
        elif mode=='pagination':
            return self.get_chunks_PAGINATION(chunksize=chunksize)
        else:
            assert False

    def get_chunks_GENERATOR(self,chunksize=sdconst.PROCESSING_CHUNKSIZE):
        """This method is used to loop over all files using yield without consuming too much memory ('yield' based impl.)

        Note
            It is not possible to write anywhere in the db file between two yields !
        """
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("select %s from data"%columns)
            while True:
                results = c.fetchmany(chunksize)
                if not results:
                    break
                li=[json.loads(rs[3]) for rs in results] # WARNING: two (sdconst.PROCESSING_CHUNKSIZE) list in memory at the same time
                yield li

    def get_chunks_PAGINATION(self,chunksize=sdconst.PROCESSING_CHUNKSIZE):
        dbpagination=DBPagination()
        dbpagination.reset()

        files=dbpagination.get_files()
        while len(files)>0:
            for t in files:

                # <= PERFORM TASK HERE

                update_db(l__date,t.file_id)

            sddb._conn.commit() # commit block of insertSelectionTransferJunction

            files=dbpagination.get_files()

    def append_files(self,files):

        # WARNING: slow perf here. Maybe replace rown-by-row insert with array insert.
        with contextlib.closing(self.conn.cursor()) as c:
            for f in files:
                c.execute("INSERT INTO data (%s) VALUES (?, ?, ?, ?)"%columns, (f['id'], f['size'], f['data_node'], json.dumps(f)))
            self.conn.commit()

    def add_attached_parameters(self,attached_parameters):

        # WARNING: slow perf here. Maybe replace with 'ALTER TABLE foo RENAME TO bar'
        li=self.get_files()
        for f in li:
            assert 'attached_parameters' not in f
            f['attached_parameters']=copy.deepcopy(attached_parameters)
        self.set_files(self,li)

    def delete(self):
        if self.conn is not None:
            conn.close()
        if os.path.isfile(self.dbfile):
            os.unlink(self.dbfile)

def get_store(lowmem=False):
    if lowmem:
        return DatabaseStorage()
    else:
        return MemoryStorage()

# init.

columns="id, size, data_node, attrs"
