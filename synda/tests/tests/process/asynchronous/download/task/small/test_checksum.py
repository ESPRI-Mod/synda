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

 object :
"""
import pytest
from synda.sdt.sdtypes import File
from synda.tests.manager import Manager

from synda.source.process.asynchronous.download.task.subcommand.download import FILE_CORRUPTION_CHECKSUM_ERROR_MSG
from synda.source.process.asynchronous.download.worker.aiohttp.task import Task
from synda.source.config.process.download.constants import TRANSFER

manager = Manager()
manager.set_tests_mode()

url = 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/mrsos/1/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'
file_functional_id = 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.land.Lmon.r1i1p1.v1.mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'
filename = 'mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'
local_path = 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'

size = 27452324

good_checksum = '79e92073e7f0e31a968744ef4c0cbeb80104a07bb9ba82862bab2ee50212bd8a'
bad_checksum = ''


@pytest.mark.asyncio
async def test_checksum_ok():
    manager.create_test_environment()

    file_instance = File(
        **{
            'file_id': 17,
            'url': url,
            'file_functional_id': file_functional_id,
            'filename': filename,
            'local_path': local_path,
            'data_node': 'aims3.llnl.gov',
            'checksum': good_checksum,
            'checksum_type': 'sha256', 'duration': 166.78693, 'size': size, 'rate': 164595.17541332525,
            'start_date': '2021-04-13 11:39:50.041778', 'end_date': '2021-04-13 11:42:36.828708',
            'crea_date': '2021-04-07 09:59:06.855726', 'status': 'running', 'error_msg': None, 'sdget_status': 0,
            'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'fd29adc5-0005-4365-a4a8-e59085bb3976',
            'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'mrsos', 'last_access_date': None,
            'dataset_id': 7,
            'insertion_group_id': 1, 'timestamp': '2012-03-07T10:13:15Z', 'dataset': None,
         }

    )

    new_task = Task(file_instance, "test", manager=None)
    new_task.create_local_path()

    await new_task.download()

    validated = new_task.post_process_control.validate_checksum()

    assert validated
    assert new_task.get_file_instance().status == TRANSFER["status"]['done']
    assert new_task.get_file_instance().error_msg == ""


@pytest.mark.asyncio
async def test_checksum_ko_keep():
    manager.create_test_environment()

    file_instance = File(
        **{

            'file_id': 17,
            'url': url,
            'file_functional_id': file_functional_id,
            'filename': filename,
            'local_path': local_path,
            'data_node': 'aims3.llnl.gov',
            'checksum': bad_checksum,
            'checksum_type': 'sha256', 'duration': 166.78693, 'size': size, 'rate': 164595.17541332525,
            'start_date': '2021-04-13 11:39:50.041778', 'end_date': '2021-04-13 11:42:36.828708',
            'crea_date': '2021-04-07 09:59:06.855726', 'status': 'running', 'error_msg': None, 'sdget_status': 0,
            'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'fd29adc5-0005-4365-a4a8-e59085bb3976',
            'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'mrsos', 'last_access_date': None,
            'dataset_id': 7,
            'insertion_group_id': 1, 'timestamp': '2012-03-07T10:13:15Z', 'dataset': None,
         }

    )

    new_task = Task(file_instance, "test", manager=None)
    new_task.create_local_path()

    await new_task.download()

    validated = new_task.post_process_control.validate_checksum("keep")

    assert not validated
    assert new_task.get_file_instance().status == TRANSFER["status"]['done']
    assert new_task.get_file_instance().error_msg == ""


@pytest.mark.asyncio
async def test_checksum_ko_remove():
    manager.create_test_environment()

    file_instance = File(
        **{
            'file_id': 17,
            'url': url,
            'file_functional_id': file_functional_id,
            'filename': filename,
            'local_path': local_path,
            'data_node': 'aims3.llnl.gov',
            'checksum': bad_checksum,
            'checksum_type': 'sha256', 'duration': 166.78693, 'size': size, 'rate': 164595.17541332525,
            'start_date': '2021-04-13 11:39:50.041778', 'end_date': '2021-04-13 11:42:36.828708',
            'crea_date': '2021-04-07 09:59:06.855726', 'status': 'running', 'error_msg': None, 'sdget_status': 0,
            'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'fd29adc5-0005-4365-a4a8-e59085bb3976',
            'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'mrsos', 'last_access_date': None,
            'dataset_id': 7,
            'insertion_group_id': 1, 'timestamp': '2012-03-07T10:13:15Z', 'dataset': None,
         }

    )

    new_task = Task(file_instance, "test", manager=None)
    new_task.create_local_path()

    await new_task.download()

    validated = new_task.post_process_control.validate_checksum(
        incorrect_checksum_action="remove",
    )

    assert not validated
    assert new_task.get_file_instance().status == TRANSFER["status"]['error']
    assert new_task.get_file_instance().priority == 999
    assert new_task.get_file_instance().error_msg == FILE_CORRUPTION_CHECKSUM_ERROR_MSG
