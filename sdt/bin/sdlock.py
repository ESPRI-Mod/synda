#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains routines used to focus on one index (by turning off 'distrib' flag)."""

import sdsessionparam
import sdremoteparam
from operator import attrgetter

def lock(model):
    dry_run=sdsessionparam.get_value('dry_run')
    params=sdremoteparam.run(pname='index_node',facets_group={'type':['Dataset'],'model':[model],'replica':['false']},dry_run=dry_run)
    indexes=params.get('index_node',[])

    if not dry_run:
        if len(indexes)>0:
            master_index=max(indexes, key=attrgetter('count'))

            sdsessionparam.set("searchapi_host",master_index.name)
            sdsessionparam.set("distrib","false")
            sdsessionparam.set("model",model)
        else:
            raise SDException('SDATLOCK-001','Model not found')

def unlock(model):
    sdsessionparam.remove_session_param('searchapi_host')
    sdsessionparam.remove_session_param('model')
    sdsessionparam.set("distrib","true")
