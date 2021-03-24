#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains subcommands description text.
"""


def check():

    buf = ("  dataset_version\n"
           "    synda check dataset_version [search_parameter ...] checks the\n"
           "    correctness and consistency of dataset version numbers in all dataset\n"
           "    versions (or, if search parameters are given, those that match those\n"
           "    parameters).\n"
           "\n"
           "    The first check consists in verifying that version numbers are\n"
           "    syntactically valid. The \"version\" field is deemed valid if it matches\n"
           "    (case-insensitively) the Python regular expression r/^(\\d+)$/ or, as an\n"
           "    extension, r/^v(\\d+)$/. A missing \"version\" field is the same as a\n"
           "    \"version\" field set to \"0\".\n"
           "\n"
           "    The second check only applies to datasets which have more than one\n"
           "    version. It consists in verifying that all the versions of a dataset\n"
           "    have unique version numbers. An integral version number is extracted\n"
           "    from the value of each \"version\" field by converting the string\n"
           "    matched by the capture group in the regular expressions above to an\n"
           "    integer. For example, a \"version\" field set to \"20160101\" would match\n"
           "    regexp /^(\\d+)$/ therefore the version number would be 20160101. There\n"
           "    must be no duplicated version numbers in all the versions of a\n"
           "    dataset. Note that this test is more stringent than merely checking\n"
           "    for duplicated \"version\" fields : a dataset with two versions having\n"
           "    \"version\" fields set to \"1\" and \"01\" respectively would not pass\n"
           "    because both have version number 1.\n"
           "\n"
           "    If all the versions of a dataset have a \"timestamp\" field, a third\n"
           "    check is done. The versions of a dataset are sorted by time stamp and\n"
           "    the sequence numbers are examined. Gaps in the sequence are accepted\n"
           "    but the numbers must be increasing. For example, this dataset would\n"
           "    pass :\n"
           "\n"
           "                           timestamp             version\n"
           "                           2016-01-01T00:00:00Z  1\n"
           "                           2016-01-02T00:00:00Z  20160102\n"
           "\n"
           "    but this one would not :\n"
           "\n"
           "                           timestamp             version\n"
           "                           2016-01-01T00:00:00Z  20160101\n"
           "                           2016-01-02T00:00:00Z  2\n"
           "\n"
           "    By default, the report is in plain text format and is written to standard\n"
           "    output. The pdf format can be used instead through the use of\n"
           "    '--output_format' option.\n"
           "    \n"
           "    The report comprises four parts :\n"
           "\n"
           "    - A header which gives the date and time of execution and the Synda\n"
           "      command line.\n"
           "\n"
           "    - For every dataset with errors, the name of the dataset and, for each\n"
           "      of its versions, the \"timestamp\" and \"version\" fields along with a\n"
           "      list of the errors found in this dataset version, if any.\n"
           "\n"
           "    - Statistics :\n"
           "      - the number of dataset versions found\n"
           "      - ... with a \"timestamp\" field\n"
           "      - ... without a \"timestamp\" field\n"
           "      - the number of datasets found\n"
           "      - ... with a \"timestamp\" field on all  of their versions\n"
           "      - ... with a \"timestamp\" field on some of their versions\n"
           "      - ... with a \"timestamp\" field on none of their versions\n"
           "\n"
           "    - For each type of error,\n"
           "      - a detailed description of the error,\n"
           "      - the number of dataset versions in which it was found,\n"
           "      - the number of datasets to which it applies, ie datasets with at\n"
           "        least one version having in error.\n"
           "  file_variable\n"
           "    list files having more than one variable\n"
           "  selection\n"
           "    check if selection files parameters are valid\n")
    return buf
