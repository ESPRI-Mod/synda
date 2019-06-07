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
Clarification added 2019-05-21:
 This doesn't explicitly "remove replicates".  run() will remove all copies but the first
 encountered.  They are replicates iff the first encountered is at the "original" data node.

See also
    - sdshrink
"""
# If we ever want to prioritize data nodes, it can be done here, or in whatever builds
# the files list.

import string
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

def run_latest(metadata,functional_id_keyname):
    sdlog.info("SYNDRMDR-003","Replicate only latest datasets...")

    po=sdpipelineprocessing.ProcessingObject(remove_allbut_latest,functional_id_keyname)
    metadata=sdpipelineprocessing.run_pipeline(metadata,po)

    return metadata

def remove_allbut_latest(files,functional_id_keyname):
    """The first argument 'files' is a list of files or datasets.  The second argument is
    'file_functional_id' or 'dataset_functional_id'.  This function will remove
    any which are not latest version (within the list), and return the result, as a list.
    """
    # This gets the version by parsing file_functional_id.  Thus this is fragile.  But it works
    # for CMIP-5 and CMIP-6, and requires a minimum of changes at higher levels.
    latest = {}
    for f in files:
        version = f['dataset_version']
        if version[0]=='v':
            # 'v1234' and '1234' are treated the same. '1234' is wrong but occurs.
            version = version[1:]
        versionnum = int(version)

        # 'latest' will be indexed by a variant of functional_id with the version removed:
        functional_id = f[functional_id_keyname]
        fid_split = string.split(functional_id,'.')
        if 'filename' in f and fid_split[-3].find(version)>=0:
            # version the substring right before the filename; the find is to make sure we got it.
            fid_split[-3] = 'v000000'
        elif fid_split[-1].find(version)>=0:
            # version is the last substring; the find is to make sure of that.
            fid_split[-1] = 'v000000'
        fid_noversion = string.join(fid_split,'.')

        # In practice, if a dataset has sequential versions like v2 and date-based versions like
        # v20131002, then the date-based versions are more recent (they are more standard).
        if fid_noversion not in latest.keys() or versionnum>latest[fid_noversion][0]:
            latest[fid_noversion] = (versionnum,f)
    new_files = [lv[1] for lv in latest.values()]

    return new_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
