# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
 Tests driven by pytest

 object : Table creation & cursor

"""
import os
import pytest
from synda.tests.manager import Manager

manager = Manager()
manager.set_tests_mode()
from synda.tests.tests.config.file.db.utils import create_table
from synda.source.constants import get_env_folder

db_file = os.path.join(
    os.path.join(
        get_env_folder(),
        "db",
    ),
    "sdt_empty.db",
)


@pytest.mark.on_all_envs
def test_create_file_table():
    create_table(db_file, 'file')


@pytest.mark.on_all_envs
def test_create_dataset_table():
    create_table(db_file, 'dataset')


@pytest.mark.on_all_envs
def test_create_export_table():
    create_table(db_file, 'export')


@pytest.mark.on_all_envs
def test_create_failed_url_table():
    create_table(db_file, 'failed_url')


@pytest.mark.on_all_envs
def test_create_file_without_dataset_table():
    create_table(db_file, 'file_without_dataset')


@pytest.mark.on_all_envs
def test_create_file_without_selection_table():
    create_table(db_file, 'file_without_selection')


@pytest.mark.on_all_envs
def test_create_generic_cache_table():
    create_table(db_file, 'generic_cache')


@pytest.mark.on_all_envs
def test_create_history_table():
    create_table(db_file, 'history')


@pytest.mark.on_all_envs
def test_create_param_table():
    create_table(db_file, 'param')


@pytest.mark.on_all_envs
def test_create_selection_table():
    create_table(db_file, 'selection')


@pytest.mark.on_all_envs
def test_create_selection_file_table():
    create_table(db_file, 'selection__file')


@pytest.mark.on_all_envs
def test_create_version_table():
    create_table(db_file, 'version')
