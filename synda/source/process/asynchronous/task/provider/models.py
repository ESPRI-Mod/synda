# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
class Default(object):
    """
        This class must be used for tests only
        It may validate:
           - the asynchronous mechanism used to process tha available tasks organized as batches
           - the report building
           - the verbose mode

    """

    def __init__(self):
        self.example = {
            '0': dict(
                tasks=list(range(1)),
                counter=0,
            )
        }
        self.counter = 0

    def simulate_event(self):
        return self.counter == 1

    def do_action(self):
        pass

    def get_db_batch_names(self):
        return list(self.example.keys())

    async def get_task(self, batch_name):
        task_name = ""

        if self.example[batch_name]["counter"] <= len(self.example[batch_name]["tasks"]) - 1:
            task_id = self.example[batch_name]["tasks"][self.example[batch_name]["counter"]]
            self.example[batch_name]["counter"] += 1
            task_name = str(task_id)
        self.counter += 1

        if self.simulate_event():
            self.do_action()

        db_batch_names = self.get_db_batch_names()

        return task_name, db_batch_names


class CreateBatch(Default):
    """
        This class must be used for tests only
        It may validate:
           - the asynchronous mechanism used to process tha available tasks organized as batches
           - the report building
           - the verbose mode

    """

    def __init__(self):
        Default.__init__(self)
        nb_tasks_0 = 5
        nb_tasks_1 = 3
        nb_tasks_2 = 7
        # nb_tasks_0 = 1
        # nb_tasks_1 = 1
        # nb_tasks_2 = 1
        self.example = \
            {
                '0': dict(
                    tasks=list(range(nb_tasks_0)),
                    counter=0,
                ),
                '1': dict(
                    tasks=list(range(nb_tasks_1)),
                    counter=0,
                ),
                '2': dict(
                    tasks=list(range(nb_tasks_2)),
                    counter=0,
                ),
            }

    def simulate_event(self):
        return self.counter == 3

    def do_action(self):
        batch = {
            '3': dict(
                tasks=range(1),
                counter=0,
            ),
        }
        self.example.update(
            batch,
        )

    async def get_task(self, batch_name):
        task_name = ""

        if self.example[batch_name]["counter"] <= len(self.example[batch_name]["tasks"]) - 1:
            task_id = self.example[batch_name]["tasks"][self.example[batch_name]["counter"]]
            self.example[batch_name]["counter"] += 1
            task_name = str(task_id)
        self.counter += 1

        if self.simulate_event():
            self.do_action()

        db_batch_names = self.get_db_batch_names()

        return task_name, db_batch_names


class BatchUpdatedTooLate(Default):
    """
        This class must be used for tests only
        It may validate:
           - the asynchronous mechanism used to process tha available tasks organized as batches
           - the report building
           - the verbose mode

    """
    def __init__(self):
        Default.__init__(self)
        nb_tasks = 1

        self.example = \
            {
                '0': dict(
                    tasks=list(range(nb_tasks)),
                    counter=0,
                ),
            }

    def simulate_event(self):
        return self.counter == 3

    def do_action(self):
        self.example["0"]["tasks"].extend(
            [1],
        )

    async def get_task(self, batch_name):
        task_name = ""

        if self.example[batch_name]["counter"] <= len(self.example[batch_name]["tasks"]) - 1:
            task_id = self.example[batch_name]["tasks"][self.example[batch_name]["counter"]]
            self.example[batch_name]["counter"] += 1
            task_name = str(task_id)
        self.counter += 1

        if self.simulate_event():
            self.do_action()

        db_batch_names = self.get_db_batch_names()

        return task_name, db_batch_names


class BatchUpdatedDuringDownloadingProcess(Default):
    """
        This class must be used for tests only
        It may validate:
           - the asynchronous mechanism used to process tha available tasks organized as batches
           - the report building
           - the verbose mode

    """
    def __init__(self):
        Default.__init__(self)
        nb_tasks = 2

        self.example = \
            {
                '0': dict(
                    tasks=list(range(nb_tasks)),
                    counter=0,
                ),
            }

    def simulate_event(self):
        return self.counter == 1

    def do_action(self):
        self.example["0"]["tasks"].extend(
            list(range(1)),
        )

    async def get_task(self, batch_name):
        task_name = ""

        if self.example[batch_name]["counter"] <= len(self.example[batch_name]["tasks"]) - 1:
            task_id = self.example[batch_name]["tasks"][self.example[batch_name]["counter"]]
            self.example[batch_name]["counter"] += 1
            task_name = str(task_id)
        self.counter += 1

        if self.simulate_event():
            self.do_action()

        db_batch_names = self.get_db_batch_names()

        return task_name, db_batch_names


class Provider(BatchUpdatedDuringDownloadingProcess):
    """

    """
    def __init__(self):
        BatchUpdatedDuringDownloadingProcess.__init__(self)
