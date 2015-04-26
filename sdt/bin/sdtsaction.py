#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains type sensitive action used by 'synda' script.

Note
    In this file, module import directives are moved near the calls,
    so to improve startup time.
"""

import sdconst
import syndautils
import sdprint
from sdtools import print_stderr

def list_(args):
    """list is an alias for search in local mode.
    (i.e. 'synda list' is equivalent to 'synda search -l')
    """
    args.localsearch=True
    search(args)

def search(args):

    if args.replica:
        import sdstream, sddeferredafter
        sdstream.set_scalar(args.stream,'keep_replica','true')
        sddeferredafter.add_forced_parameter(args.stream,'nearest','false')

    if args.type_==sdconst.SA_TYPE_FILE:
        file_search(args)
    elif args.type_==sdconst.SA_TYPE_AGGREGATION:
        move_to_dataset_printing_routine=syndautils.is_one_variable_per_dataset_project(args) # HACK
        if move_to_dataset_printing_routine:
            # one var exist per dataset for this project

            dataset_search(args)
        else:
            # many var exist per dataset for this project

            variable_search(args)

    elif args.type_==sdconst.SA_TYPE_DATASET:
        dataset_search(args)

def show(args):
    if args.type_==sdconst.SA_TYPE_FILE:
        file_show(args)
    elif args.type_==sdconst.SA_TYPE_AGGREGATION:
        print_stderr('Not implemented yet.')   
    elif args.type_==sdconst.SA_TYPE_DATASET:
        dataset_show(args)

def version(args):
    if args.type_==sdconst.SA_TYPE_FILE:
        file_version(args)
    elif args.type_==sdconst.SA_TYPE_AGGREGATION:
        print_stderr('%s operation is not available for variable/aggregation type'%args.action)   
    elif args.type_==sdconst.SA_TYPE_DATASET:
        dataset_version(args)

def dump(args):
    if args.type_==sdconst.SA_TYPE_FILE:
        file_dump(args)
    elif args.type_==sdconst.SA_TYPE_AGGREGATION:
        print_stderr('%s operation is not available for variable/aggregation type'%args.action)   
    elif args.type_==sdconst.SA_TYPE_DATASET:
        dataset_dump(args)

# o-------------------------------------------------------o

def dataset_foobar():
    print_stderr('Not implemented yet.')   

def variable_foobar():
    print_stderr('Not implemented yet.')   

def file_foobar():
    print_stderr('Not implemented yet.')   

# o-------------------------------------------------------o

def dataset_search(args):
    import sddeferredafter

    sddeferredafter.add_default_parameter(args.stream,'limit',100) # add default limit

    if args.localsearch:
        import sdldataset
        datasets=sdldataset.get_datasets(stream=args.stream,dry_run=args.dry_run)
        if len(datasets)==0:
            print "Dataset not found"
        else:
            sdldataset.print_list(datasets)
    else:
        import sdrdataset, sddeferredafter, sdstream

        sddeferredafter.add_forced_parameter(args.stream,'fields',dataset_light_fields)
        datasets=sdrdataset.get_datasets(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if len(datasets)==0:
                print "Dataset not found"
            else:
                if args.replica:
                    sdrdataset.print_replica_list(datasets)
                else:
                    sdrdataset.print_list(datasets)

def variable_search(args):
    import sddeferredafter

    sddeferredafter.add_default_parameter(args.stream,'limit',15) # note: in variable mode, total number of row is: (number of dataset) * (variable per dataset)

    if args.localsearch:
        print_stderr('Not implemented yet.')   
        """
        import sdldataset
        datasets=sdldataset.get_datasets(stream=args.stream,dry_run=args.dry_run)
        if len(datasets)==0:
            print "Variable not found"
        else:
            sdldataset.print_list(datasets)
        """
    else:
        import sdrdataset, sdrvariable, sddeferredafter

        sddeferredafter.add_forced_parameter(args.stream,'fields',variable_light_fields)
        datasets=sdrdataset.get_datasets(stream=args.stream,dry_run=args.dry_run)
        if len(datasets)==0:
            print "Variable not found"
        else:
            sdrvariable.print_list(datasets)

def file_search(args):
    # we treat this action separately from the others, as there is different constraint for this action (speed here is the most important so we retrieve only a subset of output attributes)

    import sdrfile, sddeferredafter

    # tuning: note that we don't reduce the number of field returned here. Maybe change that to optimise download time / reduce bandwidth footprint.


    if args.localsearch:
        import sdlfile
        files=sdlfile.get_files(stream=args.stream,dry_run=args.dry_run)
        if len(files)==0:
            print_stderr("File not found")   
        else:
            sdlfile.print_list(files)
    else:
        sddeferredafter.add_default_parameter(args.stream,'limit',100)
        files=sdrfile.get_files(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if len(files)==0:
                print_stderr("File not found")   
            else:
                if args.replica:
                    sdrfile.print_replica_list(files)
                else:
                    sdrfile.print_list(files)

# o-------------------------------------------------------o

def dataset_show(args):
    if args.localsearch:
        import sdldataset
        dataset=sdldataset.get_dataset(stream=args.stream,dry_run=args.dry_run)
        if dataset is None:
            print "Dataset not found"
        else:
            sdldataset.print_details(dataset)
    else:
        import sdrdataset
        dataset=sdrdataset.get_dataset(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if dataset is None:
                print_stderr("Dataset not found")
            else:
                sdrdataset.print_details(dataset)

def variable_show(args):
    if args.localsearch:
        print_stderr('Not implemented yet.')   
        """
        import sdldataset
        dataset=sdldataset.get_dataset(stream=args.stream,dry_run=args.dry_run)
        if dataset is None:
            print "Variable not found"
        else:
            sdldataset.print_details(dataset)
        """
    else:
        print_stderr('Not implemented yet.')   
        """
        import sdrdataset

        sddeferredafter.add_forced_parameter(args.stream,'fields','instance_id,id,type') # force output fields
        dataset=sdrdataset.get_dataset(stream=args.stream,dry_run=args.dry_run)
        if dataset is None:
            print_stderr("Variable not found")
        else:
            sdrdataset.print_details(dataset)
        """

def file_show(args):
    import sdrfile
    file=sdrfile.get_file(stream=args.stream,dry_run=args.dry_run)

    if not args.dry_run:
        if file is None:
            print_stderr("File not found")
        else:
            sdrfile.print_details(file)

# o-------------------------------------------------------o

def dataset_version(args):
    import sdinference,sdstream,sdremoteparam
    stream=sdinference.run(args.stream)
    dataset_functional_id=sdstream.get_scalar(stream,'dataset_id') # don't be misled about identifiers here: sdinference produces search-api key (always do) name and then I use Synchro-data key name (for better readability).
    dataset_functional_id_without_version=syndautils.strip_dataset_version(dataset_functional_id)
    params=sdremoteparam.run(pname='version',facets_group={'type':[sdconst.SA_TYPE_DATASET],'master_id':[dataset_functional_id_without_version]},dry_run=args.dry_run)
    # TODO: func for code below
    items=params.get('version',[])
    for item in items:
        print item.name

def variable_version(args):
    assert False # there is no version for variable

def file_version(args):
    print_stderr('Not implemented yet.')   

# o-------------------------------------------------------o

def dataset_dump(args):
    import sdrdataset, sddeferredafter

    sddeferredafter.add_default_parameter(args.stream,'limit',100)
    post_pipeline_mode=None if args.raw_mode else 'dataset'
    files=sdrdataset.get_datasets(stream=args.stream,post_pipeline_mode=post_pipeline_mode,dry_run=args.dry_run)

    if not args.dry_run:
        if len(files)>0:
            sdprint.print_format(files,args.format)
        else:
            print "Dataset not found"

def variable_dump(args):
    assert False # there is no dump for variable

def file_dump(args):
    import sdrfile, sddeferredafter,sdcolumnfilter

    sddeferredafter.add_default_parameter(args.stream,'limit',100)
    post_pipeline_mode=None if args.raw_mode else 'file'
    files=sdrfile.get_files(stream=args.stream,post_pipeline_mode=post_pipeline_mode,dry_run=args.dry_run)

    if not args.dry_run:
        if len(files)>0:
            files=sdcolumnfilter.run(files,args.column)
            sdprint.print_format(files,args.format)
        else:
            print_stderr("File not found")   

# init.

dataset_light_fields=sdconst.LIGHT_FIELDS
variable_light_fields=sdconst.LIGHT_FIELDS
file_light_fields=sdconst.LIGHT_FIELDS

actions={
    'dump':dump,
    'list':list_, 
    'search':search, 
    'show':show,
    'version':version
}
