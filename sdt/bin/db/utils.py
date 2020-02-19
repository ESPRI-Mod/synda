#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime as dt
import random

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sdt.bin.db import session

# Sqlalchemy metadata singleton.
METADATA = MetaData()


class _BaseEntity(object):
    """Base entity sub-classed from all synda db types.

    """

    def __init__(self):
        """Constructor.

        """
        super(_BaseEntity, self).__init__()


# Mixin with sql alchemy.
Entity = declarative_base(metadata=METADATA, cls=_BaseEntity)


def text_filter(qry, field, key):
    """Applies a text based filter expression.

    """
    return qry.filter(sqlalchemy.func.upper(field) == unicode(key).strip().upper())


def update(entity):
    """Updates entity fields
    :param db.Entity item: A supported entity instance
    """
    session.update(entity)


def delete(entity):
    """Marks entity instance for deletion.

    :param db.Entity item: A supported entity instance.

    """
    session.delete(entity)


def delete_all(etype):
    """Deletes all entities of passed type.

    :param class etype: A supported entity type.

    """
    delete_by_facet(etype)


def delete_by_facet(etype, filter_expression=None):
    """Delete entity instance by id.

    :param class etype: A supported entity type.
    :param expression filter_expression: Facet filter expression.

    """
    qry = session.query(etype)
    if filter_expression:
        qry = qry.filter(filter_expression)
    qry.delete()


def delete_by_id(etype, entity_id):
    """Delete entity instance by id.

    :param class etype: A supported entity type.
    :param int entity_id: id of entity.

    """
    delete_by_facet(etype, etype.id == entity_id)


def delete_by_name(etype, entity_name):
    """Deletes an entity instance by it's name.

    :param class etype: A supported entity type.
    :param unicode entity_name: Name of entity.

    """
    delete_by_facet(etype, etype.name == entity_name)


def exec_query(etype, qry, get_iterable=False):
    """Executes a query and return result (sorted if is a collection).

    :param class etype: A supported entity type.
    :param expression qry: A SqlAlchemy query expression.
    :param bool get_iterable: Flag indicating whether to return an iterable or not.

    :returns: Entity or entity collection.
    :rtype: Sub-class of db.Entity

    """
    return sort(etype, qry.all()) if get_iterable else qry.first()


def get_all(etype):
    """Gets all instances of the entity.

    :param class etype: A supported entity type.

    :returns: Entity collection.
    :rtype: list

    """
    return get_by_facet(etype, order_by=etype.id, get_iterable=True)


def get_by_facet(etype, qfilter=None, order_by=None, get_iterable=False):
    """Gets entity instance by facet.

    :param class etype: A supported entity type.
    :param expression qfilter: Query filter expression.
    :param expression order_by: Sort expression.
    :param bool get_iterable: Flag indicating whether to return an iterable or not.

    :returns: Entity or entity collection.
    :rtype: Sub-class of db.Entity

    """
    qry = session.query(etype)
    if qfilter is not None:
        qry = qry.filter(qfilter)
    if order_by is not None:
        qry = qry.order_by(order_by)

    return exec_query(etype, qry, get_iterable)


def get_by_id(etype, entity_id):
    """Gets entity instance by id.

    :param class etype: A supported entity type.
    :param int entity_id: An entity identifier.

    :returns: Entity with matching id.
    :rtype: Sub-class of db.Entity

    """
    return get_by_facet(etype, qfilter=etype.id == entity_id)


def get_by_name(etype, entity_name):
    """Gets an entity instance by it's name.

    :param class etype: A supported entity type.
    :param unicode entity_name: Name of entity.

    :returns: Entity with matching name.
    :rtype: Sub-class of db.Entity

    """
    return get_by_facet(etype, qfilter=etype.name == entity_name)


def get_count(etype, qfilter=None):
    """Gets count of entity instances.

    :param class etype: A supported entity type.
    :param expression qfilter: Query filter expression.

    :returns: Entity collection count.
    :rtype: int

    """
    qry = session.query(etype)
    if qfilter is not None:
        qry = qry.filter(qfilter)

    return qry.count()


def get_random(etype):
    """Returns a random instance.

    :param class etype: Type of instance to be returned.

    :returns: A random item from the cache.
    :rtype: Sub-class of db.Entity

    """
    collection = get_all(etype)
    if len(collection):
        return collection[random.randint(0, len(collection) - 1)]


def get_random_sample(etype):
    """Returns a random instance sample.

    :param class etype: Type of instances to be returned.

    :returns: A random sample from the db.
    :rtype: list

    """
    collection = get_all(etype)
    if len(collection):
        return random.sample(collection, random.randint(1, len(collection)))

    return []


def insert(entity):
    """Adds a newly created model to the session.

    :param db.Entity item: A supported entity instance.

    """
    session.add(entity)

    return entity


def sort(etype, collection, sort_key=None):
    """Sorts collection via type sort key.

    :param class etype: A supported entity type.
    :param iterable collection: Collection of entities.
    :param function sort_key: Key to use when sorting.

    :returns: Sorted collection.
    :rtype: list

    """
    if sort_key is None:
        if hasattr(etype, 'name'):
            sort_key = lambda i: "" if i.name is None else i.name.upper()
        elif hasattr(etype, 'ordinal_position'):
            sort_key = lambda i: i.ordinal_position
        elif hasattr(etype, 'code'):
            sort_key = lambda i: "" if i.code is None else i.code.upper()
        else:
            sort_key = lambda i: i.id

    return [] if collection is None else sorted(collection, key=sort_key)


def persist(hydrate, etype, retriever):
    """Persists to db by either creating a new instance or
       retrieving and updating an existing instance.

    :param function hydrate: Function to populate an instance.
    :param class etype: Type of entity to be persisted.
    :param function retriever: Function to retrieve an instance.

    """
    try:
        instance = etype()
        hydrate(instance)
        session.insert(instance)
    except IntegrityError:
        session.rollback()
        instance = retriever()
        hydrate(instance)
        session.update(instance)

    return instance


def as_datetime_string(col):
    """Converts a column result into a datetime string.

    :param sqlalchemy.Column col: Collumn to be converted.

    :returns: The column wrapped in a date string conversion function.
    :rtype: sqlalchemy.Column

    """
    return sqlalchemy.func.to_char(col, "YYYY-MM-DD HH24:MI:ss.US")


def as_date_string(col):
    """Converts a column result into a date string.

    :param sqlalchemy.Column col: Column to be converted.

    :returns: The column wrapped in a date string conversion function.
    :rtype: sqlalchemy.Column

    """
    return sqlalchemy.func.to_char(col, "YYYY-MM-DD")


def dataset_groupby(table, criterion_group, criterion_order):
    return session.query(table).group_by(criterion_group).order_by(func.max(criterion_order)).all()
