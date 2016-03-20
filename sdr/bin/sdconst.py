#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

#    name,           type_, default_value,               search_api_facet, option
# TODO => what is 'option' flag for ??? (i.e. is just the exact opposite of 'search_api_facet' flag, isn't it ?
DEFAULT_SESSION_PARAMS=[
    ['verbose',      bool,  True,                         False,           True],
    ['ignorecase',   bool,  False,                        False,           True],
    ['onemgf',       bool,  False,                        False,           True],
    ['last_query',   str,   '',                           False,           True],
    ['dry_run',      bool,  False,                        False,           True],
    ['debug',        bool,  False,                        False,           True],
    ['localsearch',  bool,  False,                        False,           True],
    ['replica',      bool,  False,                        False,           False],
    ['limit',        int,  '20',                          False,           False],
    ['distrib',      bool,  True,                         False,           False],
    ['latest',       bool,  None,                         False,           False],
    ['type',         str,   SD_TYPE_DEFAULT,              False,           False]
]
