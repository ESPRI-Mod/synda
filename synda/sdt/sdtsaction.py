#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from synda.sdt import sdprint
from synda.sdt.sdtools import print_stderr
from synda.sdt import sdexception
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.api.esgf_search.constants import STRUCTURE as SEARCH_API_STRUCTURE
from synda.source.config.api.constants import METADATA_SERVER_TYPES
from synda.source.process.subcommand.constants import get_default_limit

from synda.source.config.process.count.messages import DATASET_FOUND_TEMPLATE as COUNT_DATASET_FOUND_TEMPLATE
from synda.source.config.process.count.messages import FILE_FOUND_TEMPLATE as COUNT_FILE_FOUND_TEMPLATE
from synda.source.config.process.count.messages import VARIABLE_NOT_IMPLEMENTED as COUNT_VARIABLE_NOT_IMPLEMENTED

from synda.source.config.process.list.messages import DATASET_NOT_FOUND as LIST_DATASET_NOT_FOUND
from synda.source.config.process.list.messages import FILE_NOT_FOUND as LIST_FILE_NOT_FOUND
from synda.source.config.process.list.messages import VARIABLE_NOT_IMPLEMENTED as LIST_VARIABLE_NOT_IMPLEMENTED


def list_(args):
    from synda.sdt import sdearlystreamutils

    """
    disabled as is more practical to list everything by default and filter only on user request.

    from synda.sdt import sddeferredafter

    # add default status depending on type
    if args.type_==SEARCH_API_STRUCTURE['type']['file']:
        sddeferredafter.add_default_parameter(args.stream,'status','done')
    elif args.type_==SEARCH_API_STRUCTURE['type']['dataset']:
        sddeferredafter.add_default_parameter(args.stream,'status','complete')
    """

    # branching
    if args.type_== SEARCH_API_STRUCTURE['type']['file']:
        file_list(args)
    elif args.type_== SEARCH_API_STRUCTURE['type']['aggregation']:
        move_to_dataset_printing_routine=sdearlystreamutils.is_one_variable_per_dataset_project(args.stream) # HACK
        if move_to_dataset_printing_routine:
            # one var exist per dataset for this project

            dataset_list(args)
        else:
            # many var exist per dataset for this project

            variable_list(args)

    elif args.type_== SEARCH_API_STRUCTURE['type']['dataset']:
        dataset_list(args)


def search(args):
    from synda.sdt import sdearlystreamutils,sdstream

    if args.replica:
        from synda.sdt import sddeferredafter
        sdstream.set_scalar(args.stream,'keep_replica','true')
        sddeferredafter.add_forced_parameter(args.stream,'nearest','false')

    # timestamp filters
    if args.timestamp_left_boundary is not None:
        sdstream.set_scalar(args.stream,'from',args.timestamp_left_boundary)
    if args.timestamp_right_boundary is not None:
        sdstream.set_scalar(args.stream,'to',args.timestamp_right_boundary)

    if args.type_== SEARCH_API_STRUCTURE['type']['file']:
        file_search(args)
    elif args.type_== SEARCH_API_STRUCTURE['type']['aggregation']:
        move_to_dataset_printing_routine=sdearlystreamutils.is_one_variable_per_dataset_project(args.stream) # HACK
        if move_to_dataset_printing_routine:
            # one var exist per dataset for this project

            dataset_search(args)
        else:
            # many var exist per dataset for this project

            variable_search(args)

    elif args.type_== SEARCH_API_STRUCTURE['type']['dataset']:
        dataset_search(args)


def show(args):
    if args.type_== SEARCH_API_STRUCTURE['type']['file']:
        file_show(args)
    elif args.type_== SEARCH_API_STRUCTURE['type']['aggregation']:
        print_stderr('Not implemented yet.')   
    elif args.type_== SEARCH_API_STRUCTURE['type']['dataset']:
        dataset_show(args)


def version(args):
    if args.type_== SEARCH_API_STRUCTURE['type']['file']:
        file_version(args)
    elif args.type_== SEARCH_API_STRUCTURE['type']['aggregation']:
        print_stderr('%s operation is not available for variable/aggregation type'%args.action)   
    elif args.type_== SEARCH_API_STRUCTURE['type']['dataset']:
        dataset_version(args)


def dump(args):
    if args.type_== SEARCH_API_STRUCTURE['type']['file']:
        file_dump(args)
    elif args.type_== SEARCH_API_STRUCTURE['type']['aggregation']:
        print_stderr("'%s' operation is not available for variable/aggregation type"%args.subcommand)   
    elif args.type_== SEARCH_API_STRUCTURE['type']['dataset']:
        dataset_dump(args)


def count(args):
    from synda.sdt import sdstream

    # timestamp filters
    if args.timestamp_left_boundary is not None:
        sdstream.set_scalar(args.stream,'from',args.timestamp_left_boundary)
    if args.timestamp_right_boundary is not None:
        sdstream.set_scalar(args.stream,'to',args.timestamp_right_boundary)


    if args.type_== SEARCH_API_STRUCTURE['type']['file']:
        file_count(args)
    elif args.type_== SEARCH_API_STRUCTURE['type']['aggregation']:
        print_stderr("'%s' operation is not available for variable/aggregation type"%args.subcommand)   
    elif args.type_== SEARCH_API_STRUCTURE['type']['dataset']:
        dataset_count(args)


def dataset_foobar(args):
    print_stderr('Not implemented yet.')   


def variable_foobar(args):
    print_stderr('Not implemented yet.')   


def file_foobar(args):
    print_stderr('Not implemented yet.')   


def dataset_count(args):
    from synda.sdt import sdquickcount
    result=sdquickcount.run(
        stream=args.stream,
        index_host=args.index_host,
        dry_run=args.dry_run,
        type_=SEARCH_API_STRUCTURE['type']['dataset'],
    )

    print(
        COUNT_DATASET_FOUND_TEMPLATE.format(
            result.num_found,
        ),
    )


def variable_count(args):
    print_stderr(COUNT_VARIABLE_NOT_IMPLEMENTED)


def file_count(args):
    from synda.sdt import sdquickcount
    result = sdquickcount.run(
        stream=args.stream,
        index_host=args.index_host,
        dry_run=args.dry_run,
        type_=SEARCH_API_STRUCTURE['type']['file'],
    )

    print(
        COUNT_FILE_FOUND_TEMPLATE.format(
            result.num_found,
        ),
    )


def dataset_list(args):
    from synda.sdt import sddeferredafter

    sddeferredafter.add_default_parameter(args.stream,'limit',get_default_limit('list'))

    from synda.sdt import sdldataset
    datasets=sdldataset.get_datasets(stream=args.stream,dry_run=args.dry_run)
    if len(datasets)==0:
        print_stderr(LIST_DATASET_NOT_FOUND)
    else:
        sdldataset.print_list(datasets)


def variable_list(args):
    from synda.sdt import sddeferredafter

    sddeferredafter.add_default_parameter(args.stream,'limit',get_default_limit('list')) # note: in variable mode, total number of row is given by: "total+=#variable for each ds"

    print_stderr(LIST_VARIABLE_NOT_IMPLEMENTED)
    """
    from synda.sdt import sdldataset
    datasets=sdldataset.get_datasets(stream=args.stream,dry_run=args.dry_run)
    if len(datasets)==0:
        print("Variable not found")
    else:
        sdldataset.print_list(datasets)
    """


def file_list(args):
    from synda.sdt import sddeferredafter, sdlfile

    sddeferredafter.add_default_parameter(args.stream,'limit',get_default_limit('list'))

    files=sdlfile.get_files(stream=args.stream,dry_run=args.dry_run)
    if len(files)==0:
        print_stderr(LIST_FILE_NOT_FOUND)
    else:
        sdlfile.print_list(files)


def dataset_search(args):
    from synda.sdt import sddeferredafter, sdrdataset, sdfields, sdearlystreamutils

    sddeferredafter.add_default_parameter(args.stream,'limit',args.limit)

    lpcme=sdearlystreamutils.test_facet_value_early(args.stream,'local_path_format','custom') # lpcme means 'Local Path Custom Mode Enabled'
    fields_=sdfields.get_all_dataset_fields() if lpcme else sdfields.get_dataset_light_fields()
    sddeferredafter.add_forced_parameter(args.stream,'fields',fields_)

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
    from synda.sdt import sddeferredafter, sdrdataset, sdrvariable, sdfields, sdearlystreamutils

    sddeferredafter.add_default_parameter(args.stream,'limit',args.limit) # TAGJ43JK3J43

    lpcme=sdearlystreamutils.test_facet_value_early(args.stream,'local_path_format','custom') # lpcme means 'Local Path Custom Mode Enabled'
    fields_=sdfields.get_all_variable_fields() if lpcme else sdfields.get_variable_light_fields()
    sddeferredafter.add_forced_parameter(args.stream,'fields',fields_)

    datasets=sdrdataset.get_datasets(stream=args.stream,dry_run=args.dry_run)

    if len(datasets)==0:
        print("Variable not found")
    else:
        sdrvariable.print_list(datasets,args.limit) # TAGJ43JK3J43

    # TAGJ43JK3J43
    # In variable mode, the total number of row is given by: "total+=#variable for each ds".
    # First, we limit the number of returned datasets, then we limit the number of variable
    # (this is needed as we don't know in advance the number of variable for each dataset)


def file_search(args):
    from synda.sdt import sdfilesearch
    metadata_server_type = Preferences().core_metadata_server_type
    if metadata_server_type not in METADATA_SERVER_TYPES:
        raise sdexception.SDException(
            'SDTSACTI-001',
            'Incorrect metadata server type (%s)' % metadata_server_type,
        )

    return getattr(sdfilesearch, metadata_server_type)(args)


def dataset_show(args):
    from synda.sdt import sdearlystreamutils

    # check
    li=sdearlystreamutils.get_facet_values_early(args.stream,'instance_id')
    if len(li)==0:
        print_stderr('Please specify a dataset name.')
        return 1
    elif len(li)>1:
        print_stderr('Too many arguments.')
        return 1

    if args.localsearch:
        from synda.sdt import sdldataset
        dataset=sdldataset.get_dataset(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if dataset is None:
                print_stderr("Dataset not found")
            else:
                sdldataset.print_details(dataset)
    else:
        from synda.sdt import sdrdataset
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
        from synda.sdt import sdldataset
        dataset=sdldataset.get_dataset(stream=args.stream,dry_run=args.dry_run)
        if dataset is None:
            print("Variable not found")
        else:
            sdldataset.print_details(dataset)
        """
    else:
        print_stderr('Not implemented yet.')   
        """
        from synda.sdt import sdrdataset

        sddeferredafter.add_forced_parameter(args.stream,'fields','instance_id,id,type') # force output fields
        dataset=sdrdataset.get_dataset(stream=args.stream,dry_run=args.dry_run)
        if dataset is None:
            print_stderr("Variable not found")
        else:
            sdrdataset.print_details(dataset)
        """


def file_show(args):
    from synda.sdt import sdearlystreamutils

    # check

    li=sdearlystreamutils.get_facet_values_early(args.stream,'instance_id') # check if 'instance_id' exists
    if len(li)==0:
        # 'instance_id' is not found on cli

        li=sdearlystreamutils.get_facet_values_early(args.stream,'title') # check if 'title' exists
        if len(li)==0:
            # 'title' is not found on cli

            # no identifier found, we stop the processing
            print_stderr('Please specify a file identifier (id or filename).')
            return 1

        elif len(li)>1:
            print_stderr('Too many arguments.')
            return 1
    elif len(li)>1:
        print_stderr('Too many arguments.')
        return 1

    # main

    if args.localsearch:
        from synda.sdt import sdlfile
        file=sdlfile.get_file(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if file is None:
                print_stderr("File not found")
            else:
                sdlfile.print_details(file)
    else:
        from synda.sdt import sdrfile
        file=sdrfile.get_file(stream=args.stream,dry_run=args.dry_run)

        if not args.dry_run:
            if file is None:
                print_stderr("File not found")
            else:
                sdrfile.print_details(file)


def dataset_version(args):
    from synda.sdt import sdremoteparam
    from synda.sdt import syndautils
    from synda.sdt import sdearlystreamutils

    # don't be misled about identifiers here: sdinference produces search-api
    # key (always do) name i.e. instance_id, and I use Synda style variable name
    # i.e. dataset_functional_id (for better readability).

    li = sdearlystreamutils.get_facet_values_early(args.stream, 'instance_id')

    if len(li) == 0:
        print_stderr('Please specify a dataset name.')
        return 1
    elif len(li) > 1:
        print_stderr('Too many arguments.')
        return 1
    else:
        dataset_functional_id = li[0]

    dataset_functional_id_without_version = syndautils.strip_dataset_version(dataset_functional_id)
    params = sdremoteparam.run(
        pname='version',
        facets_group={
            'type': [SEARCH_API_STRUCTURE['type']['dataset']],
            'master_id': [dataset_functional_id_without_version],
        },
        dry_run=args.dry_run,
    )

    # TODO: func for code below
    items = params.get('version', [])
    for item in items:
        print(item.name)


def variable_version(args):
    # there is no version for variable

    print_stderr('Version list feature is only available for dataset.')


def file_version(args):
    print_stderr('Not implemented yet.')


def dataset_dump(args):
    from synda.sdt import sdrdataset
    from synda.sdt import sddeferredafter
    from synda.sdt import sdcolumnfilter

    sddeferredafter.add_default_parameter(
        args.stream,
        'limit',
        get_default_limit('dump'),
    )

    post_pipeline_mode = None if args.raw_mode else 'dataset'
    files = sdrdataset.get_datasets(
        stream=args.stream,
        post_pipeline_mode=post_pipeline_mode,
        dry_run=args.dry_run,
    )

    if not args.dry_run:
        if len(files) > 0:
            files = sdcolumnfilter.run(files, args.column)
            sdprint.print_format(files, args.format)
        else:
            print_stderr('Dataset not found')


def variable_dump(args):
    # there is no dump for variable
    assert False


def file_dump(args):
    from synda.sdt import sdrfile
    from synda.sdt import sddeferredafter
    from synda.sdt import sdcolumnfilter
    from synda.sdt import sdreducecol

    sddeferredafter.add_default_parameter(
        args.stream,
        'limit',
        get_default_limit('dump'),
    )

    if args.raw_mode:
        post_pipeline_mode = None

        # we force '--all' option when '--raw_mode' option is set
        args.all = True
    else:
        post_pipeline_mode = 'file'

    files = sdrfile.get_files(
        stream=args.stream,
        post_pipeline_mode=post_pipeline_mode,
        dry_run=args.dry_run,
    )

    if args.all:
        # do not hide any attribute

        pass
    else:
        # hide non essential attributes

        files = sdreducecol.run(files)

    if not args.dry_run:

        if len(files) > 0:
            files = sdcolumnfilter.run(files, args.column)
            sdprint.print_format(files, args.format)
        else:
            print_stderr("File not found")   


actions = {
    'count': count,
    'dump': dump,
    'list': list_,
    'search': search,
    'show': show,
    'version': version,
}
