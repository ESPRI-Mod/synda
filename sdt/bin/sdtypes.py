#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains core classes.

Note
    This module contains only instantiable classes (i.e. no static class)
"""

import sys
import traceback
import re
import copy
import sdapp
import sdconfig
import sdconst
import sdtools
import json
from sdexception import SDException

class Variable():
    def __init__(self,**kwargs):
        self.__dict__.update( kwargs )

class Event():
    def __init__(self,**kwargs):
        self.status=sdconst.EVENT_STATUS_NEW
        self.__dict__.update( kwargs )
    def __str__(self):
        return self.name

class DatasetVersions():
    """Manage dataset version.

    notes
     contains all different versions of the same dataset (contains a list of Dataset object, one for each version)
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
        Returns
            dataset
        """
        for d in self._dataset_versions:
            if d.latest:
                return d

        raise SDException("SDATYPES-032","fatal error")

    def get_dataset_with_latest_flag_set(self):
        for d in self._dataset_versions:
            if d.latest:
                return d

        raise SDException("SDATYPES-044","fatal error")

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
                    raise SDException("SDATYPES-092","Incorrect version number (%s,%s)"%(d_a.version,d_b.version))


                # To raise exception instead, uncomment line below
                #raise SDException("SDATYPES-600","Incorrect timestmap (%s,%s,%s,%s)"%(d_a.dataset_functional_id,d_b.dataset_functional_id,d_a.timestamp,d_b.timestamp))


        else:
            return d_a.version > d_b.version

class Buffer():
    def __init__(self,**kw):

        # outer attributes
        self.filename=kw['filename'] # filename
        self.path=kw['path']         # file path (including filename)

        # inner attributes
        self.lines=kw.get('lines',[])

    def __str__(self):
        return ",".join(['%s=%s'%(k,str(v)) for (k,v) in self.__dict__.iteritems()])

class Selection():
    def __init__(self,**kw):
        self.childs=[]                                     # sub-selections list (a selection can contain facets groups, but can also contain other selections)
        self.parent=None                                   # parent selection (a selection can be the parent of another selection (e.g. default selection is the parent of project default selection))

        # inner attributes        
        self.facets=kw.get("facets",{})                    # contains search-API facets

        # outer attributes        
        self.filename=kw.get("filename")                   # selection filename
        self.path=kw.get("path")                           # selection file path (fullpath)
        self.selection_id=kw.get("selection_id")           # database identifier
        self.checksum=kw.get("checksum")
        self.status=kw.get("status")

    def __str__(self):
        return "filename=%s\nfacets=%s"%(self.filename,self.facets)

    def get_root(self):
        """
        Returns
            top level selection (i.e. default selection)
        """
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()

    def merge_facets(self):
        """This func merge facets starting from root level."""
        return self.get_root().merge_facets_downstream()

    def to_stream(self):
        """Alias."""
        return self.merge_facets()

    def merge_facets_downstream(self):
        """Merge and return facets corresponding to this selection

        This func merge facets of this selection and all descendant selections,
        down the selections tree.

        Returns 
            facets_groups (List)

        note
            recursive func
        """

        if len(self.childs)>0:
            # processes sub-selection (Synchro-data specific realm&freq&vars lines (e.g. variables[atmos][mon]="tas psl")).
            #
            # notes
            #  - if some facets exist in both place (in sub-selection and in main selection),
            #    sub-selection ones override main selection ones (in update() method below)
            #  - a new query (aka facets group) is created for each line.
            #  - we can't retrieve all frequencies/realms in one search-API call because variables are grouped by realm/frequency..



            # beware: tricky code
            # 
            # we need to recursively override parent parameters with child
            # parameter.  so we need create a copy of parent facets (and then
            # update it with child facets), for each child and for each facets
            # group.
            #
            facets_groups=[]
            for s in self.childs:
                for facets_group in s.merge_facets_downstream():

                    cpy=copy.deepcopy(self.facets)
                    cpy.update(facets_group)

                    facets_groups.append(cpy)

            return facets_groups

        else:
            # this loop processes main selection facets
            return [self.facets]

class File():
    def __init__(self,**kwargs):
        self.__dict__.update( kwargs )

    def get_full_local_path(self):
        return "%s/%s"%(sdconfig.data_folder,self.local_path)

    def __str__(self):
        if self.status==sdconst.TRANSFER_STATUS_ERROR:
            buf="sdget_status=%s,error_msg='%s',file_id=%d,status=%s,local_path=%s,url=%s" % (self.sdget_status,self.error_msg,self.file_id,self.status,self.get_full_local_path(),self.url)
        else:
            buf="file_id=%d,status=%s,local_path=%s,url=%s" % (self.file_id,self.status,self.get_full_local_path(),self.url)

        return buf

class Dataset():
    def __init__(self,**kw):
        self.__dict__.update(kw)

    def get_full_local_path(self):
        return "%s/%s"%(sdconfig.data_folder,self.local_path)

    def get_full_local_path_without_version(self):
        return re.sub('/[^/]+$','',self.get_full_local_path())

    def __str__(self):
            return "".join(['%s=%s\n'%(k,v) for (k,v) in self.__dict__.iteritems()])

class SessionParam():
    def __init__(self,name,type_=str,default_value=None,search_api_facet=True,value=None,removable=True,option=True):
        self.name=name
        self.type_=type_
        self.default_value=default_value
        self.search_api_facet=search_api_facet
        self.value=value
        self.removable=removable # not used for now
        self.option=option # this flag means 'is synchro-data specific option ?'

    def value_to_string(self):
        if self.value is None:
            # we return '' if None whatever what type is

            return ''
        else:
            if self.type_==bool:
                return 'true' if self.value else 'false'
            elif self.type_==int:
                return str(self.value)
            elif self.type_==str:
                return self.value

    def set_value_from_string(self,v):
        if self.type_==bool:
            self.value=True if v=='true' else False
        elif self.type_==int:
            self.value=int(v)
        elif self.type_==str:
            self.value=v

    def __str__(self):
            return "".join(['%s=%s\n'%(k,v) for (k,v) in self.__dict__.iteritems()])

class Parameter():
    """Contain values for one parameter."""

    def __init__(self,values=None,name=None):
        self.values=values
        self.name=name

    def exists(self,value):
        """Check if parameter value exists."""
        if value in self.values:
            return True
        else:
            return False

    def __str__(self):
        return "%s=>%s"%(self.name,str(self.values))

class Item():
    """
    Note
        This class contains parameter value, but as each value can also contains sub-value (e.g. 'count'),
        it is named 'Item' for better clarity (instead of Value).
    """

    def __init__(self,name=None,count=None):
        self.name=name # parameter value name (i.e. different from parameter name)
        self.count=count # do NOT remove this attribute: it is used to count files/datasets for each parameter value

    def __str__(self):
        return ",".join(['%s=%s'%(k,str(v)) for (k,v) in self.__dict__.iteritems()])

class Request():
    def __init__(self,url=None,pagination=True):
        self._url=url
        self.pagination=pagination

        if self.pagination:
            if sdtools.url_contains_limit_keyword(self._url):
                raise SDException("SDATYPES-008","assert error (url=%s)"%self._url)

        self.offset=0
        self.limit=sdconst.CHUNKSIZE

    def get_limit_filter(self):
        if self.pagination:
            # pagination enabled

            return "&limit=%d"%self.limit
        else:
            # pagination disabled
            # (in this mode, limit can be set to reduce the number of returned result)

            if sdtools.url_contains_limit_keyword(self._url):
                return "" # return void here as already set in the url
            else:
                return "&limit=%d"%self.limit

    def get_offset_filter(self):
        return "&offset=%d"%self.offset

    def get_url(self):
        url="{0}{1}{2}".format(self._url,self.get_limit_filter(),self.get_offset_filter())

        if sdconst.IDXHOSTMARK in url:
            raise SDException('SDATYPES-004','host must be set at this step (url=%s)'%url)

        # check
        if len(url)>3500: # we limit buffer size as apache server doesnt support more than 4000 chars for HTTP GET buffer
            raise SDException("SDATYPES-003","url is too long (%i)"%len(url))

        return url

    def _serialize(self,paramName,values):
        """Serialize one parameter.

        Example
          input
            paramName="variable"
            values="tasmin,tasmax"
          output
            "&variable=tasmin&variable=tasmax"
        """
        l=[]
        for v in values:
            l.append(paramName+"="+v)

        if len(l)>0:
            return "&"+"&".join(l)
        else:
            return ""

    def __str__(self):
        return ",".join(['%s=%s'%(k,str(v)) for (k,v) in self.__dict__.iteritems()])

class Response():
    """Contains web service output after XML parsing."""

    def __init__(self,**kw):
        self.files=kw.get("files",[])                # File (key/value attribute based files list)
        self.num_found=kw.get("num_found",0)         # total match found in ESGF for the query
        self.num_result=kw.get("num_result",0)       # how many match returned, depending on "offset" and "limit" parameter
        self.call_duration=kw.get("call_duration")   # ESGF index service call duration (if call has been paginated, then this member contains sum of all calls duration)

        self.parameter_values=kw.get("parameter_values",[])        # parameters list (come from the XML document footer)

        # assert
        if self.num_found is None:
            raise SDException("SDATYPES-005","assert error")
        if self.num_result is None:
            raise SDException("SDATYPES-006","assert error")

    def add_attached_parameters(self,attached_parameters):
        """This func adds some parameters to the result of a query. 
        
        Notes
            - The idea is the keep some parameters around by making them jump
              over the search call (e.g. Search-api call, SQL call..), from
              'query pipeline' to 'file pipeline'.
        """
        assert isinstance(attached_parameters, dict)
        for f in self.files:
            assert 'attached_parameters' not in f
            f['attached_parameters']=copy.deepcopy(attached_parameters)

    def __str__(self):
        return "\n".join(['%s'%(f['id'],) for f in self.files])

# init.
