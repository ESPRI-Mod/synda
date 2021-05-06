# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
class Event(object):

    def __init__(self, dashboard):
        self.dashboard = None
        self.dashboard = dashboard

    def new_task_status(self, task):
        self.dashboard.update_metrics()
