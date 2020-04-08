#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains report functions."""

import os
import humanize
import argparse
from tabulate import tabulate

from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils.sdprogress import SDProgressDot
from sdt.bin.db import dao
from sdt.bin.db import session
from sdt.bin.db import dao_operations


def print_selections_stats():
    """List selection's files count (i.e. how many files for each selections)."""
    selections = get_selectionsfilescount()

    for us in selections.values():
        print("{}-50s {}".format(us['FILENAME'], us['COUNT'], ))


def PROC0001():
    """Print obsolete versions of datasets.

    Notes
     - use shell expansion pattern in the path, as dataset can be split over the two product output1 and output2, and can also be in output !!
     - basic algo using get_datasets() method
     - also see PROC0005
    """
    with session.create():
        for d in dao.get_datasets():
            datasetVersions = dao_operations.get_dataset_versions(d, True)  # retrieves all the versions of the dataset
            if not datasetVersions.ismostrecentversionnumber(d.version):
                print(d.get_full_local_path('output{,1,2}'))


def PROC0005():
    """Print obsolete datasets versions.

    notes
     - for CMIP5 like DRS based projects, use shell expansion pattern in the
       path, as dataset can be split over the two product output1 and
       output2, and can also be in output !!
     - smart algo using get_old_versions_datasets() method
     - also see PROC0001
    """
    for d in dao_operations.get_old_versions_datasets():
        print(d.get_full_local_path(
            'output{,1,2}'))  # note: for non CMIP5-DRS-based-project, product argument is not used


def print_running_transfers():
    li = []
    with session.create():
        for tr in dao.get_files(status=sdconst.TRANSFER_STATUS_RUNNING):
            current_size = os.path.getsize(tr.get_full_local_path()) if os.path.isfile(tr.get_full_local_path()) else 0
            li.append([humanize.naturalsize(current_size, gnu=False), humanize.naturalsize(tr.size, gnu=False),
                       tr.start_date, tr.filename])

    if len(li) > 0:
        print(tabulate(li, headers=['Current size', 'Total size', 'Download start date', 'Filename'], tablefmt="plain"))
    else:
        print('No current download')


def print_old_versions_stats():
    """Print stats regarding old versions."""
    total_size = 0
    total_files = 0
    total_datasets = 0

    for d in dao_operations.get_old_versions_datasets():
        ds_info = dao_operations.get_dataset_stats(d)
        total_size += ds_info['size'][sdconst.TRANSFER_STATUS_DONE]
        total_files += ds_info['count'][sdconst.TRANSFER_STATUS_DONE]
        total_datasets += 1

        SDProgressDot.print_char(".")
    print("")

    sdlog.info("SDREPORT-433", "datasets old versions total size: %s" % humanize.naturalsize(total_size, gnu=False),
               stdout=True)
    sdlog.info("SDREPORT-434", "datasets old versions total files: %s" % total_files, stdout=True)
    sdlog.info("SDREPORT-435", "total old versions datasets: %s" % total_datasets, stdout=True)


def PROC0010():
    """List selection's files size."""
    selections_total_size = []

    # retrieve
    for us in getselections():
        total_size = getselectiontotalsize(us)
        selections_total_size.append((total_size, us))
        SDProgressDot.print_char(".")
    print

    # sort by size
    selections_total_size = sorted(selections_total_size, key=lambda selection_total_size: selection_total_size[0])

    # display
    for selection_total_size in selections_total_size:
        print("%-50s %20s" % (
            selection_total_size[1].filename, humanize.naturalsize(selection_total_size[0], gnu=False),))


def PROC0016():
    """
    list selection's files
    """
    selections_files_list = []

    # retrieve
    for us in getselections():
        selections_files_list = getselectionfileslist(us)

        # display
        print("Files list for '%s':" % us.filename)
        for f in selections_files_list:
            print("%-100s" % (f,))
