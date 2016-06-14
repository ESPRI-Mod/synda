#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
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

    """
    disabled as is more practical to list everything by default and filter only on user request.

    import sddeferredafter

    # add default status depending on type
    if args.type_==sdconst.SA_TYPE_FILE:
        sddeferredafter.add_default_parameter(args.stream,'status','done')
    elif args.type_==sdconst.SA_TYPE_DATASET:
        sddeferredafter.add_default_parameter(args.stream,'status','complete')
    """

    # branching
    if args.type_==sdconst.SA_TYPE_FILE:
        file_list(args)
    elif args.type_==sdconst.SA_TYPE_AGGREGATION:
        move_to_dataset_printing_routine=syndautils.is_one_variable_per_dataset_project(args) # HACK
        if move_to_dataset_printing_routine:
            # one var exist per dataset for this project

            dataset_list(args)
        else:
            # many var exist per dataset for this project

            variable_list(args)

    elif args.type_==sdconst.SA_TYPE_DATASET:
        dataset_list(args)

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

def pexec(args):

    # HACK
    if args.order_name=sdconst.EVENT_PEXEC_001:
        args.type_=sdconst.SA_TYPE_AGGREGATION
    else:
        assert False

    if args.type_==sdconst.SA_TYPE_FILE:
        file_pexec(args)
    elif args.type_==sdconst.SA_TYPE_AGGREGATION:
        variable_pexec(args)
    elif args.type_==sdconst.SA_TYPE_DATASET:
        dataset_pexec(args)

# o=======================================================o

def dataset_foobar(args):
    print_stderr('Not implemented yet.')   

def variable_foobar(args):
    print_stderr('Not implemented yet.')   

def file_foobar(args):
    print_stderr('Not implemented yet.')   

# o-------------------------------------------------------o

def dataset_list(args):
    import sddeferredafter

    sddeferredafter.add_default_parameter(args.stream,'limit',20)

    import sdldataset
    datasets=sdldataset.get_datasets(stream=args.stream,dry_run=args.dry_run)
    if len(datasets)==0:
        print_stderr('Dataset not found')
    else:
        sdldataset.print_list(datasets)

def variable_list(args):
    import sddeferredafter

    sddeferredafter.add_default_parameter(args.stream,'limit',15) # note: in variable mode, total number of row is given by: "total+=#variable for each ds"

    print_stderr('Not implemented yet.')   
    """
    import sdldataset
    datasets=sdldataset.get_datasets(stream=args.stream,dry_run=args.dry_run)
    if len(datasets)==0:
        print "Variable not found"
    else:
        sdldataset.print_list(datasets)
    """

def file_list(args):
    import sddeferredafter, sdlfile

    sddeferredafter.add_default_parameter(args.stream,'limit',20)

    files=sdlfile.get_files(stream=args.stream,dry_run=args.dry_run)
    if len(files)==0:
        print_stderr("File not found")   
    else:
        sdlfile.print_list(files)

# o-------------------------------------------------------o

def dataset_search(args):
    import sddeferredafter, sdrdataset, sdstream

    sddeferredafter.add_default_parameter(args.stream,'limit',100) # add default limit
    sddeferredafter.add_forced_parameter(args.stream,'fields',dataset_light_fields)

    datasets=sdrdataset.get_datasets(stream=args.stream,dry_run=args.dry_run)

    if not args.dry_run:
        if len(datasets)==0:
            print_stderr('Dataset not found')
        else:
            if args.replica:
                sdrdataset.print_replica_list(datasets)
            else:
                sdrdataset.print_list(datasets)

def variable_search(args):
    import sddeferredafter, sdrdataset, sdrvariable

    sddeferredafter.add_default_parameter(args.stream,'limit',15) # note: in variable mode, total number of row is given by: "total+=#variable for each ds"
    sddeferredafter.add_forced_parameter(args.stream,'fields',variable_light_fields)

    datasets=sdrdataset.get_datasets(stream=args.stream,dry_run=args.dry_run)

    if len(datasets)==0:
        print "Variable not found"
    else:
        sdrvariable.print_list(datasets)

def file_search(args):
    import sdrfile, sddeferredafter

    # tuning: note that we don't reduce the number of field returned here.
    # Maybe change that to optimise download time / reduce bandwidth footprint.

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

    # check
    li=syndautils.get_facet_values_early(args.stream,'instance_id')
    if len(li)==0:
        print_stderr('Please specify a dataset name.')
        return
    elif len(li)>1:
        print_stderr('Too many arguments.')
        return

    if args.localsearch:
        import sdldataset
        dataset=sdldataset.get_dataset(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if dataset is None:
                print_stderr("Dataset not found")
            else:
                sdldataset.print_details(dataset)
    else:
        import sdrdataset
        dataset=sdrdataset.get_dataset(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if dataset is None:
                print_stderr("Dataset not found")
            else:
                sdrdataset.print_details(dataset,verbose=args.verbose)

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


    # check

    li=syndautils.get_facet_values_early(args.stream,'instance_id') # check if 'instance_id' exists
    if len(li)==0:
        # 'instance_id' is not found on cli

        li=syndautils.get_facet_values_early(args.stream,'title') # check if 'title' exists
        if len(li)==0:
            # 'title' is not found on cli

            # no identifier found, we stop the processing
            print_stderr('Please specify a file identifier (id or filename).')
            return

        elif len(li)>1:
            print_stderr('Too many arguments.')
            return
    elif len(li)>1:
        print_stderr('Too many arguments.')
        return


    # main

    if args.localsearch:
        import sdlfile
        file=sdlfile.get_file(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if file is None:
                print_stderr("File not found")
            else:
                sdlfile.print_details(file)
    else:
        import sdrfile
        file=sdrfile.get_file(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if file is None:
                print_stderr("File not found")
            else:
                sdrfile.print_details(file)

# o-------------------------------------------------------o

def dataset_version(args):
    import sdremoteparam

    # don't be misled about identifiers here: sdinference produces search-api
    # key (always do) name i.e. instance_id, and I use Synda style variable name
    # i.e. dataset_functional_id (for better readability).

    li=syndautils.get_facet_values_early(args.stream,'instance_id')

    if len(li)==0:
        print_stderr('Please specify a dataset name.')
        return
    elif len(li)>1:
        print_stderr('Too many arguments.')
        return
    else:
        dataset_functional_id=li[0]

    dataset_functional_id_without_version=syndautils.strip_dataset_version(dataset_functional_id)
    params=sdremoteparam.run(pname='version',facets_group={'type':[sdconst.SA_TYPE_DATASET],'master_id':[dataset_functional_id_without_version]},dry_run=args.dry_run)
    # TODO: func for code below
    items=params.get('version',[])
    for item in items:
        print item.name

def variable_version(args):
    # there is no version for variable

    print_stderr('Version list feature is only available for dataset.')

def file_version(args):
    print_stderr('Not implemented yet.')   

# o-------------------------------------------------------o

def dataset_dump(args):
    import sdrdataset, sddeferredafter, sdcolumnfilter

    sddeferredafter.add_default_parameter(args.stream,'limit',100)
    post_pipeline_mode=None if args.raw_mode else 'dataset'
    files=sdrdataset.get_datasets(stream=args.stream,post_pipeline_mode=post_pipeline_mode,dry_run=args.dry_run)

    if not args.dry_run:
        if len(files)>0:
            files=sdcolumnfilter.run(files,args.column)
            sdprint.print_format(files,args.format)
        else:
            print_stderr('Dataset not found')

def variable_dump(args):
    assert False # there is no dump for variable

def file_dump(args):
    import sdrfile, sddeferredafter, sdcolumnfilter, sdreducecol

    sddeferredafter.add_default_parameter(args.stream,'limit',100)


    if args.raw_mode:
        post_pipeline_mode=None

        args.all=True # we force '--all' option when '--raw_mode' option is set
    else:
        post_pipeline_mode='file'


    files=sdrfile.get_files(stream=args.stream,post_pipeline_mode=post_pipeline_mode,dry_run=args.dry_run)


    if args.all:
        # do not hide any attribute

        pass
    else:
        # hide non essential attributes

        files=sdreducecol.run(files)


    if not args.dry_run:
        if len(files)>0:
            files=sdcolumnfilter.run(files,args.column)
            sdprint.print_format(files,args.format)
        else:
            print_stderr("File not found")   

# o-------------------------------------------------------o

def dataset_pexec(args):
    import sdrdataset, sddeferredafter, sdstream, sdpporder, sddb

    sddeferredafter.add_default_parameter(args.stream,'limit',8000) # add default limit

    datasets=sdrdataset.get_datasets(stream=args.stream)

    if len(datasets)>0:
        for d in datasets:
            if d['status']==sdconst.DATASET_STATUS_COMPLETE:
                sdpporder.submit(args.order_name,sdconst.SA_TYPE_DATASET,d['project'],d['model'],d['local_path'],commit=False)
        sddb.conn.commit()

        print_stderr("Post-processing task successfully submitted")   
    else:
        print_stderr('Dataset not found')   

def variable_pexec(args):
    import sdrdataset, sdrvariable, sddeferredafter, sdpporder, sddb

    sddeferredafter.add_default_parameter(args.stream,'limit', 8000) # note: in variable mode, total number of row is given by: "total+=#variable for each ds"

    datasets=sdrdataset.get_datasets(stream=args.stream)

    if len(datasets)>0:
        for d in datasets:
            if d['status']==sdconst.DATASET_STATUS_COMPLETE: # TODO: use VARIABLE_COMPLETE here !
                for v in d['variable']:
                    sdpporder.submit(args.order_name,sdconst.SA_TYPE_AGGREGATION,d['project'],d['model'],d['local_path'],variable=v,commit=False)
        sddb.conn.commit()

        print_stderr("Post-processing task successfully submitted")   
    else:
        print_stderr('Variable not found')   

def file_pexec(args):
    import sdrfile, sddeferredafter, sdpporder, sddb

    sddeferredafter.add_default_parameter(args.stream,'limit',8000)

    files=sdrfile.get_files(stream=args.stream)

    if len(files)>0:
        for f in files:
            if f['status']==sdconst.TRANSFER_STATUS_DONE:
                sdpporder.submit(args.order_name,sdconst.SA_TYPE_FILE,f['project'],f['model'],f['dataset_local_path'],variable=f['variable'],filename=f['filename'],commit=False)
        sddb.conn.commit()

        print_stderr("Post-processing task successfully submitted")   
    else:
        print_stderr("File not found")   

# init.

dataset_light_fields=sdconst.LIGHT_FIELDS
variable_light_fields=sdconst.LIGHT_FIELDS
file_light_fields=sdconst.LIGHT_FIELDS

actions={
    'dump':dump,
    'list':list_, 
    'pexec':pexec, 
    'search':search, 
    'show':show,
    'version':version
}
