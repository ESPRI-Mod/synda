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

 Sub-command : GET
 Optional argument : internal file
 Operating context :
"""
import pytest

from synda.tests.manager import Manager
Manager().set_tests_mode()

from synda.source.config.file.internal.models import Config
from synda.source.config.process.download.constants import get_transfer_protocols
from synda.source.config.process.download.hack.constants import get_projects as get_hack_projects
from synda.source.config.file.internal.models import Config as Internal
from synda.tests.tests.config.file.internal.constants import FILENAMES

internal = Internal()


@pytest.mark.on_all_envs
def test_return_default_value():
    config = Config(FILENAMES["standard"])
    assert config.api_esgf_search_domain_name == internal.api_esgf_search_domain_name
    assert config.processes_chunksize == internal.processes_chunksize
    assert config.is_processes_get_files_caching
    assert config.hack_projects_with_one_variable_per_dataset == internal.hack_projects_with_one_variable_per_dataset
    assert config.processes_http_client == internal.processes_http_client
    assert config.processes_transfer_protocols == internal.processes_transfer_protocols


@pytest.mark.on_all_envs
def test_processes_get_files_caching():
    config = Config(FILENAMES["standard"])
    modified_config = Config(FILENAMES["get_files_caching"])
    assert modified_config.is_processes_get_files_caching != config.is_processes_get_files_caching


@pytest.mark.on_all_envs
def test_transfer_protocols_empty():
    config = Config(FILENAMES["transfer_protocols"]["1"])
    assert config.processes_transfer_protocols == [""]
    assert get_transfer_protocols(
        requested=config.processes_transfer_protocols,
    )["default"] == "http"
    assert len(
        list(get_transfer_protocols(
            requested=config.processes_transfer_protocols,
        ).keys()),
    ) == 3


@pytest.mark.on_all_envs
def test_transfer_protocols_gridftp():
    config = Config(FILENAMES["transfer_protocols"]["2"])
    assert config.processes_transfer_protocols == ["gridftp"]
    assert get_transfer_protocols(
        requested=config.processes_transfer_protocols,
    )["default"] == "gridftp"
    assert get_transfer_protocols(
        requested=config.processes_transfer_protocols,
    )["gridftp"] == "gridftp"
    assert len(
        list(get_transfer_protocols(
            requested=config.processes_transfer_protocols,
        ).keys()),
    ) == 3


@pytest.mark.on_all_envs
def test_transfer_protocols_gridftp4():
    config = Config(FILENAMES["transfer_protocols"]["3"])
    assert "http" in config.processes_transfer_protocols
    assert "gridftp4" in config.processes_transfer_protocols
    assert get_transfer_protocols(
        requested=config.processes_transfer_protocols,
    )["default"] == "http"
    assert get_transfer_protocols(
        requested=config.processes_transfer_protocols,
    )["http"] == "http"
    assert len(
        list(get_transfer_protocols(
            requested=config.processes_transfer_protocols,
        ).keys()),
    ) == 3


@pytest.mark.on_all_envs
def test_hack_projects_empty():
    config = Config(FILENAMES["hack_projects"]["1"])

    assert config.hack_projects_with_one_variable_per_dataset == [""]

    assert get_hack_projects(requested=config.hack_projects_with_one_variable_per_dataset) == [""]


@pytest.mark.on_all_envs
def test_hack_projects_cordex():
    config = Config(FILENAMES["hack_projects"]["2"])

    assert len(config.hack_projects_with_one_variable_per_dataset) == 1
    assert "CORDEX" in config.hack_projects_with_one_variable_per_dataset

    assert len(get_hack_projects(requested=config.hack_projects_with_one_variable_per_dataset)) == 1
    assert "CORDEX" in get_hack_projects(requested=config.hack_projects_with_one_variable_per_dataset)


@pytest.mark.on_all_envs
def test_hack_projects_cordex_cmip5_cmip6():
    config = Config(FILENAMES["hack_projects"]["3"])

    assert len(config.hack_projects_with_one_variable_per_dataset) == 3
    assert "CORDEX" in config.hack_projects_with_one_variable_per_dataset
    assert "CMIP5" in config.hack_projects_with_one_variable_per_dataset
    assert "CMIP6" in config.hack_projects_with_one_variable_per_dataset

    assert len(
        get_hack_projects(requested=config.hack_projects_with_one_variable_per_dataset),
    ) == len(config.hack_projects_with_one_variable_per_dataset)
    assert "CORDEX" in get_hack_projects(requested=config.hack_projects_with_one_variable_per_dataset)
    assert "CMIP5" in get_hack_projects(requested=config.hack_projects_with_one_variable_per_dataset)
    assert "CMIP6" in get_hack_projects(requested=config.hack_projects_with_one_variable_per_dataset)


@pytest.mark.on_all_envs
def test_subcommand_get_display_downloads_progression_every_n_seconds_default():
    config = Config(FILENAMES["standard"])
    assert config.subcommand_get_display_downloads_progression_every_n_seconds == 1.0


@pytest.mark.on_all_envs
def test_subcommand_get_display_downloads_progression_every_n_seconds_2p5():
    config = Config(FILENAMES["subcommand_get_display_downloads_progression_every_n_seconds"])
    assert config.subcommand_get_display_downloads_progression_every_n_seconds == 2.5
