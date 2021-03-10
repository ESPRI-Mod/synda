#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script changes existing transfer attributes.

Notes
    - This filter terminates a pipeline
    - This module is intended to be plugged to sdfilepipeline output
      (i.e. stream must be duplicate free and each file must contain status attribute).
"""
from synda.sdt import sdmodifyquery
from synda.sdt import sdreplica
from synda.sdt import sdlog
from synda.sdt.sdtools import print_stderr

from synda.source.config.process.download.constants import TRANSFER


def pause_all():
    sdlog.info("SDMODIFY-431", "Moving transfer from waiting to pause..")
    nbr = sdmodifyquery.change_status(TRANSFER["status"]['waiting'], TRANSFER["status"]['pause'])
    sdlog.info("SDMODIFY-830", "%i transfer marked for retry" % nbr)


def retry_all(query_filter=None):

    sdlog.info(
        "SDMODIFY-343",
        "Moving transfer from error to waiting..",
    )
    nbr = sdmodifyquery.change_status(
        TRANSFER["status"]['error'],
        TRANSFER["status"]['waiting'],
        where=query_filter,
    )
    sdlog.info(
        "SDMODIFY-226",
        "%i transfer marked for retry" % nbr,
    )
    return nbr


def replica_next(file_, replicas):
    # replica can only be changed for those file statuses
    if file_.status in [TRANSFER["status"]['error'], TRANSFER["status"]['waiting']]:

        # TODO: maybe use replica object instead of tuple here
        new_replica = sdreplica.replica_next(file_.url, replicas)
        if new_replica is None:
            print_stderr("No other replica found (file_functional_id=%s)" % file_.file_functional_id)
        else:
            sdmodifyquery.change_replica(file_.file_functional_id, new_replica)

            sdlog.info(
                "SDMODIFY-100",
                "File replica set to {} (previous_replica={},file_functional_id={})".format(
                    new_replica[1],
                    file_.url,
                    file_.file_functional_id,
                ),
            )
    else:
        print_stderr("Replica cannot be changed (local file incorrect status).")
