#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This filter improves Search-API query response time when searching for one specific model.

Notes
    - 'sdonemgf' means 'SynDa ONE Model Go Faster'
    - This module IS independant from the 'sdonemgf_post' module.
    - This module works together with the 'sdautoextractmodel' module.
    - This module contains a cache which is only used in the 'sdtc' context
    - This module performs automatically what 'lock' and 'unlock' funcs perform manually.
"""

from operator import attrgetter
import sdremoteparam
import sdindex
import sddquery
import sdtools
import sdconfig

def run(facets_groups,dry_run=False):
    for facets_group in facets_groups:

        onemgf=sdconfig.config.getboolean('behaviour','onemgf')
        if onemgf:

            models=facets_group.get('model',[])

            if len(models)==0:
                # model not specified

                pass
            elif len(models)==1:
                # one model specified

                model=models[0]

                lock(facets_group,model)
            else:
                # more than one models specified

                pass

    return facets_groups

def lock(facets_group,model):
    verbose=sddquery.get_scalar(facets_group,'verbose',default=False,type_=bool) # we cast here as verbose can be str (set from parameter) or bool (set from '-v' option)

    if model in cache:
        facets_group["searchapi_host"]=cache[model]
        facets_group["distrib"]=['false']
    else:
        params=sdremoteparam.run(pname='index_node',facets_group={'type':['Dataset'],'model':[model],'replica':['false']},dry_run=False)
        indexes=params.get('index_node',[])

        if verbose:
            sdtools.print_stderr('Master index candidates for %s model are:'%model)
            for i in indexes:
                sdtools.print_stderr('%s %i'%(i.name,i.count))

        if len(indexes)>0:
            master_index=max(indexes, key=attrgetter('count'))

            if verbose:
                sdtools.print_stderr("'searchapi_host' has been set to %s"%master_index)

            facets_group["searchapi_host"]=master_index.name
            facets_group["distrib"]=['false']

            cache[model]=master_index.name

# module init.

cache={}
