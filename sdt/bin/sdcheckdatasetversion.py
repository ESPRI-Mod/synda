#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains dataset versions checking routines (the "synda check dataset_version" command)."""

import sys
import time
import textwrap
import texttable
import sdexception
import sddump
import sdtypes
import sddatasetversion
import sdtxt2pdf
import StringIO

OUT_WIDTH = 80

def versatile_print(s=''):
    output.write(s+'\n')

def print_framed(str):
    tbl = texttable.Texttable()
    tbl.set_cols_dtype(['t'])
    tbl.set_cols_align(['c'])
    tbl.add_row([str])
    tbl.set_cols_width([OUT_WIDTH - 2 - 2])
    versatile_print(tbl.draw())

def print_wrapped(str):
    tw = textwrap.TextWrapper(width = OUT_WIDTH - 1, initial_indent = '  ', subsequent_indent = '    ', break_on_hyphens = False)
    versatile_print('\\\n'.join(tw.wrap(str)))

def run(args):
    global output

    if args.output_format=='text':
        output=sys.stdout
    elif args.output_format=='pdf':
        output=StringIO.StringIO()

    DSV_ERR_FMT = 1
    DSV_ERR_NUM = 2
    DSV_ERR_DUP = 4
    DSV_ERR_SEQ = 8
    dsv_err = [
        { 'name': 'DSV_ERR_FMT',
          'v': DSV_ERR_FMT,
          'dsc': 'Malformed version string. The "version" field does not match (case-insensitively) any of the following Python regular expressions:\n' + '\n'.join(sddatasetversion.DatasetVersion._dataset_version_regexp_strings)
        },
        { 'name': 'DSV_ERR_NUM',
          'v': DSV_ERR_NUM,
          'dsc': 'Cannot extract version number from version string.'
        },
        { 'name': 'DSV_ERR_DUP',
          'v': DSV_ERR_DUP,
          'dsc': 'Duplicate version number. The integer extracted from the "version" field has the same value as that of another version of the same dataset.'
        },
        { 'name': 'DSV_ERR_SEQ',
          'v': DSV_ERR_SEQ,
          'dsc': 'Sequence error. The integer extracted from the "version" field is not strictly greater than that for the previous version in timestamp order of the same dataset.'
        },
    ]
    status = 0
    stats = {
        'dsv_with_version':         0,
        'dsv_without_version':      0,
        'dsv_with_timestamp':       0,
        'dsv_without_timestamp':    0,
        'DSV_ERR_FMT':              0,
        'DSV_ERR_NUM':              0,
        'DSV_ERR_DUP':              0,
        'DSV_ERR_SEQ':              0,
    }
    all_dsv = []
    dsv_grouped_by_master_id = {}
    datasets_with_errors = set()
    dsv_with_errors = 0
    total_errors = 0

    print_framed('Synda report on errors in dataset versions')
    versatile_print()
    versatile_print('Date: %s' % time.strftime('%Y-%m-%d %H:%M:%S %z'))
    versatile_print('Command line:')
    # FIXME make sure we have the exact command line, including options
    print_wrapped(' '.join(sys.argv))

    if args.output_format=='text':
        sys.stdout.flush()

    all_dsv = sddump.dump_ESGF(parameter=args.parameter,selection_file=args.selection_file,fields='master_id,version,timestamp',dry_run=args.dry_run,record=args.record,playback=args.playback)

    if not args.dry_run:

        # group dataset by 'master_id'
        #
        # MEMO
        #     'master_id' is the dataset identifier without 'version' item
        for dsv in all_dsv:
            d = sdtypes.Dataset(**dsv)
            dsv_info = {}
            # The "version" and "timestamp" ESGF fields are optional according
            # to http://earthsystemcog.org/projects/cog/esgf_core_metadata.
            # Haven't come across any version-less data sets so far but there
            # are thousands of timestamp-less data sets out there.
            if 'version' in dir(d):
                stats['dsv_with_version'] += 1
                dsv_info['verstr'] = d.version
            else:
                stats['dsv_without_version'] += 1
                dsv_info['verstr'] = 0
            ds_flags = 0
            if 'timestamp' in dir(d):
                stats['dsv_with_timestamp'] += 1
                dsv_info['timestamp'] = d.timestamp
                ds_flags = 1
            else:
                stats['dsv_without_timestamp'] += 1
                #dsv_info['timestamp'] = '1970-01-01T00:00:00Z'
                ds_flags = 2
            if d.master_id not in dsv_grouped_by_master_id:
                dsv_grouped_by_master_id[d.master_id] = {}
                dsv_grouped_by_master_id[d.master_id]['flags'] = ds_flags
                dsv_grouped_by_master_id[d.master_id]['dsv'] = []
            dsv_grouped_by_master_id[d.master_id]['flags'] |= ds_flags
            dsv_grouped_by_master_id[d.master_id]['dsv'].append(dsv_info)

        # debug
        # print how many version exist for each dataset
        """
        for master_id,dataset_versions in dsv_grouped_by_master_id.iteritems():
            versatile_print('%s => %i'%(master_id,dataset_versions.count()))
        """

        # Add "vfn" & "vernum" keys to every dsv_info
        for master_id, ds_info in dsv_grouped_by_master_id.iteritems():
            for dsv_info in ds_info['dsv']:
                vfn, vernum = sddatasetversion.DatasetVersion(dsv_info['verstr']).analyse()
                dsv_info['vfn'] = vfn
                dsv_info['vernum'] = vernum

        # Initialise the per-data-set error counters and per-data-set version
        # error flags
        for master_id, ds_info in dsv_grouped_by_master_id.iteritems():
            ds_info['errors'] = 0
            for dsv_info in ds_info['dsv']:
                dsv_info['err_flags'] = 0

        # Basic check : all version strings must have a valid format and we
        # must be able to extract a version number from them.
        for master_id, ds_info in dsv_grouped_by_master_id.iteritems():
            for dsv_info in ds_info['dsv']:
                if dsv_info['vfn'] is None:
                    dsv_info['err_flags'] |= DSV_ERR_FMT
                    ds_info['errors'] += 1
                if dsv_info['vernum'] is None:
                    dsv_info['err_flags'] |= DSV_ERR_NUM
                    ds_info['errors'] += 1

        # Intermediate check : no two versions of the same data set must have
        # the same versions numbers.
        for master_id, ds_info in dsv_grouped_by_master_id.iteritems():
            dsv_verstr = set()
            for dsv_info in ds_info['dsv']:
                if dsv_info['vernum'] in dsv_verstr:
                    dsv_info['err_flags'] |= DSV_ERR_DUP
                    ds_info['errors'] += 1
                dsv_verstr.add(dsv_info['vernum'])

        # Monotonicity check : verify that, after sorting the versions by
        # timestamp, the version numbers are strictly increasing. Versions
        # which have no "timestamp" field must be excluded from the check.
        for master_id, ds_info in dsv_grouped_by_master_id.iteritems():
            dsv_list = []
            for dsv_info in ds_info['dsv']:
                if 'timestamp' in dsv_info:
                    dsv_list.append(dsv_info)
            dsv_list = sorted(dsv_list, cmp = lambda a, b: cmp(a['timestamp'], b['timestamp']))
            for n, dsv_info in enumerate(dsv_list):
                if n > 0 and dsv_info['vernum'] <= dsv_list[n - 1]['vernum']:
                    dsv_info['err_flags'] |= DSV_ERR_SEQ
                    ds_info['errors'] += 1

        # datasets_with_errors = the master_id of all the data sets with errors
        for master_id, ds_info in dsv_grouped_by_master_id.iteritems():
            if ds_info['errors'] != 0:
                datasets_with_errors.add(master_id)

        # Write a report for each dataset with errors
        for master_id in sorted(datasets_with_errors):
            dsv_list = dsv_grouped_by_master_id[master_id]['dsv']
            nmax = len(dsv_list)
            versatile_print('\nDataset "%s":' % (master_id))
            dataset_errors = 0
            for n, dsv_info in enumerate(dsv_list, 1):
                if 'timestamp' in dsv_info:
                    ts = '"%s"' % dsv_info['timestamp']
                else:
                    ts = 'none'
                versatile_print('  Version %d/%d: time stamp %s, version string "%s":' % (n, nmax, ts, dsv_info['verstr']))
                err_flags = dsv_info['err_flags']
                if err_flags == 0:
                    versatile_print('    No errors')
                else:
                    if err_flags & DSV_ERR_FMT:
                        versatile_print('    Version string is not in any known format')
                    if err_flags & DSV_ERR_NUM:
                        versatile_print('    Cannot extract version number from version string')
                    if err_flags & DSV_ERR_DUP:
                        versatile_print('    Version string is a duplicate of another version string in the same dataset')
                    if err_flags & DSV_ERR_SEQ:
                        versatile_print('    Version number is not greater than previous version (%s -> %s)' % (dsv_list[n - 2]['vernum'], dsv_info['vernum']))
                    dsv_errors = 0
                    bits = dsv_info['err_flags']
                    while bits != 0:
                        if bits & 1:
                            dsv_errors += 1
                        bits >>= 1
                    dataset_errors += dsv_errors
                    dsv_with_errors += 1
            versatile_print('  Dataset has %d error(s)' % (dataset_errors))
            total_errors += dataset_errors

    # Write a summary
    digits = len('%d' % (len(all_dsv)))
    versatile_print('\nFound %d dataset versions(s), of which' % (len(all_dsv)))
    versatile_print('  %*d have a timestamp field' % (digits, stats['dsv_with_timestamp']))
    versatile_print('  %*d lack a timestamp field' % (digits, stats['dsv_without_timestamp']))

    #digits = len('%d' % (len(dsv_grouped_by_master_id)))
    versatile_print('\nFound %d dataset(s), of which' % (len(dsv_grouped_by_master_id)))
    versatile_print('  %*d have a timestamp field on all  of their versions' % (digits, sum(map(lambda x: 1 if x['flags'] == 1 else 0, dsv_grouped_by_master_id.values()))))
    versatile_print('  %*d have a timestamp field on some of their versions' % (digits, sum(map(lambda x: 1 if x['flags'] == 3 else 0, dsv_grouped_by_master_id.values()))))
    versatile_print('  %*d have a timestamp field on none of their versions' % (digits, sum(map(lambda x: 1 if x['flags'] == 2 else 0, dsv_grouped_by_master_id.values()))))

    versatile_print('\nBreakdown of errors:')
    tbl = texttable.Texttable()
    tbl.set_cols_dtype(['i', 'i', 't'])
    tbl.set_cols_align(['r', 'r', 'l'])
    tbl.add_row(['Datasets', 'Dataset versions', 'Description of the error'])
    tbl.set_cols_valign(['t', 't', 't'])
    for e in dsv_err:
        ds_count = 0
        dsv_count = 0
        for master_id, ds_info in dsv_grouped_by_master_id.iteritems():
            c = 0
            for dsv_info in ds_info['dsv']:
                if dsv_info['err_flags'] & e['v']:
                    c += 1
            dsv_count += c
            if c != 0:
                ds_count += 1
        tbl.add_row([dsv_count, ds_count, e['dsc']])
    tbl.add_row([dsv_with_errors, len(datasets_with_errors), 'One or more of the above'])
    # FIXME don't hard code
    ds_digits = max(8, digits)
    dsv_digits = max(8, digits)
    dsc_width = OUT_WIDTH - 2 - ds_digits - 3 - dsv_digits - 3 - 2
    tbl.set_cols_width([ds_digits, dsv_digits, dsc_width])
    versatile_print(tbl.draw())

    versatile_print('\nA total of %d error(s) were found' % (total_errors))
    versatile_print('End of report')
    if (total_errors != 0):
        status = 1

    if args.output_format=='pdf':
        sdtxt2pdf.run(output,args.outfile,False)

    return status

# init.
output=None
