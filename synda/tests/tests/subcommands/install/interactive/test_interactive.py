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

 Sub-command    : install
 Function       : is_interactive_active
 Specifications : install-01 (a, b, c & d [= c1 + c2])
"""
import pytest
from synda.sdt.sdinstall import is_interactive_active


@pytest.mark.on_all_envs
def test_specif_install_01a():
    non_interactive_from_cli = False
    interactive_from_preferences = True
    assert is_interactive_active(non_interactive_from_cli, interactive_from_preferences) is True


@pytest.mark.on_all_envs
def test_specif_install_01b():
    non_interactive_from_cli = False
    interactive_from_preferences = False
    assert is_interactive_active(non_interactive_from_cli, interactive_from_preferences) is False


@pytest.mark.on_all_envs
def test_specif_install_01c_1():
    non_interactive_from_cli = True
    interactive_from_preferences = False  # ignored
    assert is_interactive_active(non_interactive_from_cli, interactive_from_preferences) is False


@pytest.mark.on_all_envs
def test_specif_install_01c_2():
    non_interactive_from_cli = True
    interactive_from_preferences = True  # ignored
    assert is_interactive_active(non_interactive_from_cli, interactive_from_preferences) is False
