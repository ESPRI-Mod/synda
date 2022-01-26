#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains paths and configuration parameters."""

import os

from synda.sdt import sdtools
from synda.sdt.sdexception import SDException

from synda.source.config.api.esgf_search.constants import OUTPUT_FORMAT as SEARCH_API_OUTPUT_FORMAT


def check_path(path):
    if not os.path.exists(path):
        raise SDException(
            "SDCONFIG-014",
            "Path not found ({}) ".format(
                path,
            ),
        )


def print_(name):
    if name is None:
        # print all configuration parameters

        sdtools.print_module_variables(globals())
    else:
        # print given configuration parameter

        if name in globals():
            print(globals()[name])
        else:
            print('No configuration entry found by the name {}'.format(name))


# CONTROLS

# environment variables

if 'ST_HOME' not in os.environ:
    raise SDException('SDCONFIG-010', "'ST_HOME' is not set")

# tree paths for input/output storage (see data.tar.gz file)

# credential_file = Credentials().get()

# TODO investigate what's the reason for this?
# user_paths=sdconfigutils.UserPaths(os.path.expanduser("~/.sdt"))

# check_path(bin_folder)

# this is to prevent flooding log file with domain message during debugging session
# (i.e. set it to false when debugging).
log_domain_inconsistency = True

# If true, domain inconsistencies are printed on stderr
print_domain_inconsistency = True

# choices : dataset_id | query
dataset_filter_mecanism_in_file_context = 'dataset_id'

max_metadata_parallel_download_per_index = 3

metadata_parallel_download = False


# note that variable below only set which low_level mecanism to use to find the nearest
# (i.e. it's not an on/off flag (the on/off flag is the 'nearest' selection file parameter))

# choices : pre | post
nearest_schedule = 'post'

# choices : error | warning
unknown_value_behaviour = 'error'

mono_host_retry = False
WAITING_TIME_IN_CASE_OF_RETRY = 1.0

proxymt_progress_stat = False

lowmem = True
fix_encoding = False

# Beware before enabling this: must be well tested/reviewed as it seems to currently introduce regression.
twophasesearch = False

# If true, stop download if error occurs during download
# if false, the download continue. Note that in the case of a certificate renewal error,
# the daemon always stops not matter if this false is true or false.
stop_download_if_error_occurs = False

searchapi_output_format = SEARCH_API_OUTPUT_FORMAT

# when true, allow fast cycle for test (used for UAT)
fake_download = False

copy_ds_attrs = False
