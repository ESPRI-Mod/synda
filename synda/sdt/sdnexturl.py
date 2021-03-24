#!/usr/share/python/synda/sdt/bin/python
#jfp was
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains next url routine."""
# multiple changes by JfP to make fallback more flexible.

import argparse
from synda.sdt import sdlog
from synda.sdt import sdquicksearch
from synda.sdt import sdexception
import sqlite3

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.db.models import Config as Db
from synda.source.config.api.constants import URL_FIELDS


def run(tr):
    """
    Returns
        True: url has been switched to a new one
        False: nothing changed (same url)
    """
    try:
        db_file = Db().get()

        conn = sqlite3.connect(
            db_file,
            Preferences().download_direct_db_timeout,
        )
        c = conn.cursor()
        c.execute("INSERT INTO failed_url(url,file_id) VALUES (?,"+
                  "(SELECT file_id FROM file WHERE file_functional_id=?))",
                  (tr.url, tr.file_functional_id) )
        conn.commit()
    except sqlite3.IntegrityError as e:
        # url,file_id is already in the failed_url table
        sdlog.info("SDNEXTUR-001","During database operations, IntegrityError %s on %s with new file_id=%s"
                   %(e,url,tr.file_id))
        conn.commit()
    except Exception as e:
        sdlog.info("SDNEXTUR-002","During database operations, unknown exception %s"%(e,))
        return False
    finally:
        c.close()

    try:
        next_url(tr,conn)
        return True
    except sdexception.FileNotFoundException as e:
        sdlog.info("SDNEXTUR-003","Cannot switch url for %s (FileNotFoundException)"%(tr.file_functional_id,))
        return False
    except sdexception.NextUrlNotFoundException as e:
        sdlog.info("SDNEXTUR-004","Cannot switch url for %s (NextUrlNotFoundException)"%(tr.file_functional_id,))
        return False
    except Exception as e:
        sdlog.info("SDNEXTUR-005","Unknown exception (file_functional_id=%s,exception=%s)"%(tr.file_functional_id,str(e)))
        conn.close()
        return False
    finally:
        conn.close()


def next_url(tr,conn):
    all_urlps=get_urls(tr.file_functional_id) # [[url1,protocol1],[url2,protocol2],...]
    sdlog.info("SDNEXTUR-006","all_urpls= %s"%(all_urlps,))
    c = conn.cursor()
    fus = c.execute("SELECT url FROM failed_url WHERE file_id="+
                  "(SELECT file_id FROM file WHERE file_functional_id=?)",
                    (tr.file_functional_id,))
    failed_urls = [fu[0] for fu in fus.fetchall()]
    sdlog.info("SDNEXTUR-007","failed_urls= %s"%(failed_urls,))
    urlps = [urlp for urlp in all_urlps if urlp[0] not in failed_urls]
    # ... Note that list comprehensions preserve order.
    urls = [urlp[0] for urlp in urlps]
    
    if len(urls)>0:
        old_url=tr.url
        new_url=urls[0]
        tr.url=new_url
        sdlog.info("SDNEXTUR-008","Url successfully switched (file_functional_id=%s,old_url=%s,new_url=%s)"%(tr.file_functional_id,old_url,new_url))
    else:
        sdlog.info("SDNEXTUR-009","Next url not found (file_functional_id=%s)"%(tr.file_functional_id,))
        raise sdexception.NextUrlNotFoundException()


def get_urls(file_functional_id):
    """returns a prioritized list of [url,protocol] where each url can supply the specified file"""

    try:
        result=sdquicksearch.run(
            parameter=['limit=4','fields=%s'%url_fields,'type=File','instance_id=%s'%
                       file_functional_id],
            post_pipeline_mode=None )
    except Exception as e:
        sdlog.debug("SDNEXTUR-010", "exception %s.  instance_id=%s"%(e,file_functional_id))
        raise e

    li=result.get_files()
    sdlog.info("SDNEXTUR-011","sdquicksearch returned %s sets of file urls: %s"%(len(li),li))
    if li==[]:
        # No urls found. Try again, but wildcard the file id. (That leads to a string search on all
        # fields for the wildcarded file id, rather than a match of the instance_id field only.)
        result=sdquicksearch.run(
            parameter=['limit=4','fields=%s'%url_fields,'type=File','instance_id=%s'%
                       file_functional_id+'*'],
            post_pipeline_mode=None )
        li=result.get_files()
        sdlog.info("SDNEXTUR-012","sdquicksearch 2nd call %s sets of file urls: %s"%(len(li),li))
    # result looks like
    # [ {protocol11:url11, protocol12:url12, attached_parameters:dict, score:number, type:'File',
    #    size:number} }, {[another dict of the same format}, {another dict},... ]
    # with no more than limit=4 items in the list, and no more than three protocols.  
    # We'll return something like urlps = [ [url1,protocol1], [url2,protocol2],... ]
    # The return value could be an empty list.
    # Note: These nested lists are ugly; it's just a quick way to code something up.

    urlps = []
    for dic in li:
        urlps += [ [dic[key],key] for key in dic.keys() if key.find('url_')>=0 and
                   dic[key].find('//None')<0 ]
        # ... protocol keys are one of 'url_http', 'url_gridftp'
        # The search for //None bypasses an issue with the SOLR lookup where there is no
        # url_gridftp possibility.

    return prioritize_urlps( urlps )


url_fields = ','.join(URL_FIELDS)  # used for the sdquicksearch call above


def prioritize_urlps( urlps ):
    """Orders a list urlps so that the highest-priority urls come first.  urlps is a list of
    lists of the form [url,protocol].  First, GridFTP urls are preferred over everything else.
    Then, prefer some data nodes over others."""
    def priprotocol(protocol):
        if protocol.find('gridftp')>0:  return 0
        if protocol.find('http')>0:     return 1
        return 2
    def priurl(url):
        if url.find('llnl')>0:  return 0
        if url.find('ceda')>0:  return 1
        if url.find('dkrz')>0:  return 2
        if url.find('ipsl')>0:  return 3
        if url.find('nci')>0:   return 4
        return 5
    return sorted( urlps, key=(lambda urlp: (priprotocol(urlp[1]), priurl(urlp[0]))) )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #file_functional_id='cmip5.output1.LASG-CESS.FGOALS-g2.decadal1985.day.atmos.day.r1i1p1.v1.va_day_FGOALS-g2_decadal1985_r1i1p1_19880101-19881231.nc'
    #file_functional_id='cmip5.output1.CMCC.CMCC-CMS.piControl.mon.atmos.Amon.r1i1p1.v20120717.pr_Amon_CMCC-CMS_piControl_r1i1p1_416401-417312.nc'
    file_functional_id='cmip5.output1.NOAA-GFDL.GFDL-CM2p1.historical.mon.atmos.Amon.r3i1p1.v20110601.cl_Amon_GFDL-CM2p1_historical_r3i1p1_190601-191012.nc'
    from pprint import pprint
    pprint( get_urls(file_functional_id,'esgf-node.llnl.gov') )
