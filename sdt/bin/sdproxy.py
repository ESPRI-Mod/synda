#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains search-api proxy."""

import time
import argparse
import sdapp
import sdtypes
from sdexception import SDException
from sdtime import SDTimer
import sdnetutils
import sdconst
import sdlog
import sdtools
import sdconfig
import sdaddap
import sdurlutils

# not a singleton
class SearchAPIProxy():
    def __init__(self,**kw):
        pass

    def run(self,url=None,attached_parameters=None):
        """Execute one search query (as pagination is used, it can result in many HTTP queries)."""

        if attached_parameters is None:
            attached_parameters={}

        request=sdtypes.Request(url=url,pagination=True)
        final_url=request.get_url()

        sdlog.debug("SYDPROXY-490","paginated call started (url=%s)"%final_url)

        try:
            paginated_response=self.call_web_service__PAGINATION(request)
        except Exception,e:
            sdlog.error("SYDPROXY-400","Error occurs during search-API paginated call (url=%s)"%(final_url,))
            sdlog.error("SYDPROXY-410","%s"%(str(e),))
            raise

        sdlog.debug("SYDPROXY-001","paginated call completed (call-duration=%i, files-count=%i, url=%s)"%(paginated_response.call_duration, paginated_response.count(), final_url))

        if attached_parameters.get('verbose',False) == True:
            sdtools.print_stderr("Url: %s"%final_url)
            sdtools.print_stderr("Duration: %s"%paginated_response.call_duration)
            sdtools.print_stderr("")

        md=paginated_response.to_metadata() # we cast to remove pagination related code and have a lighter object

        md=sdaddap.run(md,attached_parameters)

        return md

    def call_web_service(self,request):

        sdlog.debug("SYDPROXY-100","Search-API call started (%s)."%request.get_url())

        try:
            response=sdnetutils.call_web_service(request.get_url(),timeout=sdconst.SEARCH_API_HTTP_TIMEOUT) # returns Response object
        except:

            # if exception occurs in sdnetutils.call_web_service() method, all
            # previous calls to this method inside this paginated call are also
            # cancelled

            # we reset the offset so the paginated call can be restarted from the begining the next time
            # (maybe overkill as offset is reinitialized when entering 'call_web_service__PAGINATION()' func)
            request.offset=0

            raise

        sdlog.info("SYDPROXY-100","Search-API call completed (returned-files-count=%i,match-count=%i,url=%s)."%(response.count(),response.num_found,request.get_url()))

        return response

    def call_web_service__RETRY(self,request):
        """Add mono-host retry to call_web_service() method.

        Notes
            - multi-host retry is available via sdproxy_mt module.
            - when using sdproxy_mt module, this retry is normally not necessary,
              except for one case: it's when one wants to dump huge amount of data from ESGF
              (i.e. not 10 000, but something more like 1 000 000). In this case,
              probability for a failure inside one pagination call is big (because one
              pagination call is composed of many sub calls (i.e. not just 2 or 3)).
        """
        max_retry=3

        i=0
        while True:
            if i>0:
                sdlog.info("SYDPROXY-088","Retry search-API call (%s)."%request.get_url())

            try:
                response=self.call_web_service(request)
                break
            except:
                sdlog.info("SYDPROXY-090","Search-API call failed (%s)."%request.get_url())

                if i>=max_retry:
                    sdlog.info("SYDPROXY-092","Maximum number of retry attempts reached: cancel pagination call (%s)."%request.get_url())
                    raise
                else:
                    i+=1

        return response

    def call_web_service__PAGINATION(self,request):
        """
        Notes
            This function contain paging management (i.e. make web service calls until all results are returned)
        """

        # init
        request.limit=sdconst.SEARCH_API_CHUNKSIZE
        request.offset=0
        offset = 0
        paginated_response=sdtypes.PaginatedResponse()
        nread = 0 # how many already read
        moredata = True

        while moredata: # paging loop

            # paging (pre-processing)
            request.offset=offset

            # call
            if sdconfig.mono_host_retry:
                response=self.call_web_service__RETRY(request)
            else:
                response=self.call_web_service(request)

            # paging (post-processing)
            offset += sdconst.SEARCH_API_CHUNKSIZE
            nread += response.count()
            nleft = response.num_found - nread

            moredata = (nleft>0) and (response.count()>0) # the second member is for the case when "num_found > 0" but nothing is returned

            paginated_response.slurp(response) # warning: response is modified here

        return paginated_response

if __name__ == '__main__':

    url="http://esgf-data.dkrz.de/esg-search/search?fields=*&realm=atmos&project=CMIP5&time_frequency=mon&experiment=rcp26&variable=tasmin&model=CNRM-CM5&model=CSIRO-Mk3-6-0&model=BCC-CSM1-1-m&ensemble=r1i1p1&type=File"

    url=sdurlutils.add_solr_output_format(url)

    search=SearchAPIProxy()
    result=search.run(url=url)

    # dict to "File" operation
    file_list=[]
    for file_ in result.get_files():
        file_list.append(sdtypes.File(**file_))

    for f in file_list:
        print "%s %s"%(f.timestamp,f.id)
