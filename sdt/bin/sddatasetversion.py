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

import sdapp
import sdmath
from sdexception import SDException,MixedVersionFormatException,IncorrectVTCException

_VERSION_FORMAT_SHORT='short' # e.g. 'v1'
_VERSION_FORMAT_LONG='long' # e.g. '20120101'
_VERSION_FORMAT_LONG_WITH_PREFIX='long_with_prefix' # e.g. 'v20120101'

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

    def version_format_check(self):
        """Verify version format regularity."""

        version_formats=[]
        for d in self._dataset_versions:
            if self.is_short_version_format(d.version):
                version_formats.append(_VERSION_FORMAT_SHORT)
            elif self.is_long_version_format(d.version):
                version_formats.append(_VERSION_FORMAT_LONG)
            elif self.is_long_version_with_prefix_format(d.version):
                version_formats.append(_VERSION_FORMAT_LONG_WITH_PREFIX)
            else:
                raise SDException('SDDATVER-004','Incorrect version format (%s)'%d.version)

        if len(version_formats)!=1: # only one version format must be use for a dataset (i.e. short and long format should not be mixed)
            raise MixedVersionFormatException('SDDATVER-005','Mixed version format')

    def version_and_timestamp_correlation_check(self):
        """Verify that timestamp monotonicity follows version monotonicity
        (i.e. if version increase, timestamp must increase too)."""

        # debug
        #print self.get_sorted_versions()
        #print self.get_dataset_versions_SORT_BY_VERSION()

        li=[]
        for d in self.get_dataset_versions_SORT_BY_VERSION():
            
            # debug
            #print d.version

            li.append(d.version)

        if not sdmath.monotone_increasing(li):
            raise IncorrectVTCException()

    def version_consistency_check(self):

        assert len(self._dataset_versions)>0

        try:
            self.version_format_check()
        except MixedVersionFormatException,e:
            raise
        except:
            raise

        try:
            self.version_and_timestamp_correlation_check()
        except IncorrectVTCException,e:
            raise
        except:
            raise
