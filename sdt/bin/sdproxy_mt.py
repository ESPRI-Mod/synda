#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module runs many searches (SearchAPIProxy.run()) in parallel."""

import Queue
import sdapp
import threading
import random
import time
import traceback
import sdlog
from sdproxy import SearchAPIProxy
from sdtypes import File
from sdexception import SDException
import sdindex
import sdconst
import sdconfig
import sdsquery
import sdtools

class MetadataThread(threading.Thread):
    def __init__(self,host,service,query,result_queue,error_queue):
        self.host=host                 # index
        self.service=service           # search-API service (SearchAPIProxy object)
        self.query=query               # query
        self.result_queue=result_queue # output queue (global thread-safe Queue PTR)
        self.error_queue=error_queue   # error queue used by the retry mecanism (global thread-safe Queue PTR)

        threading.Thread.__init__(self)

    def run(self):
        """
        Note
          Better put Response object in ThreadSafe object (i.e. in queue not in files list)
        """
        ap=self.query.get('attached_parameters',{})

        try:
            url_with_host_set=self.query['url'].replace(sdconst.IDXHOSTMARK,self.host)

            #sdlog.debug("SDPROXMT-012","Using %s"%self.host,stderr=False,logfile=True)



            # BEWARE: printing stuff on stdxxx is NOT welcome here, as we are
            # here running inside a progress bar... so printing on stdxxx
            # result in a big mess. Maybe enable verbose mode here only if
            # progress is off, or just output to logfile....
            # Well, in fact, maybe the better is to move the progress here,
            # (i.e. as the slow part is the remote call, let's have the progress
            # close to it, not far upstream !).
            """
            verbose=sdsquery.get_scalar(self.query,'verbose',default=False,type_=bool) # we cast here as verbose can be str (set from parameter) or bool (set from '-v' option)
            if verbose:
                sdtools.print_stderr("Using %s"%self.host)
            """


            result=self.service.run(url=url_with_host_set,attached_parameters=ap) # service is an instance of SearchAPIProxy
            self.result_queue.put(result) # 'result' is a return Response object
        except Exception, e:
            # note
            #  - it's not fatal to come here, because error queries will be
            #    retried later using a different host (well until "max_retry"
            #    is reached of course)

            self.error_queue.put(self.query)

            # not needed to log here as already done by 'SYDPROXY-400' and 'SYDPROXY-410'
            #sdlog.info("SDPROXMT-001", "Query failed (url=%s)"%(url_with_host_set,))
            #sdlog.info("SDPROXMT-006", "%s"%(str(e)),)

            # debug
            #traceback.print_exc(file=open(sdconfig.stacktrace_log_file,"a"))

def run(i__queries):
    """
    Notes
        - this method contains the retry mecanism
        - return files list
    """

    # check
    for q in i__queries:
        if sdconst.IDXHOSTMARK not in q['url']:
            raise SDException('SDPROXMT-044','Incorrect query: host must not be set at this step')

    # retry loop
    max_retry=6
    i=0
    results=[]
    l__queries=i__queries
    while i < max_retry:

        (successes,errors)=run_helper(l__queries)

        # add OK results
        for r in successes:
            results.append(r)

        if len(errors)>0:
            sdlog.info("SDPROXMT-082","%d search-API queries failed"%(len(errors),))
            sdlog.info("SDPROXMT-083","retry 'failed search-API queries'")
            l__queries=errors

            i+=1

            continue

        else:

            if i>0:
                sdlog.info("SDPROXMT-089","retry succeeded")

            break



    if len(errors)>0:
        sdlog.error("SDPROXMT-084","max retry iteration reached. %d queries did not succeed"%(len(errors),))

    return results # result is a files list

def start_new_thread(host,url):
    sdlog.debug("SDPROXMT-002","Starting new search-API thread (%s)"%host)

    service=searchAPIServices[host]["iSearchAPIProxy"]

    th=MetadataThread(host,service,url,__result_queue,__error_queue)
    th.setDaemon(True)
    th.start()

    return th

def all_threads_completed():
    """
    Returns:
      True   => all threads completed
      False  => threads still running
    """
    for host in searchAPIServices.keys():
        for t in searchAPIServices[host]['threadlist']:
            if t.is_alive():
                return False

    return True

def process_query(host,query):
    """
    return 
      True   => query processed
      False  => query not processed (host is busy)
    """

    if len(searchAPIServices[host]['threadlist'])<max_thread_per_host:

        searchAPIServices[host]['threadlist'].append(start_new_thread(host,query))

        return True
    else:

        return False

def distribute_queries(queries):

    hosts=searchAPIServices.keys()

    random.shuffle(hosts) # this is to prevent always starting with the same server

    for host in hosts:

        if len(queries)<1:

            break

        else:

            query=queries.pop()

            status=process_query(host,query)

            if not status:
                # host is busy (thread is running on the host)
                # so we send back query in the stack

                queries.append(query)

def run_helper(queries):
    """
    notes
      - "queries" is non-threadsafe (i.e. not a Queue), but doesn't matter as threads do not use it
    """
    total_files=[]

    total_query_to_process=len(queries)

    sdlog.debug("SDPROXMT-003","%d search-API queries to process (max_thread_per_host=%d,timeout=%d)"%(total_query_to_process,max_thread_per_host,sdconst.SEARCH_API_HTTP_TIMEOUT))

    while True:
        if sdconfig.proxymt_progress_stat:
            sdlog.info("SDPROXMT-033","threads per host: %s"%",".join(['%s=%s'%(host,len(searchAPIServices[host]['threadlist'])) for host in searchAPIServices.keys()]))

        if len(queries)>0:
            distribute_queries(queries)
        else:
            # leave the loop only if all threads completed
            if all_threads_completed():
                break

        # remove completed threads from list
        for host in searchAPIServices.keys():
            li=[]
            for t in searchAPIServices[host]['threadlist']:
                if t.is_alive():
                    li.append(t)
            searchAPIServices[host]['threadlist']=li

        # log
        total_query_already_processed = total_query_to_process - len(queries)
        if total_query_to_process > 0: # display progress only when there are a lot of queries
            if len(queries) > 0: # display progress only when still query to process
                sdlog.info("SDPROXMT-004","total_queries=%d, running_or_done_queries=%d, waiting_queries=%d"%(total_query_to_process,total_query_already_processed,len(queries)))

        # if all services are busy, we sleep to limit loop speed
        # (note that all the code around the "sleep" call is to detect system overload)
        sleep_time=10
        warning_threshold=5 # threshold not to emit warning for every small load exceedance
        befo=time.time()
        time.sleep(sleep_time)
        afte=time.time()
        diff=afte-befo
        if diff>sleep_time+warning_threshold:
            sdlog.warning("SDPROXMT-005","WARNING: system overload detected (sleep takes %d second to complete)."%diff)

    # retrieve result from output queue
    while not __result_queue.empty():


        result=__result_queue.get(False) # retrieve files from ONE search-API call

        for f in result.files: # move from 'Response' object to files list
            total_files.append(f)

    # retrieve error from output queue and insert them into a list
    errors=[]
    while not __error_queue.empty():
        query=__error_queue.get(False)
        errors.append(query)

    return (total_files,errors)

def set_index_hosts(index_hosts):
    global searchAPIServices

    searchAPIServices={}
    for index_host in index_hosts:
        searchAPIServices[index_host]={}
        searchAPIServices[index_host]['iSearchAPIProxy']=SearchAPIProxy() # contains service PTR
        searchAPIServices[index_host]['threadlist']=[]                    # contains threads PTR

# module init

max_thread_per_host=sdconfig.max_metadata_parallel_download_per_index

__result_queue=Queue.Queue() # thread safe data structure to hold search-API result
__error_queue=Queue.Queue()  # thread safe data structure to hold unsuccessful request (used by the retry mecanism)

searchAPIServices=None # list of search-API services (M queries will be sent to one service at once, resulting in MxN parallel streams, with N the number of service)

set_index_hosts(sdindex.index_host_list)

if __name__ == '__main__':
    url="http://%s/esg-search/search?fields=*&realm=atmos&project=CMIP5&time_frequency=mon&experiment=rcp26&variable=tasmin&model=CNRM-CM5&model=CSIRO-Mk3-6-0&model=BCC-CSM1-1-m&ensemble=r1i1p1&type=File"%sdconst.IDXHOSTMARK
    queries=[{'url':url}]
    files=run(queries)

    # dict to "File" operation
    file_list=[]
    for file_ in files:
        file_list.append(File(**file_))

    for f in file_list:
        print "%s %s"%(f.timestamp,f.id)
