# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import asyncio


class Provider(object):

    def __init__(self, file_instances):
        self.file_instances = []
        self.file_instances = file_instances
        self.get_data_nodes()

    async def get_file_instance(self, data_node):
        await asyncio.sleep(0.0)
        if len(self.file_instances) > 0:
            file_instance = self.file_instances.pop()
        else:
            file_instance = None
        return file_instance

    def get_nb_tasks(self):
        return len(self.file_instances)

    def get_data_node(self, file_instance):
        basename = file_instance.url.split("http://")
        if len(basename) < 2:
            basename = file_instance.url.split("https://")
        try:
            data_node = basename[1].split("/")[0]
        except:
            data_node = ""
        # save the result
        file_instance.data_node = data_node
        return data_node

    def get_data_nodes(self):
        data_nodes = []
        for file_instance in self.file_instances:
            data_node = self.get_data_node(file_instance)
            data_nodes.append(data_node)
        return list(set(data_nodes))

    def get_db_batch_names(self):
        return self.get_data_nodes()

    async def get_task(self, batch_name=""):
        task = await self.get_file_instance(batch_name)
        return task, self.get_db_batch_names()
