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

"""ESGF files discovery

This script parse selection file, apply some filters, build search-api
queries, execute queries, apply some filters and print the result.

Notes
 - process only one selection file (aka template) at a time
"""

import os
import argparse
import json
import sdapp
import sdlog
import sdconfig
import sdpipeline
import sdrun
import sdi18n
import sdcliex
import sdprint
import sdconst
import sdtools
import sdsqueries
import sdbatchtimestamp
import sdadddsattr
import sdtypes
import sdcommonarg
from sdexception import SDException,MissingDatasetTimestampUrlException
from sdprogress import ProgressThread
from sdquicksearch import separate_negatives_str

import pdb

def run(stream=None,
        selection=None,
        path=None,
        parameter=None,
        post_pipeline_mode='file',
        parallel=sdconfig.metadata_parallel_download,
        index_host=None,
        dry_run=False,
        load_default=None,
        playback=None,
        record=None):
    """
    Note
        squeries means 'Serialized queries'
    """

    if parameter is None:
        parameter=[]
        parameterclean=[]
        if stream is not None:
            # Normally "synda install..." gets you here
            streamclean, negspecs = separate_negatives_str( stream )
    else:
        # Normally you get here from running sdsearch standalone
        streamclean = stream
        parameterclean, negspecs = separate_negatives_par( parameter )

    squeries=sdpipeline.build_queries(
        stream=streamclean, path=path, parameter=parameterclean, selection=selection,
        parallel=parallel, index_host=index_host, dry_run=dry_run, load_default=load_default )

    action=sdsqueries.get_scalar(squeries,'action',None)
    progress=sdsqueries.get_scalar(squeries,'progress',False,type_=bool)
    # ... we cast here as progress can be str (set from parameter) or bool (set programmaticaly)

    # Prevent use of 'limit' keyword ('limit' keyword can't be used in this module because it interfere with the pagination system)
    for q in squeries:
        if sdtools.url_contains_limit_keyword(q['url']):
            raise SDException('SDSEARCH-001',"'limit' facet is not supported in this mode. Use 'sdquicksearch' module instead.")

    if dry_run:
        sdsqueries.print_(squeries)
        return sdtypes.Metadata()
    else:
        if progress:
            #sdtools.print_stderr(sdi18n.m0003(ap.get('searchapi_host'))) # waiting message
            ProgressThread.start(sleep=0.1,running_message='',end_message='Search completed.') # spinner start

        metadata=_get_files(squeries,parallel,post_pipeline_mode,action,playback,record,negspecs)

        if progress:
            ProgressThread.stop() # spinner stop

        return metadata

def separate_negatives_par( parameter ):
    """Checks parameter (a list of strings based on a selection file) for negative specifications,
    e.g.  'institution_id=-NOAA-GFDL'.  Returns a stream in which such negatives have
    been deleted, and dict of lists of those negative specifications.  Presently, this is only
    implemented for 'institution_id=...'."""
    parameterclean = []
    poss = []
    negs = {'institution_id': []}
    if parameter is not None:
        for str in parameter:
            key = str.split('=')[0]
            if key!='institution_id':
                parameterclean += [str]
                continue
            insts = str.split('=')[1].split(',')
            new_insts = [ inst for inst in insts if inst[0]!='-' ]
            poss += new_insts
            negs['institution_id'] += [inst[1:] for inst in insts if inst[0]=='-' ]
        if len(poss)>0:
            parameterclean += ['='.join(['institution_id',','.join(poss)])]
        negs['institution_id'] = list(set(negs['institution_id']))
    return parameterclean, negs

def remove_negatives( metadata, negspecs ):
    """Removes items in result which match negspecs.  result is output of a search by an
    ESGF index node invoked in ws_call().
    example of negspecs:  {'institution_id': ['NOAA-GFDL']}
    """
    metadata.delete_some( 'institution_id', negspecs['institution_id'] )
    return metadata

def execute_queries(squeries,parallel,post_pipeline_mode,action,negspecs):
    """This func serializes received metadata on-disk to prevent memory overload."""

    sdlog.info("SDSEARCH-580","Retrieve metadata from remote service")
    metadata=sdrun.run(squeries,parallel)
    sdlog.info("SDSEARCH-584","Metadata successfully retrieved (%d files)"%metadata.count())
    metadata = remove_negatives( metadata, negspecs )

    sdlog.info("SDSEARCH-590","Metadata processing begin")
    metadata=sdpipeline.post_pipeline(metadata,post_pipeline_mode)
    sdlog.info("SDSEARCH-594","Metadata processing end")



    # moving code below inside sdfilepipeline module is not straightforward,
    # because all datasets are retrieved in one row, so we don't want it
    # to happen for each chunk (i.e. lowmem mecanism).
    # so better keep it here for now.
    # if this is also needed for, e.g. "synda dump" operation,
    # just duplicate the code below at the right place.

    sdlog.info("SDSEARCH-620","Retrieve timestamps begins")
    metadata=fill_dataset_timestamp(squeries,metadata,parallel,action) # complete missing info
    sdlog.info("SDSEARCH-634","Retrieve timestamps ends")

    if sdconfig.copy_ds_attrs:
        sdlog.info("SDSEARCH-624","Retrieve datasets attrs begins")
        metadata=copy_dataset_attrs(squeries,metadata,parallel,action)
        sdlog.info("SDSEARCH-644","Retrieve datasets attrs ends")


    return metadata

def _get_files(squeries,parallel,post_pipeline_mode,action,playback,record,negspecs):
    """
    TODO: maybe move this code inside sdmts module (e.g. metadata.dump(path))
    """

    if playback is not None:
        with open(playback, 'r') as fh:
            metadata=sdtypes.Metadata(files=json.load(fh)) # warning: load full list in memory

    else:

        metadata=execute_queries(squeries,parallel,post_pipeline_mode,action,negspecs)

        if record is not None:
            with open(record, 'w') as fh:
                json.dump(metadata.get_files(),fh,indent=4) # warning: load full list in memory

    return metadata

def fill_dataset_timestamp(squeries,metadata,parallel,action):

    # HACK
    #
    # second run to retrieve dataset timestamps in one row
    #
    # MEMO: when action is 'install', type is always 'File' (i.e. this code gets executed only for type=File)
    #
    if action is not None:
        if action=='install':
            metadata=sdbatchtimestamp.run(squeries,metadata,parallel)

    return metadata

def copy_dataset_attrs(squeries,metadata,parallel,action):

    # HACK
    #
    # retrieve dataset attrs in one row
    #
    # MEMO: when action is 'install', type is always 'File' (i.e. this code gets executed only for type=File)
    #
    if action is not None:
        if action=='install':
            metadata=sdadddsattr.run(squeries,metadata,parallel)

    return metadata

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""examples of use
  %s -f file
  cat file | %s
%s
"""%(prog,prog,sdcliex.search(prog)))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)

    parser.add_argument('-f','--file',default=None)
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-i','--index_host')
    parser.add_argument('-m','--post_pipeline_mode',default='file',choices=sdconst.POST_PIPELINE_MODES)
    parser.add_argument('-y','--dry_run',action='store_true')
    parser.add_argument('-z','--print_short',action='store_true')
    parser.add_argument('-1','--print_only_one_item',action='store_true')

    sdcommonarg.add_playback_record_options(parser)

    parser.add_argument('--load-default',dest='load_default',action='store_true')
    parser.add_argument('--no-load-default',dest='load_default',action='store_false')
    parser.set_defaults(load_default=None)

    parser.add_argument('--parallel',dest='parallel',action='store_true')
    parser.add_argument('--no-parallel',dest='parallel',action='store_false')
    parser.set_defaults(parallel=True)

    args = parser.parse_args()

    metadata=run(path=args.file,
                 parameter=args.parameter,
                 post_pipeline_mode=args.post_pipeline_mode,
                 dry_run=args.dry_run,
                 load_default=args.load_default,
                 parallel=args.parallel,
                 playback=args.playback,
                 record=args.record)

    if not args.dry_run:
        if args.print_short:
            from pprint import pprint
            datasets = list(set([f['dataset_functional_id'] for f in metadata.get_files()]))
            datasets.sort()
            pprint(datasets)
        else:
            sdprint.print_format(metadata.get_files(),args.format,args.print_only_one_item) # warning: load list in memory
