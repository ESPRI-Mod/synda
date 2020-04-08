

from sdt.bin.commons.search import sdsearch
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import syndautils
from sdt.bin.commons.utils import sdtools
from sdt.bin.commons.param import sddeferredbefore
from sdt.bin.commons.pipeline import sdpostpipelineutils
from sdt.bin.commons.pipeline import sdpporder
from sdt.bin.db import dao
from sdt.bin.db import session


def run(args):
    if args.order_name == 'cdf':
        selection_filename = None

        # use search-api operator to build datasets list
        stream = syndautils.get_stream(subcommand=args.subcommand, selection_file=args.selection_file,
                                       no_default=args.no_default)
        sddeferredbefore.add_forced_parameter(stream, 'type', 'Dataset')

        dataset_found_count = 0
        order_variable_count = 0
        order_dataset_count = 0
        for facets_group in stream:  # we need to process each facets_group one by one because of TAG45345JK3J53K

            metadata = sdsearch.run(stream=[facets_group], post_pipeline_mode='dataset')  # TAGJ43KJ234JK

            dataset_found_count += metadata.count()

            if metadata.count() > 0:

                # WART
                # (gets overwritten at each iteration, but not a big deal as always the same value)
                # this is to keep the first found value (i.e. if last facets_group is empty but not the
                # previous ones do not keep the last one (which would be None))

                if selection_filename is None:
                    dataset = metadata.get_one_file()
                    selection_filename = sdpostpipelineutils.get_attached_parameter__global([dataset],
                                                                                            'selection_filename')
                    # note that if no files are found at all for this selection (no matter the status),
                    # then the filename will be blank

                for d in metadata.get_files():  # warning: load list in memory
                    if d['status'] == sdconst.DATASET_STATUS_COMPLETE:

                        # TAG45J4K45JK

                        # first, send cdf variable order
                        # (note: total number of variable event is given by: "total+=#variable for each ds")
                        for v in d['variable']:
                            # TAG45345JK3J53K (we check here that the variable has been asked for in the first place)
                            if v in facets_group['variable']:
                                order_variable_count += 1

                                # hack
                                # maybe move this test at TAG45J4K45JK line, and replace 'EVENT_CDF_VARIABLE_O' by a
                                # dataset level event (note however that the choice about passing 'EVENT_CDF_VARIABLE_O'
                                # event as variable or dataset is arbitrary, both work. But passing as variable is a bit
                                # strange as variable appears in both dataset_pattern and variable columns)
                                if sdtools.is_one_var_per_ds(d['project']):
                                    e_names = [sdconst.EVENT_CDF_INT_VARIABLE_O, sdconst.EVENT_CDF_COR_VARIABLE_O]
                                    # this case is a bit awkward as we have 'variable' in both dataset_pattern and
                                    # variable columns..

                                else:
                                    e_names = [sdconst.EVENT_CDF_INT_VARIABLE_N, sdconst.EVENT_CDF_COR_VARIABLE_N]

                                for e_name in e_names:
                                    sdpporder.submit(e_name, d['project'], d['model'], d['local_path'], variable=v,
                                                     commit=False)

                        # second, send cdf dataset order
                        if d['project'] in sdconst.PROJECT_WITH_ONE_VARIABLE_PER_DATASET:

                            # we do not trigger 'dataset' level event in this case
                            pass
                        else:

                            order_dataset_count += 1

                            e_names = [sdconst.EVENT_CDF_INT_DATASET, sdconst.EVENT_CDF_COR_DATASET]
                            for e_name in e_names:
                                sdpporder.submit(e_name, d['project'], d['model'], d['local_path'], commit=False)

        if dataset_found_count > 0:
            if order_dataset_count == 0 and order_variable_count == 0:
                print_stderr("Data not ready (data must be already downloaded "
                             "before performing pexec task): operation cancelled")
            else:
                with session.create():
                    dao.add_history_line(sdconst.ACTION_PEXEC, selection_filename)
                print_stderr("Post-processing task successfully submitted "
                             "(order_dataset_count={},order_variable_count={})".format(order_dataset_count,
                                                                                       order_variable_count))
        else:
            print_stderr('Data not found')

    elif args.order_name == 'cds':
        selection_filename = None

        # use search-api operator to build datasets list
        stream = syndautils.get_stream(subcommand=args.subcommand, selection_file=args.selection_file,
                                       no_default=args.no_default)
        sddeferredbefore.add_forced_parameter(stream, 'type', 'Dataset')

        dataset_found_count = 0
        order_variable_count = 0
        for facets_group in stream:  # we need to process each facets_group one by one because of TAG45345JK3J53K

            metadata = sdsearch.run(stream=[facets_group], post_pipeline_mode='dataset')  # TAGJ43KJ234JK

            dataset_found_count += metadata.count()

            if metadata.count() > 0:

                # WART
                # (gets overwritten at each iteration, but not a big deal as always the same value)
                # this is to keep the first found value (i.e. if last facets_group is empty but not the previous
                # ones do not keep the last one (which would be None))

                if selection_filename is None:
                    dataset = metadata.get_one_file()
                    # note that if no files are found at all for this selection (no matter the status),
                    # then the filename will be blank

                    selection_filename = sdpostpipelineutils.get_attached_parameter__global([dataset],
                                                                                            'selection_filename')
                for d in metadata.get_files():  # warning: load list in memory
                    if d['status'] == sdconst.DATASET_STATUS_COMPLETE:

                        # TAG45J4K45JK

                        # send cds variable order
                        # (note: total number of variable event is given by: "total+=#variable for each ds")
                        for v in d['variable']:
                            # we check here that the variable has been asked for in the first place
                            if v in facets_group['variable']:
                                order_variable_count += 1
                                sdpporder.submit(sdconst.EVENT_CDS_VARIABLE, d['project'], d['model'], d['local_path'],
                                                 variable=v, commit=False)

        if dataset_found_count > 0:
            if order_variable_count == 0:
                print_stderr("Data not ready (data must be already downloaded "
                             "before performing pexec task): operation cancelled")
            else:
                with session.create():
                    dao.add_history_line(sdconst.ACTION_PEXEC, selection_filename)
                print_stderr("Post-processing task successfully submitted "
                             "(order_variable_count={})".format(order_variable_count))
        else:
            print_stderr('Data not found')

    else:
        print_stderr("Invalid order name ('{}')".format(args.order_name))
        return 1
    return 0
