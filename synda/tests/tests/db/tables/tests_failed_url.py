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

 object : Table "failed_url"

"""
import pytest
from synda.tests.manager import Manager

manager = Manager()
manager.set_tests_mode()

from synda.source.db.connection.request.table.dao.delete.manager import Manager as DeleteTableManager
from synda.source.db.task.failed_url.update.models import insert_into_failed_url
from synda.source.db.task.failed_url.read.models import get_all_rows


@pytest.mark.on_all_envs
def test_insert():
    manager.create_test_environment()
    url = "http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/psl/1/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc"
    file_functional_id = "cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v1.psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc"
    lastrowid, msg = insert_into_failed_url(url, file_functional_id)

    assert msg == ""

    all_data = get_all_rows()

    assert lastrowid == all_data[0]["url_id"]
    assert url == all_data[0]["url"]
    assert file_functional_id == all_data[0]["file_id"]

    create_manager = DeleteTableManager()
