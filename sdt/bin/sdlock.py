#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdlock.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
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
