#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

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
    buf="""  dataset_version
    synda check dataset_version [search_parameter ...] checks the
    correctness and consistency of dataset version numbers in all dataset
    versions (or, if search parameters are given, those that match those
    parameters).

    The first check consists in verifying that version numbers are
    syntactically valid. The "version" field is deemed valid if it matches
    (case-insensitively) the Python regular expression /^(\d+)$/ or, as an
    extension, /^v(\d+)$/. A missing "version" field is the same as a
    "version" field set to "0".

    The second check only applies to datasets which have more than one
    version. It consists in verifying that all the versions of a dataset
    have unique version numbers. An integral version number is extracted
    from the value of each "version" field by converting the string
    matched by the capture group in the regular expressions above to an
    integer. For example, a "version" field set to "20160101" would match
    regexp /^(\d+)$/ therefore the version number would be 20160101. There
    must be no duplicated version numbers in all the versions of a
    dataset. Note that this test is more stringent than merely checking
    for duplicated "version" fields : a dataset with two versions having
    "version" fields set to "1" and "01" respectively would not pass
    because both have version number 1.

    If all the versions of a dataset have a "timestamp" field, a third
    check is done. The versions of a dataset are sorted by time stamp and
    the sequence numbers are examined. Gaps in the sequence are accepted
    but the numbers must be increasing. For example, this dataset would
    pass :

                           timestamp             version
                           2016-01-01T00:00:00Z  1
                           2016-01-02T00:00:00Z  20160102

    but this one would not :

                           timestamp             version
                           2016-01-01T00:00:00Z  20160101
                           2016-01-02T00:00:00Z  2

    By default, the report is in plain text format and is written to standard
    output. The pdf format can be used instead through the use of
    '--output_format' option.
    
    The report comprises four parts :

    - A header which gives the date and time of execution and the Synda
      command line.

    - For every dataset with errors, the name of the dataset and, for each
      of its versions, the "timestamp" and "version" fields along with a
      list of the errors found in this dataset version, if any.

    - Statistics :
      - the number of dataset versions found
      - ... with a "timestamp" field
      - ... without a "timestamp" field
      - the number of datasets found
      - ... with a "timestamp" field on all  of their versions
      - ... with a "timestamp" field on some of their versions
      - ... with a "timestamp" field on none of their versions

    - For each type of error,
      - a detailed description of the error,
      - the number of dataset versions in which it was found,
      - the number of datasets to which it applies, ie datasets with at
        least one version having in error.
  file_variable
    list files having more than one variable
  selection
    check if selection files parameters are valid
"""
    return buf
