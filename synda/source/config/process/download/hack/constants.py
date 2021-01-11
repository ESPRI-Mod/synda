# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.internal.models import Config as Internal

ALLOWED_VALUES = ["CORDEX", "CMIP6"]


def remove_not_allowed(choices, allowed):
    for choice in choices:
        if choice not in allowed:
            choices.remove(choice)


def validate_projects(choices):

    # remove not allowed requested choices

    # remove_not_allowed(choices, ALLOWED_VALUES)

    projects = choices

    return projects


def get_projects(requested=Internal().hack_projects_with_one_variable_per_dataset):

    return validate_projects(requested)
