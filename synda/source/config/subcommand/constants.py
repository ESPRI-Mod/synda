# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.user.preferences.models import Config as Preferences


NAMES = {
    'autoremove',
    'certificate',
    'check',
    'check-env',
    'init-env',
    'config',
    'contact',
    'count',
    'daemon',
    'dump',
    'facet',
    'get',
    "help",
    'history',
    'install',
    'intro',
    'list',
    'metric',
    'open',
    'param',
    'queue',
    'remove',
    'replica',
    'reset',
    'retry',
    'search',
    'selection',
    'show',
    'stat',
    'update',
    'upgrade',
    'variable',
    'version',
    'watch',
}

DEFAULT_LIMITS = {
    'small': {
        'search': Preferences().interface_search_listing_limit_for_small_mode,
        'dump': Preferences().interface_dump_listing_limit_for_small_mode,
        'list': Preferences().interface_list_listing_limit_for_small_mode,
    },

    'medium': {
        'search': Preferences().interface_search_listing_limit_for_medium_mode,
        'dump': Preferences().interface_dump_listing_limit_for_medium_mode,
        'list': Preferences().interface_list_listing_limit_for_medium_mode,
    },

    'big': {
        'search': Preferences().interface_search_listing_limit_for_big_mode,
        'dump': Preferences().interface_dump_listing_limit_for_big_mode,
        'list': Preferences().interface_list_listing_limit_for_big_mode,
    },
}


def get_default_limit(default_limits_mode, command):
    return DEFAULT_LIMITS[default_limits_mode][command]
