# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import threading


class Execute(threading.Thread):
    def __init__(self, sub_command):
        threading.Thread.__init__(self)
        self.sub_command = sub_command

    def run(self):
        self.sub_command.execute()
