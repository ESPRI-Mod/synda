#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module check if files appear in both output1 and output2."""

import os, argparse, logging

def intersect(a, b):
     return list(set(a) & set(b))

def get_output12_dataset_paths(path):
    """Return tuple with output1 based dataset path and output2 based dataset path."""

    assert "/*/" in path

    o1=path.replace("/*/","/output1/")
    o2=path.replace("/*/","/output2/")

    tu=(o1,o2)

    return tu

def is_duplicate(output1_path,output2_path):
    if os.path.exists(output1_path) and os.path.exists(output2_path):
        output1_files = os.listdir(output1_path)
        output2_files = os.listdir(output2_path)

        interset_files=intersect(output1_files,output2_files)

        if len(interset_files)>0:
            return True
        else:
            return False
    else:
        return False

def run(job):
    logging.info('is_duplicate.py start')

    (path_output1,path_output2)=get_output12_dataset_paths(job['full_path_variable'])
    if is_duplicate(path_output1,path_output2):
        job['transition_return_code']=1
    else:
        job['transition_return_code']=0

    logging.info('is_duplicate.py complete')
    return job

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
