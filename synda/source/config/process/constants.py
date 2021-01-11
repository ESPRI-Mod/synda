# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# as list maybe duplicated in memory at some point in the pipeline, we use a lower value here than SEARCH_API_CHUNKSIZE
CHUNKSIZE = 5000

FETCH_MODE_GENERATOR = 'generator'

ADMIN_SUBCOMMANDS = ['autoremove', 'install', 'open', 'pexec', 'remove', 'reset', 'retry', 'update', 'upgrade']
