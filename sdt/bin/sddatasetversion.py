#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains dataset versions management code."""

import argparse
import re
import sdtypes
import sdapp
import sdmath
from sdexception import SDException,MixedVersionFormatException,IncorrectVTCException,IncorrectVersionFormatException

_VERSION_FORMAT_SHORT='short' # e.g. 'v1'
_VERSION_FORMAT_LONG='long' # e.g. '20120101'
_VERSION_FORMAT_LONG_WITH_PREFIX='long_with_prefix' # e.g. 'v20120101'

class DatasetVersion():
    """Dataset version object"""

    # FIXME we distinguish between versions like 20160618 or 20160619 and
    # versions like 1 or 2. 
    # If a data set goes from 1 to 20160618 we see it as an error for now.
    # May change in the future (it may be handled as long as it doesn't go back to 3 for the next version. TBC)

    # FIXME If there is any overlap between those formats, the least selective
    # ones must come last. 
    # For example, if /\d+/ came before /\d{8}/,
    # which_format() would identify 20160618
    # as matching /\d+/ instead of /\d{8}/.

    _dataset_version_regexp_strings=[
        #r'^v(\d{8})$',
        r'^v(\d+)$',
        #r'^(\d{8})$',
        r'^(\d+)$',
    ]

    _dataset_version_regexps = map(lambda s: re.compile(s, re.IGNORECASE), _dataset_version_regexp_strings);

    def __init__(self, version):
        self.version = version
        self._version_formats = None

    def get_version(self):
        return self.version

    def analyse(self):
        """Analyse a version string, identifying the format in which it is and
           extracting a version number (an integer) for comparing it to other
           versions. Returns the number of the regexp it matches and the
           version number or (None, None) if it matches none.
        """
        for n, re in enumerate(self._dataset_version_regexps):
            #print 'n = %d, re = "%s", self.version = "%s"' % (n, re, self.version)
            match = re.match(self.version)
            if match:
                vernum = long(match.group(0)) + 0
                vernum_str = '%s' % vernum
                if (vernum_str != match.group(0)):  # Not supposed to happen
                    raise SDException("SDDATVER-006", 'Unexpected error while extracting version number from version string "%s" with regexp "%s": capture "%s" converts to "%s"' % (self.version, self._dataset_version_regexp_strings[n], match.group(0), vernum_str))
                return n, vernum

        return None, None

class DatasetVersions():
    """Manage dataset version.

    Note
        This class contains all different versions of the same dataset (contains a list of Dataset object, one for each version)
    """
    _dataset_versions=None # contains Dataset objects

    def __init__(self):
        self._dataset_versions=[]

    def add_dataset_version(self,d):
        self._dataset_versions.append(d)

    def get_datasets(self):
        return self._dataset_versions

    def count(self):
        return len(self._dataset_versions)

    def exists_version_with_latest_flag_set_to_true(self):
        for d in self._dataset_versions:
            if d.latest:
                return True

        return False

    def is_version_higher_than_latest(self,i__d):
        """ returns true if i__d version is higher than the version with latest flag set, else returns false """
        return self.compare(i__d,self.get_dataset_with_latest_flag_set())

    def get_dataset_with_latest_flag_set(self):
        for d in self._dataset_versions:
            if d.latest:
                return d

        raise SDException("SDDATVER-001","fatal error")

    def is_most_recent_version_number(self,i__d):
        """Is i__d version the latest one.

        Note
            This method do not use the latest flag (computes from scratch)

        TODO
            Maybe rewrite this method to be based on get_latest_dataset() method (so to remove duplicate code)
        """

        # initialise with the first dataset's (may be any dataset)
        last_version=self._dataset_versions[0]

        for d in self._dataset_versions:
            if self.compare(d,last_version):
                last_version=d

        if last_version.version == i__d.version:
            return True
        else:
            return False

    def get_latest_dataset(self):
        """Return the latest dataset.

        Note
            This method do not use the latest flag (computes from scratch)
        """

        # initialise with the first dataset's (may be any dataset)
        latest_dataset=self._dataset_versions[0]

        for d in self._dataset_versions:
            if self.compare(d,latest_dataset):
                latest_dataset=d

        return latest_dataset

    def get_oldest_dataset(self):
        """Returns the oldest dataset."""

        # initialise with the first dataset's (may be any dataset)
        oldest_dataset=self._dataset_versions[0]

        for d in self._dataset_versions:
            if not self.compare(d,oldest_dataset):
                oldest_dataset=d

        return oldest_dataset

    def compare(self,d_a,d_b):
        """Returns true if d_a is more recent (higher in most case) than d_b, else false.

        Samples
            d_a.version => v20110901
            d_b.version => v1
        """
        if len(d_a.version)!=len(d_b.version):

            if d_a.timestamp is not None and d_b.timestamp is not None:

                if d_a.timestamp > d_b.timestamp:
                    return True
                else:
                    return False

            else:
                # As some dataset don't have the timestamp set (e.g. obs4MIPs.PCMDI.CloudSat.mon.v1)
                # we need to fallback to the emergency solution below.




                # In some cases, dataset's timestamp cannot be set (can be
                # because the dataset version doesn't exist anymore in ESGF, or
                # because the timestamp doesn't exist for some dataset as well
                # as for dataset's file). For such cases, we use the old
                # comparaison method.
                #
                if len(d_a.version)==9 and len(d_b.version)==2:
                    return True
                elif len(d_a.version)==2 and len(d_b.version)==9:
                    return False
                else:
                    raise SDException("SDDATVER-002","Incorrect version number (%s,%s)"%(d_a.version,d_b.version))


                # To raise exception instead, uncomment line below
                #raise SDException("SDDATVER-003","Incorrect timestamp (%s,%s,%s,%s)"%(d_a.dataset_functional_id,d_b.dataset_functional_id,d_a.timestamp,d_b.timestamp))


        else:
            return d_a.version > d_b.version

    def is_short_version_format(self,version):
        if len(version)==2:
            return True
        else:
            return False

    def is_long_version_format(self,version):
        if len(version)==8:
            return True
        else:
            return False

    def is_long_version_with_prefix_format(self,version):
        if len(version)==9:
            return True
        else:
            return False

    def get_dataset_versions_SORT_BY_VERSION(self):
        dataset_versions=sorted(self._dataset_versions, key=lambda dataset_version: dataset_version.version)
        return dataset_versions

    def get_sorted_versions(self):
        li=self.get_versions()
        return sorted(li)

    def get_versions(self):
        return [d.version for d in self._dataset_versions]
