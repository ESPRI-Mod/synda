# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
class Provider(object):
    """
        This class must be used for tests only
        It may validate:
           - the asynchronous mechanism used to process tha available tasks organized as batches
           - the report building
           - the verbose mode

    """
    def __init__(self):
        self.simple_example = \
            {
                '0': dict(
                    tasks=range(5),
                    counter=0,
                ),
                '1': dict(
                    tasks=range(3),
                    counter=0,
                ),
                '2': dict(
                    tasks=range(7),
                    counter=0,
                ),
            }

    def get_batch_names(self):
        return list(self.simple_example.keys())

    async def get_task(self, batch_name):
        task_name = ""
        if self.simple_example[batch_name]["counter"] <= len(self.simple_example[batch_name]["tasks"]) - 1:
            task_id = self.simple_example[batch_name]["tasks"][self.simple_example[batch_name]["counter"]]
            self.simple_example[batch_name]["counter"] += 1
            task_name = str(task_id)
        return task_name
