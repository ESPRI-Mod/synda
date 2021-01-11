# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.process.subcommand.required.env.models import Process as Base
from synda.source.process.authority.models import Authority


from synda.source.config.api.esgf_search.constants import TYPE_DATASET as API_TYPE_DATASET


class Process(Base):

    def __init__(self, arguments=None):
        super(Process, self).__init__(name="count", authority=Authority(), arguments=arguments, exceptions_codes=[0, 1])


if __name__ == '__main__':

    w_arguments = dict(
        positional=["CMIP5"],
        optional=[
            "--{}".format(
                API_TYPE_DATASET.lower(),
            ),
        ],
    )

    p = Process(w_arguments)
