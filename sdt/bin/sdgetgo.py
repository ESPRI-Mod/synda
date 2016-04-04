#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains Globus Transfer file transfer functions."""

import os
import sys
import json
import argparse
import sdapp
import sdutils

def download_file(url,local_path,checksum_type):
    status=file_transfer_synchronous_wrapper(url,local_path)

    if status==0:
        local_checksum=sdutils.compute_checksum(local_path,checksum_type)
    else:
        local_checksum=None

    return (status,local_checksum)

def file_transfer_synchronous_wrapper(source_file,dest_file):
    """Synchronous wrapper for Globus Transfer file transfer function."""

    try:
        code, reason, result = api.transfer_submission_id()
        submission_id = result["value"]

        t = Transfer(submission_id, "go#ep1", "go#ep2")
        t.add_item(source_file, dest_file)

        status, reason, result = api.transfer(t)
        task_id = result["task_id"]

        while get_status() in ['waiting','running']:
            time.sleep(50)

        if get_status() == 'done':
            return 0
        else:
            return 1

    except Exception, e:
        return 1

def get_status():
    status, reason, result = api.task(task_id)
    return result["status"]

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    sys.exit(0)
