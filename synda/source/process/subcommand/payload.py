# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
class Payload(object):
    """
    Contains useful data required by all subcommands to work
    """

    def __init__(self, authority, config):

        # initializations
        self.authority = None
        self.config = None

        # settings
        self.authority = authority
        self.config = config

    def get_authority(self):
        return self.authority

    def get_config(self):
        return self.config
