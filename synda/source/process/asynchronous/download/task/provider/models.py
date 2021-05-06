# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.sdt import sddao
from synda.sdt import sdfiledao
# from synda.sdt.sdlog import default_logger_file_name


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


async def get_file_instance(data_node):
    file_instance = sddao.get_one_waiting_transfer_new(datanode=data_node)
    if file_instance:
        sdfiledao.update_file_as_running(file_instance)
    return file_instance


class Provider(object):
    def __init__(self):
        self.batches = []

        self.batches = get_batches()

    def get_batch_names(self):
        batch_names = []
        for batch in self.batches:
            batch_names.append(list(batch.keys())[0])
        return batch_names

    @staticmethod
    async def get_task(batch_name):
        return await get_file_instance(batch_name)
