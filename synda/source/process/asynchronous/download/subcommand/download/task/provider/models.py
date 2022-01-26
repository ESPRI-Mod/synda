# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import psutil
import asyncio
import uvloop

from synda.sdt import sddao
from synda.sdt import sdfiledao

uvloop.install()

SLEEP_DURATION = 0.1
TIMEOUT = 60


def get_data_nodes():
    data_nodes = []
    validated, unvalidated = sddao.check_waiting_files_for_download()
    sdfiledao.update_files(unvalidated)
    if unvalidated:
        print(
            '{} downloads aborted (out of a total of {}), you can check the logs for further information.'.format(
                len(unvalidated),
                len(unvalidated) + len(validated),
            ),
        )

    if validated:
        data_nodes = [list(record.keys())[0] for record in validated]

    return data_nodes


async def confirm_is_running(file_instance):

    file_functional_id = file_instance.file_functional_id
    waiting = 0
    while not sdfiledao.file_status_is_running(file_functional_id) and waiting < TIMEOUT:
        await asyncio.sleep(SLEEP_DURATION)
        waiting += SLEEP_DURATION

    return sdfiledao.file_status_is_running(file_functional_id)


async def get_file_instance(data_node):
    # print(psutil.virtual_memory())
    # print(psutil.swap_memory())
    file_instance = sddao.get_one_waiting_instance(datanode=data_node, ascending=False)
    if file_instance:
        sdfiledao.update_file_as_running(file_instance)
        # is_running = await confirm_is_running(file_instance)
        # print("File id  : {} is confirmed has running".format(file_instance.file_id))
    return file_instance


class Provider(object):

    def get_db_batch_names(self):
        return get_data_nodes()

    async def get_task(self, batch_name):
        task = await get_file_instance(batch_name)
        return task, self.get_db_batch_names()
