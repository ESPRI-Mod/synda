#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

import collections
import datetime as dt
import uuid
import os

from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy import Enum
from sqlalchemy import PrimaryKeyConstraint

from sdt.bin.db.utils import Entity


# from sdt.bin.db.utils import convertor
# from errata.utils.constants import *


class Dataset(Entity):
    """
    A dataset object
    """
    # SQLAlchemy directives.
    __tablename__ = 'dataset'
    # Core columns
    dataset_id = Column(Integer, primary_key=True)
    dataset_functional_id = Column(Text)
    status = Column(Text)
    path = Column(Text)
    path_without_version = Column(Text)
    version = Column(Text)
    local_path = Column(Text)
    latest = Column(Integer)
    project = Column(Text)
    model = Column(Text)

    # Tracking columns
    crea_date = Column(DateTime)
    last_mod_date = Column(DateTime)
    latest_date = Column(Text)
    last_done_transfer_date = Column(Text)
    template = Column(Text)
    timestamp = Column(Text)

    def __repr__(self):
        """Instance representation.

        """
        return "<Dataset(id={}, version={}, is latest={}, path=={})>".format(
            self.dataset_functional_id, self.version, self.latest, self.local_path)

    def get_full_local_path(self, prefix):
        add_prefix = True

        if len(self.local_path) > 0:
            if self.local_path[0] == '/':
                add_prefix = False

        if add_prefix:
            path = os.path.join(prefix, self.local_path)
        else:
            path = self.local_path

        return path


# TODO consider this todict conversion
# def to_dict(self, resources, facets):
#     """Encode object as a simple dictionary.
#
#     :param list resources: Collection of issue resources.
#     :param list facets: Collection of issue facets.
#
#     """
#     def _get_facets():
#         return sorted(['{}:{}'.format(i.facet_type, i.facet_value) for i in facets if i.issue_uid == self.uid])
#
#     def _get_reources(resource_type):
#         return sorted([i.resource_location for i in resources \
#                        if i.issue_uid == self.uid and i.resource_type == resource_type])
#
#     obj = convertor.to_dict(self)
#     obj['facets'] = _get_facets()
#     obj['datasets'] = _get_reources(RESOURCE_TYPE_DATASET)
#     obj['materials'] = _get_reources(RESOURCE_TYPE_MATERIAL)
#     obj['urls'] = _get_reources(RESOURCE_TYPE_URL)
#
#     return obj

class File(Entity):
    """
    A file object
    """
    # SQLAlchemy directives.
    __tablename__ = 'file'
    # Core columns
    file_id = Column(Integer, primary_key=True)
    url = Column(Text)
    file_functional_id = Column(Text)
    filename = Column(Text)
    local_path = Column(Text)
    data_node = Column(Text)
    checksum = Column(Text)
    checksum_type = Column(Text)
    duration = Column(Integer)
    size = Column(Integer)
    model = Column(Text)
    project = Column(Text)
    variable = Column(Text)
    dataset_id = Column(Text)
    insertion_group_id = Column(Integer)

    # Tracking columns
    rate = Column(Integer)
    start_date = Column(Text)
    end_date = Column(Text)
    crea_date = Column(Text)
    status = Column(Text)
    error_msg = Column(Text)
    sdget_status = Column(Text)
    sdget_error_msg = Column(Integer)
    priority = Column(Integer)
    tracking_id = Column(Text)
    last_access_date = Column(Text)

    timestamp = Column(Text)

    def __repr__(self):
        """Instance representation.

        """
        return "<File(id={}, checksum={}, sdget_status=={})>".format(
            self.file_functional_id, self.checksum, self.sdget_status)

    def get_full_local_path(self, prefix):
        add_prefix = True

        if len(self.local_path) > 0:
            if self.local_path[0] == '/':
                add_prefix = False

        if add_prefix:
            path = os.path.join(prefix, self.local_path)
        else:
            path = self.local_path

        return path


class Export(Entity):
    """
    A export object
    """
    # SQLAlchemy directives.
    __tablename__ = 'export'
    # Core columns
    dataset_id = Column(Integer, primary_key=True)
    export_date = Column(Text)

    def __repr__(self):
        """Instance representation.

        """
        return "<Export(dataset id={}, export date={})>".format(
            self.dataset_id, self.export_date)


class Selection(Entity):
    """
    A selection object
    """
    __tablename__ = 'selection'

    selection_id = Column(Integer, primary_key=True)
    filename = Column(Text)
    checksum = Column(Text)
    status = Column(Text)

    def __repr__(self):
        """
        instance representation
        """
        return "<Selection(selection id={}, filename={}, checksum={}, status={})>".format(
            self.selection_id, self.filename, self.checksum, self.status)


class SelectionFile(Entity):
    """
    A selection object
    """
    __tablename__ = 'selection__file'
    __table_args__ = (
        PrimaryKeyConstraint('selection_id', 'file_id'),
    )
    selection_id = Column(Integer, nullable=False)
    file_id = Column(Integer, nullable=False)

    def __repr__(self):
        """
        instance representation
        """
        return "<Selection file(selection id={}, file id={})>".format(
            self.selection_id, self.file_id)


class FileWithoutSelection(Entity):
    """
    A file without selection object
    """
    __tablename__ = 'file_without_selection'
    __table_args__ = (
        PrimaryKeyConstraint('file_id'),
    )
    file_id = Column(Integer, nullable=False)

    def __repr__(self):
        """
        instance representation
        """
        return "<File without selection(file id={})>".format(self.file_id)


class FileWithoutDataset(Entity):
    """
    A file without dataset object
    """
    __tablename__ = 'file_without_dataset'
    __table_args__ = (
        PrimaryKeyConstraint('file_id'),
    )
    file_id = Column(Integer, nullable=False)

    def __repr__(self):
        """
        instance representation
        """
        return "<File without dataset(file id={})>".format(self.file_id)


class Param(Entity):
    """
    Param object
    """
    __tablename__ = 'param'
    __table_args__ = (
        PrimaryKeyConstraint('name', 'value'),
    )
    name = Column(Text)
    value = Column(Text)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        """
        instance representation
        """
        return "<Param(name={}, value={})>".format(self.name, self.value)


class Version(Entity):
    """
    Version object
    """
    __tablename__ = 'version'
    __table_args__ = (
        PrimaryKeyConstraint('version'),
    )

    version = Column(Text)

    def __repr__(self):
        """
        instance representation
        """
        return "<Version(version={})>".format(self.version)


class History(Entity):
    """
    History object
    """
    __tablename__ = 'history'
    history_id = Column(Integer, primary_key=True)
    action = Column(Text)
    selection_filename = Column(Text)
    crea_date = Column(Text)
    insertion_group_id = Column(Integer)
    selection_file_checksum = Column(Text)
    selection_file = Column(Text)

    def __repr__(self):
        """
        instance representation
        """
        return "<History(action={}, selection file name={}, creation date={})>" \
            .format(self.action, self.selection_filename, self.crea_date)


class Event(Entity):
    """
    Event object
    """
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    name = Column(Text)
    status = Column(Text)
    project = Column(Text)
    model = Column(Text)
    dataset_pattern = Column(Text)
    variable = Column(Text)
    filename_pattern = Column(Text)
    crea_date = Column(Text)
    priority = Column(Integer)

    def __repr__(self):
        """
        instance representation
        """
        return "<Event(name={}, status={}, priority={})>" \
            .format(self.name, self.status, self.priority)


class GenericCache(Entity):
    """
    Generic cache object
    """
    __tablename__ = 'generic_cache'
    __table_args__ = (
        PrimaryKeyConstraint('realm', 'name', 'value'),
    )
    realm = Column(Text)
    name = Column(Text)
    value = Column(Text)

    def __repr__(self):
        """
        instance representation
        """
        return "<Generic cache(realm={}, name={}, value={})>" \
            .format(self.realm, self.name, self.value)


# Set unique description (case insensitive) index.
Index('idx_file_1', File.status)
Index('idx_file_2', File.priority)
Index('idx_file_3', File.crea_date)
Index('idx_file_4', File.file_functional_id, unique=True)
Index('idx_file_5', File.dataset_id)
Index('idx_file_6', File.tracking_id)
Index('idx_file_7', File.checksum)
Index('idx_file_8', File.insertion_group_id)
Index('idx_file_9', File.project)
Index('idx_file_10', File.model)
Index('idx_file_11', File.filename)
Index('idx_file_12', File.local_path, unique=True)
Index('idx_file_13', File.data_node)
Index('idx_dataset_1', Dataset.dataset_functional_id, unique=True)
Index('idx_dataset_2', Dataset.status)
Index('idx_dataset_3', Dataset.path_without_version)
Index('idx_dataset_4', Dataset.path, unique=True)
Index('idx_dataset_5', Dataset.local_path)
Index('idx_export_1', Export.dataset_id)
Index('idx_selection_1', Selection.filename, unique=True)
Index('idx_selection__file_1', SelectionFile.selection_id, SelectionFile.file_id, unique=True)
Index('idx_file_without_selection_1', FileWithoutSelection.file_id)
Index('idx_file_without_dataset_1', FileWithoutDataset.file_id)
Index('idx_param_1', Param.name, Param.value, unique=True)
Index('idx_event_1', Event.name)
Index('idx_event_2', Event.status)
Index('idx_event_1', Event.crea_date)
