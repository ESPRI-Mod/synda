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
from synda.sdt import sddao
from synda.sdt import sdfiledao
# from synda.sdt.sdlog import default_logger_file_name

SLEEP_DURATION = 0.1
TIMEOUT = 60


def get_batches():
    validated, unvalidated = sddao.check_waiting_files_for_download()
    sdfiledao.update_files(unvalidated)
    if unvalidated:
        print(
            '{} downloads aborted (out of a total of {}), you can check the logs for further information.'.format(
                len(unvalidated),
                len(unvalidated) + len(validated),
            ),
        )
        # print(
        #     '{} downloads aborted (out of a total of {}), you can check the logs at {} for further information.'.format(
        #         len(unvalidated),
        #         len(unvalidated) + len(validated),
        #         default_logger_file_name,
        #     ),
        # )

    if not validated:
        print(
            '=> Nothing done',
        )

    return validated


async def confirm_is_running(file_instance):

    file_functional_id = file_instance.file_functional_id
    waiting = 0
    while not sdfiledao.file_status_is_running(file_functional_id) and waiting < TIMEOUT:
        await asyncio.sleep(SLEEP_DURATION)
        waiting += SLEEP_DURATION

    return sdfiledao.file_status_is_running(file_functional_id)


async def get_file_instances(data_node, ascending=True):
    # print(psutil.virtual_memory())
    # print(psutil.swap_memory())
    # if file_instance:
    #     sdfiledao.update_file_as_running(file_instance)
        # is_running = await confirm_is_running(file_instance)
        # print("File id  : {} is confirmed has running".format(file_instance.file_id))
    return sddao.get_new_tasks(datanode=data_node, ascending=ascending)


class Provider(object):
    def __init__(self):
        self.file_instances = []
        self.batches = []
        self.batches = get_batches()

    def get_batch_names(self):
        batch_names = []
        for batch in self.batches:
            batch_names.append(list(batch.keys())[0])
        return batch_names

    async def get_task(self, batch_name, ascending):
        if not self.file_instances:
            self.file_instances = await get_file_instances(batch_name, ascending=ascending)

        if self.file_instances:
            index = 0
            file_instance = self.file_instances.pop(index)
            if file_instance:
                sdfiledao.update_file_as_running(file_instance)
        else:
            file_instance = None

        return file_instance
