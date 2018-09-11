#!/usr/share/python/synda/sdt/bin/python
#jfp was
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module removes file duplicates and replica.

Notes
    - This module removes duplicate files in a random way (i.e. all files have the same chance to be removed).
    - This module removes replicates
    - sdrmdup means 'SynDa ReMove DUPlicate and REPlicate'

See also
    - sdshrink
"""

import sdapp
import sdconst
import sdprint
import sdpostpipelineutils
import sdlmattrfilter
import sdpipelineprocessing
import sdlog
import pdb

def run(metadata,functional_id_keyname):

    sdlog.info("SYNDRMDR-001","Build 'seen' table..")

    light_metadata=sdlmattrfilter.run(metadata,[functional_id_keyname]) # create light list with needed columns only not to overload system memory

    # build 'seen' data structure (list of dict => dict (id=>bool))
    seen=dict((f[functional_id_keyname], False) for f in light_metadata.get_files()) # warning: load list in memory


    sdlog.info("SYNDRMDR-002","Perform duplicate and replicate suppression..")

    po=sdpipelineprocessing.ProcessingObject(remove,functional_id_keyname,seen)
    metadata=sdpipelineprocessing.run_pipeline(metadata,po)

    return metadata

def remove(files,functional_id_keyname,seen):
    new_files=[]
    for f in files:
        uniq_id=f[functional_id_keyname]
        if not seen[uniq_id]:
            new_files.append(f)
            seen[uniq_id]=True # mark as seen so other duplicate will be excluded (first item in the loop win)
    return new_files

def latest_dataset(metadata):
    # create light list with needed columns only not to overload system memory:
    light_metadata=sdlmattrfilter.run(metadata,['dataset_path_without_version','dataset_version'])

    sdlog.info("SYNDRMDR-003","Replicate only latest datasets...")

    po=sdpipelineprocessing.ProcessingObject(remove_allbut_latest)
    metadata=sdpipelineprocessing.run_pipeline(metadata,po)

    return metadata

def remove_allbut_latest(datasets):
    """The first argument 'datasets' is a list of datasets.  This function will remove
    any which are not latest version (within the list), and return the result, as a list.
    """
    latest = {}
    for f in datasets:
        dataset_path=f['dataset_path_without_version']   # dataset_path_without_version
        version = f['dataset_version']
        if version[0]=='v':
            # 'v1234' and '1234' are treated the same. '1234' is wrong but occurs.
            version = version[1:]
        version = int(version)
        # In practice, if a dataset has sequential versions like v2 and date-based versions like
        # v20131002, then the date-based versions are more recent (they are more standard).
        if dataset_path not in latest.keys() or version>latest[dataset_path][0]:
            latest[dataset_path] = (version,f)
    new_datasets = [lv[1] for lv in latest.values()]

    return new_datasets


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
