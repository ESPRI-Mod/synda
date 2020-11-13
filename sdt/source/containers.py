# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################


class Container(object):

    def __init__(self,):
        self.data = []

    def get_data(self):
        return self.data

    def add(self, item):
        self.data.append(item)
        return self.get_last_item()

    def set_data(self, data):
        self.data = data

    def get_last_item(self):
        return self.data[-1]
