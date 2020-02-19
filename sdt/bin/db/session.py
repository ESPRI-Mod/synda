#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

import contextlib
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sdt.bin.sdconfig

# SQLAlchemy engine.
sa_engine = None

# DB connection string used to create SQLAlchemy engine.
_sa_connection = None

# SQLAlchemy session.
_sa_session = None


# TODO convert the prints into proper logging.


@contextlib.contextmanager
def create(connection=None, commitable=False):
    """Starts & manages a db session.

    :param connection: DB connection information.
    :type connection: str | sqlalchemy.Engine
    :param bool commitable: Flag indicating whether to auto-commit.

    """
    _start(connection)
    print("db connection [{}] opened".format(id(_sa_session)))

    try:
        yield
    except Exception as err:
        msg = "An unhandled exception occurred within context of a {} database connection: {}."
        msg = msg.format("writeable" if commitable else "readonly", err)
        # logger.log_db(msg)
        raise err
    else:
        if commitable:
            commit()
        print("db connection [{}] closed".format(id(_sa_session)))
    finally:
        _end()


def _start(connection=None):
    """Starts a db session.

    :param connection: Either a db connection string or a SQLAlchemy db engine.
    :type connection: str | sqlalchemy.Engine

    """
    global sa_engine
    global _sa_session
    global _sa_connection

    # Set default connection.
    if connection is None:
        connection = 'sqlite:///' + sdt.bin.sdconfig.db_file
        print('connection info ' + connection)
    # Set engine.
    if _sa_connection != connection:
        _sa_connection = connection
        sa_engine = create_engine(connection, echo=False)
        # sa_engine = create_engine(connection,
        #                           echo=False,
        #                           connect_args={"options": "-c timezone=utc"})
        print("db engine instantiated: {}".format(id(sa_engine)))

    # Set session.
    _sa_session = sessionmaker(bind=sa_engine)()
    # _sa_session = sessionmaker(bind=sa_engine, expire_on_commit=False)()


def _end():
    """Ends a session.

    """
    global _sa_session

    if _sa_session is not None:
        _sa_session.close()
        _sa_session = None


def commit():
    """Commits a session.

    """
    if _sa_session is not None:
        _sa_session.commit()


def rollback():
    """Rolls back a session.

    """
    if _sa_session is not None:
        _sa_session.rollback()


def insert(instance, auto_commit=True):
    """Adds a newly created type instance to the session and optionally commits the session.

    :param Entity instance: A db type instance.
    :param bool auto_commit: Flag indicating whether a commit is to be issued.

    """
    if instance is not None and _sa_session is not None:
        _sa_session.add(instance)
        if auto_commit:
            commit()

    return instance


def add(instance, auto_commit=True):
    """Adds a newly created type instance to the session and optionally commits the session.

    :param Entity instance: A db type instance.
    :param bool auto_commit: Flag indicating whether a commit is to be issued.

    """
    return insert(instance, auto_commit)


def delete(instance, auto_commit=True):
    """Marks a type instance for deletion and optionally commits the session.

    :param instance: A db type instance.
    :type instance: sub-class of Entity

    :param auto_commit: Flag indicating whether a commit is to be issued.
    :type auto_commit: bool

    """
    if instance is not None and _sa_session is not None:
        _sa_session.delete(instance)
        if auto_commit:
            commit()


def update(instance, auto_commit=True):
    """Marks a type instance for update and optionally commits the session.

    :param db.Entity instance: A db type instance.
    :param bool auto_commit: Flag indicating whether a commit is to be issued.

    """
    if instance is not None and _sa_session is not None:
        if auto_commit:
            commit()

    return instance


def query(*etypes):
    """Begins a query operation against a session.

    """
    if len(etypes) == 0 or _sa_session is None:
        return None

    q = None
    for etype in etypes:
        q = _sa_session.query(etype) if q is None else q.join(etype)
    return q


def raw_query(*args):
    """Initiates a raw query operation against a SQLAlchemy session.

    Avoids having to expose directly the underlying SQLAlchemy session.

    """
    return _sa_session.query(*args)
