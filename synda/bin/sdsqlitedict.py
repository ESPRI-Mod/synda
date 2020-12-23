#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains disk persistent dict using sqlite as backend.

Note
    I didn't use the original pypi package because
        - 'setup.py' was non-compatible with Python 2.6
        - it installed heavy dependencies I don't need
          ("kyotocabinet >= 1.9", "cassandra-driver >= 2.1.3")

Credit
    https://pypi.python.org/pypi/persistentdicts/2.0.4
"""

import json
import collections
import sqlite3
import contextlib

class ProxyDict(collections.MutableMapping):

    def __init__(self, target=None, *args, **kwargs):
        if target is None:
            self.target = dict()
        else:
            self.target = target
        self.update(dict(*args, **kwargs))

    def __len__(self):
        return len(self.target)

    def __getitem__(self, key):
        return self.invert_trans(self.target[self.trans(key)])

    def __setitem__(self, key, value):
        self.target[self.trans(key)] = self.trans(value)

    def __delitem__(self, key):
        del self.target[self.trans(key)]

    def iteritems(self):
        for key, value in self.target.iteritems():
            yield self.invert_trans(key), self.invert_trans(value)

    def __iter__(self):
        for key in self.target:
            yield self.invert_trans(key)

    def __str__(self):
        return str(dict(self))

    def has_key(self, key):
        return self.trans(key) in self.target

    def copy(self):
        return ProxyDict(target=self.target)

    def trans(self, x):
        return x

    def invert_trans(self, x):
        return x

class JsonProxyDict(ProxyDict):

    def trans(self, x):
        return json.dumps(x)

    def invert_trans(self, x):
        return json.loads(x)

    def copy(self):
        return JsonProxyDict(target=self.target)

class SqliteStringDict(collections.MutableMapping):
    """
    Sqlite database with an interface of dictionary
    """

    def __init__(self, path, table, isolation_level):
        self.path = path
        self.table = table
        self.isolation_level = isolation_level
        self.conn = sqlite3.connect(self.path,
                                    isolation_level=self.isolation_level)

        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("CREATE TABLE IF NOT EXISTS %s "
                      "(key TEXT PRIMARY KEY, value TEXT)" % self.table)
            self.conn.commit()

    def __len__(self):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT COUNT(*) from %s" % self.table)
            res = int(c.fetchone()[0])
        return res

    def __getitem__(self, key):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT value FROM %s "
                      "WHERE key = ? LIMIT 1" % self.table,
                      (key,))
            row = c.fetchone()
            if row is None:
                raise KeyError
            return row[0]

    def __setitem__(self, key, value):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("INSERT OR REPLACE INTO %s (key, value)"
                      "VALUES (?, ?)" % self.table, (key, value))
            self.conn.commit()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("DELETE FROM %s "
                      "WHERE key=?" % self.table,
                      (key,))
            self.conn.commit()

    def __contains__(self, key):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT 1 FROM %s "
                      "WHERE key=? LIMIT 1" % self.table,
                      (key,))
            row = c.fetchone()
            return row is not None

    def iteritems(self):
        with contextlib.closing(self.conn.cursor()) as c:
            for row in c.execute(
                    "SELECT key, value FROM %s" % self.table):
                yield row[0], row[1]

    def __iter__(self):
        for key, value in self.iteritems():
            yield key

class SqliteDict(JsonProxyDict):

    def __init__(self, path=":memory:", table="dict",
                 isolation_level="DEFERRED", *args, **kwargs):
        target = SqliteStringDict(path, table=table,
                                  isolation_level=isolation_level)
        super(JsonProxyDict, self).__init__(target)
        self.update(dict(*args, **kwargs))

    def copy(self):
        t = self.target
        return SqliteDict(t.path, t.table, t.isolation_level)
