# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from synda.tests.context.env.models import Context


def activate_tests_mode():
    os.environ["ST_TESTS_MODE_STATUS"] = "activated"


class Manager(object):

    def __init__(self):

        # init
        self.env = None
        self.initial_tests_mode_status_value = ""

    def restore_initial_tests_mode_status_value_if_necessary(self):
        if self.initial_tests_mode_status_value:
            os.environ["ST_TESTS_MODE_STATUS"] = self.initial_tests_mode_status_value

    def set_tests_mode(self):

        if "ST_TESTS_MODE_STATUS" in os.environ:
            self.initial_tests_mode_status_value = os.environ["ST_TESTS_MODE_STATUS"]

        activate_tests_mode()

        # settings

        self.env = Context()

    def create_test_environment(self, source=""):
        self.env.create(source=source)

    def delete_test_environment(self):
        self.env.delete(self.env.root)
