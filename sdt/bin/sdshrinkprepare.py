#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains shrink preprocessing routines."""

class ShrinkPrepareDataStructure():
    def __init__(self):
        self.light_files=[]
    def run():

class ShrinkComputeFlag():

    def __init__(self):
        keep_replica=sdpostpipelineutils.get_attached_parameter__global(files,'keep_replica')
        self.nearestpost_enabled=True

    def run(self,files):

            
    def is_nearestpost_enabled(files):
        if self.nearestpost_enabled==False:
    
            # already set to false in a previous chunk
            return
        else:
            if sdconfig.nearest_schedule=='post':
                if nearest_flag_set_on_all_files(files):
                    self.nearestpost_enabled=True
                else:
                    self.nearestpost_enabled=False
            else:
                self.nearestpost_enabled=False

    def nearest_flag_set_on_all_files(files):
        """This func checks that all files have the 'nearest' flag (as
        sdnearestpost processing type is 'interfile', we need ALL files to
        be flagged).
        """

        for f in files:
            nearest=sdpostpipelineutils.get_attached_parameter(f,'nearest','false')
            if nearest=='false':
                return False
        return True
