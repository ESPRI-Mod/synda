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

# previous stuff
#
#import sdsqlitedict
#
#self.store=sdmts.get_metadata_tmp_storage()
#metadata.store[k] = files # store metadata on-disk
#
#for k in metadata.store:
#    files+=metadata.store[k]
#
#def get_metadata_tmp_storage():
#
#    cleanup() # empty previous storage if any
#
#    d = sdsqlitedict.SqliteDict(path=dbfile)
#
#    return d
#
#def cleanup():
#    if os.path.isfile(dbfile):
#        os.unlink(dbfile)

class MemoryStorage():

    def __init__(self):
        self.files=[]

    def set_files(self,files):
        self.files=files

    def count(self):
        return len(self.files)

    def get_files(self):
        return self.files

    def add_attached_parameters(self,attached_parameters):
        for f in self.files:
            assert 'attached_parameters' not in f
            f['attached_parameters']=copy.deepcopy(attached_parameters)

class DatabaseStorage():

    def __init__(self):

        assert not os.path.isfile(dbfile) # dbfile shouldn't exist at this time

        self.conn = sqlite3.connect(dbfile, isolation_level='DEFERRED')

        self.create_table()

    def create_table(self,name='data'):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("CREATE TABLE %s (id TEXT PRIMARY KEY, size INT, data_node TEXT, attrs TEXT)"%name)
            self.conn.commit()

    def drop_table(self):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("DROP TABLE data")
            self.conn.commit()

    def set_files(self,files):

        # WARNING: slow perf here. Maybe remove the dbfile.
        self.drop_table()
        self.create_table()

        # WARNING: slow perf here. Maybe replace rown-by-row insert with array insert.
        with contextlib.closing(self.conn.cursor()) as c:
            for f in files:
                c.execute("INSERT INTO data (id, size, data_node, attrs) VALUES (?, ?, ?, ?)", (f['id'], f['size'], f['data_node'], json.dumps(f)))
            self.conn.commit()

    def count(self):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT COUNT(1) from data")
            res = int(c.fetchone()[0])
        return res

    def get_files(self):

        # WARNING: slow perf here. Maybe use 'yield' keyword as in sdsqlitedict module.
        li=[]
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT id, size, data_node, attrs from data")
            rs=c.fetchone()
            #li.append((rs[0],rs[1],rs[2],rs[3])
            li.append(json.loads(rs[3]))
        return li

    def add_attached_parameters(self,attached_parameters):

        # WARNING: slow perf here. Maybe replace with 'ALTER TABLE foo RENAME TO bar'
        li=self.get_files()
        for f in li:
            assert 'attached_parameters' not in f
            f['attached_parameters']=copy.deepcopy(attached_parameters)
        self.set_files(self,li):

def get_store(lowmem=False):
    if lowmem:
        return DatabaseStorage()
    else:
        return MemoryStorage()

# init.

#FIXME to handle collision-free dbfile naming (as now used by sdtypes.py)
#FIXME close db connection et remove the dbfile once done
dbfilename='sdt_transient_storage.db'
dbfile=os.path.join(sdconfig.db_folder,dbfilename)
