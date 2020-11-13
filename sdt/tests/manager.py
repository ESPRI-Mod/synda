# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.tests.context.external_storage.models import Context


class Manager(object):

    def __init__(self):
        self.context = Context()

    def set_tests_mode(self):
        self.context.set_tests_mode()

    def create_test_environment(self):
        self.context.create_tree()

    def delete_test_environment(self):
        self.context.delete_tree()
