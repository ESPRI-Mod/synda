#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains core classes.

Note
    This module contains only instantiable classes (i.e. no static class)
"""

import os
import sys
import re
import copy
import json
import sdapp
import sdconfig
import sdmts
import sdconst
import sdtools
from sdexception import SDException

def build_full_local_path(local_path,prefix=sdconfig.data_folder):
    add_prefix=True

    if len(local_path)>0:
        if local_path[0]=='/':
            add_prefix=False

    if add_prefix:
        path=os.path.join(prefix,local_path)
    else:
        path=local_path

    return path

class Variable():
    def __init__(self,**kwargs):
        self.__dict__.update( kwargs )

class Event():
    def __init__(self,**kwargs):
        self.status=sdconst.EVENT_STATUS_NEW
        self.__dict__.update( kwargs )
    def __str__(self):
        return self.name

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
            # processes sub-selection (Synda specific realm&freq&vars lines (e.g. variables[atmos][mon]="tas psl")).
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

class BaseType():
    def get_full_local_path(self,prefix=sdconfig.data_folder):
        return build_full_local_path(self.local_path,prefix)

class File(BaseType):
    def __init__(self,**kwargs):
        self.__dict__.update( kwargs )

    def __str__(self):
        if self.status==sdconst.TRANSFER_STATUS_ERROR:
            buf="sdget_status=%s,sdget_error_msg=%s,error_msg='%s',file_id=%d,status=%s,local_path=%s,url=%s" % (self.sdget_status,self.sdget_error_msg,self.error_msg,self.file_id,self.status,self.get_full_local_path(),self.url)
        else:
            buf="file_id=%d,status=%s,local_path=%s,url=%s" % (self.file_id,self.status,self.get_full_local_path(),self.url)

        return buf

class Dataset(BaseType):
    def __init__(self,**kw):
        self.__dict__.update(kw)

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
        self.option=option # this flag means 'is Synda specific option ?'

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
    def __init__(self,url=None,pagination=True,limit=sdconst.SEARCH_API_CHUNKSIZE):
        self._url=url
        self.pagination=pagination

        if self.pagination:
            if sdtools.url_contains_limit_keyword(self._url):
                raise SDException("SDATYPES-008","assert error (url=%s)"%self._url)

        self.offset=0
        self.limit=limit

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

class CommonIO(object):
    """Abstract."""

    def __init__(self,*args,**kwargs):
        lowmem=kwargs.get('lowmem',sdconfig.lowmem)            # note that if store is not None, lowmem have no effect

        files=kwargs.get("files",None)
        store=kwargs.get('store',None)

        assert not (files is not None and store is not None)

        if files is not None:
            self.store=sdmts.get_new_store(lowmem)
            self.store.set_files(files)                        # Files (key/value attribute based files list)
            self.size=compute_total_size(files)
        elif store is not None:
            # passing 'store' as argument is only used for internal operation (e.g. copy)

            self.store=store
            self.size=kwargs.get('size',None)

            assert self.size is not None # size must be given if store is given
        else:
            self.store=sdmts.get_new_store(lowmem)
            self.size=0

    def __del__(self):
        """Destructor

        Calls 'delete' when object is garbage collected.
        """

        self.delete()

    def count(self):
        return self.store.count()

    def set_files(self,files):
        self.store.set_files(files)
        self.size=compute_total_size(files)

    def add_files(self,files):
        assert isinstance(files, list)
        self.store.append_files(files)
        self.size+=compute_total_size(files)

    def get_files(self): # warning: load list in memory
        return self.store.get_files()

    def get_chunks(self,io_mode=sdconst.PROCESSING_FETCH_MODE_GENERATOR):
        assert not isinstance(self.store,list)
        return self.store.get_chunks(io_mode)

    def delete(self):
        self.store.delete()

    def get_one_file(self):
        return self.store.get_one_file()

    def connect(self):
        self.store.connect()

    def disconnect(self):
        self.store.disconnect()

def compute_total_size(files):
    if len(files)>0:
        file_=files[0] # assume all items are of the same type

        # FIXME: remove this block
        if 'size' not in file_:
            return 0
        else:
            return sum(int(f['size']) for f in files)

        # FIXME: use this block instead
        # test with: synda search CMIP5 decadal1995 mon land
        """
        type_=file_.get('type')
        if type_=='Dataset':
            return 0
        elif type_=='File':
            return sum(int(f['size']) for f in files)
        else:
            raise SDException("SDATYPES-024","Incorrect type (type=%s)"%str(type_))
        """

    else:
        return 0

class ResponseIngester(object):
    """Abstract."""

    def slurp(self,response):
        assert isinstance(response,Response)
        self.store.append_files(response.get_files()) # get_files() here loads list in memory, but should work on lowmem machine as Response object never exceed SEARCH_API_CHUNKSIZE
        self.call_duration+=response.call_duration
        self.size+=response.size

class MetaResponse(CommonIO,ResponseIngester):
    """Abstract."""

    def __init__(self,*args,**kwargs):
        CommonIO.__init__(self,*args,**kwargs)
        self.call_duration=0

    def to_metadata(self):
        metadata=Metadata(store=self.store.copy(),size=self.size)
        return metadata

class Metadata(CommonIO):
    """Concrete."""

    def slurp(self,metadata):
        assert isinstance(metadata, Metadata)
        self.store.merge(metadata.store)
        self.size+=metadata.size

    def copy(self):
        cpy=Metadata(store=self.store.copy(),size=self.size)
        return cpy

class PaginatedResponse(MetaResponse):
    """Concrete."""

    pass

class MultiQueryResponse(MetaResponse):
    """Concrete."""

    pass

class Response(CommonIO):
    """Contains web service output after XML parsing.

    Note
        Concrete
    """

    def __init__(self,*args,**kwargs):
        CommonIO.__init__(self,*args,**kwargs)                         # call base class initializer

        self.num_found=kwargs.get("num_found",0)                       # total match found in ESGF for the query
        self.call_duration=kwargs.get("call_duration")                 # ESGF index service call duration (if call has been paginated, then this member contains sum of all calls duration)
        self.parameter_values=kwargs.get("parameter_values",[])        # parameters list (come from the XML document footer)

        # check

        if self.num_found is None:
            raise SDException("SDATYPES-005","assert error")

        if self.count()>sdconst.SEARCH_API_CHUNKSIZE:
            assert False

    def __str__(self):
        return "\n".join(['%s'%(f['id'],) for f in self.store.get_files()]) # warning load listin memory

# init.
