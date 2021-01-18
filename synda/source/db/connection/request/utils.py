# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################


def add_condition(sub_conditions):
    return " AND ".join(
        ["%s=:%s" % (k, k) if sub_conditions[k] is not None else "%s IS NULL" % k for k in sub_conditions],
    )
