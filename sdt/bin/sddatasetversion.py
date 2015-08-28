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
from sdexception import SDException

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
        return self.compare(i__d,self.get_version_with_latest_flag_set())

    def get_version_with_latest_flag_set(self):
        """
        Description
            alias

        Returns
            dataset
        """
        return get_dataset_with_latest_flag_set()

    def get_dataset_with_latest_flag_set(self):
        for d in self._dataset_versions:
            if d.latest:
                return d

        raise SDException("SDDATVER-001","fatal error")

    def is_most_recent_version_number(self,i__d):
        """Is i__d version the latest one

        note
          this method is *NOT* related with the latest flag !! (it is just a version *NUMBER* comparison method)
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

    def compare(self,d_a,d_b):
        """Returns true if d_a is higher than d_b, else false.

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
