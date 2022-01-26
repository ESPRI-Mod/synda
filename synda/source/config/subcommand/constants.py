# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.sdt.sdtools import print_stderr

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.version import CURRENT as CURRENT_SYNDA_VERSION

deprecated_msg_template = "DeprecationError: The 'synda {}' subcommand has been removed in Synda " + \
                          CURRENT_SYNDA_VERSION + "."

DEPRECATED_STRUCT = dict(
    daemon="Use 'synda download [start|stop|status|queue|watch]' instead.",
    queue="Use 'synda download queue' instead.",
    watch="Use 'synda download watch' instead."
)

DEPRECATED_NAMES = [
    "daemon",
    "queue",
    "watch",
]

NAMES = {
    'autoremove',
    'certificate',
    'check',
    'check-env',
    'init-env',
    'config',
    'contact',
    'count',
    'download',
    'dump',
    'facet',
    'get',
    'getinfo',
    "help",
    'history',
    'install',
    'intro',
    'list',
    'metric',
    'param',
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
    'synda_version',
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


def deprecated(subcommand):
    print_stderr(
        msg="{} {}".format(
            deprecated_msg_template.format(subcommand),
            DEPRECATED_STRUCT[subcommand],
        )
    )
    exit(0)
