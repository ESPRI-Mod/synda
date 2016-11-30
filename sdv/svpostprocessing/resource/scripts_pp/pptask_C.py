#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Sample script."""

import re
import os
import argparse
import logging

def run(job):
    logging.info('sample script start')

    print job['full_path_variable']

    #job['transition_return_code']=1
    job['transition_return_code']=0

    logging.info('sample script complete')

    return job

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    run()
