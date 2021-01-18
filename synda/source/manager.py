# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
from synda.source.containers import Container


class Manager(Container):

    def __init__(self, identifier=""):
        super(Manager, self).__init__(identifier=identifier)
        self.data_identifiers = []

    def get_data_identifiers(self):
        return self.data_identifiers

    def add(self, item):
        self.data.append(item)
        self.data_identifiers.append(item.get_identifier())
        return self.get_last_item()

    def set_data(self, data):
        for item in data:
            self.add(item)

    def get_item(self, identifier):
        try:
            index = self.data_identifiers.index(identifier)
            item = self.data[index]

        except ValueError:
            item = None

        return item


if __name__ == '__main__':
    pass
