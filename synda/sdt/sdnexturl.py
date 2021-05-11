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

from synda.source.db.connection.models import Connection
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.db.models import Config as Db
from synda.source.config.api.constants import URL_FIELDS
from synda.source.db.task.failed_url.update.models import insert_into_failed_url


def run(tr):
    """
    Returns
        True: url has been switched to a new one
        False: nothing changed (same url)
    """
    lastrowid, msg = insert_into_failed_url(tr.url, tr.file_functional_id)

    if msg:
        code = "SDNEXTUR-001" if "integrity" in msg.lower() else "SDNEXTUR-002"
        sdlog.info(
            code,
            "{} | {}".format(
                msg,
                "url = {}, file_functional_id={}".format(
                    tr.url,
                    tr.file_functional_id,
                )
            ),
        )

    success = False
    conn = None
    try:
        conn = Connection().get_database_connection()
        next_http_url(tr, conn)
        success = True
    except sdexception.FileNotFoundException as e:
        sdlog.info(
            "SDNEXTUR-003", "Cannot switch url for %s (FileNotFoundException)" % (tr.file_functional_id,),
        )
    except sdexception.NextUrlNotFoundException as e:
        sdlog.info(
            "SDNEXTUR-004", "Cannot switch url for %s (NextUrlNotFoundException)" % (tr.file_functional_id,),
        )
    except Exception as e:
        sdlog.info(
            "SDNEXTUR-005", "Unknown exception (file_functional_id=%s,exception=%s)" % (tr.file_functional_id, str(e)),
        )
    finally:
        if conn:
            conn.close()

    return success


def next_http_url(tr, conn):
    # [[url1,protocol1],[url2,protocol2],...]
    all_urlps = get_urls(tr.file_functional_id)
    sdlog.info("SDNEXTUR-006", "all_urpls= %s" % (all_urlps,))
    c = conn.cursor()
    fus = c.execute(
        "SELECT url FROM failed_url WHERE file_id=(SELECT file_id FROM file WHERE file_functional_id=?)",
        (tr.file_functional_id,),
    )
    failed_urls = [fu[0] for fu in fus.fetchall()]
    sdlog.info("SDNEXTUR-007", "failed_urls= %s" % (failed_urls,))
    urlps = [urlp for urlp in all_urlps if urlp[0] not in failed_urls]
    # ... Note that list comprehensions preserve order.
    urls = [urlp[0] for urlp in urlps if urlp[0].startswith("http")]
    # At this point urls is just a list of urls.
    
    if len(urls) > 0:
        old_url = tr.url
        new_url = urls[0]
        tr.url = new_url
        sdlog.info(
            "SDNEXTUR-008",
            "Url successfully switched (file_functional_id=%s,old_url=%s,new_url=%s)" % (tr.file_functional_id, old_url, new_url))
    else:
        sdlog.info("SDNEXTUR-009","Next url not found (file_functional_id=%s)"%(tr.file_functional_id,))
        raise sdexception.NextUrlNotFoundException()


def get_urls(file_functional_id):
    """returns a prioritized list of [url,protocol] where each url can supply the specified file"""

    try:
        result = sdquicksearch.run(
            parameter=['limit=4', 'fields=%s' % url_fields, 'type=File', 'instance_id=%s' % file_functional_id],
            post_pipeline_mode=None,
        )
    except Exception as e:
        sdlog.debug("SDNEXTUR-015", "exception %s.  instance_id=%s" % (e, file_functional_id))
        raise e

    li = result.get_files()
    sdlog.info("SDNEXTUR-016", "sdquicksearch returned %s sets of file urls: %s" % (len(li), li))

    if len(li) == 0:
        # No urls found. Try again, but wildcard the file id. (That leads to a string search on all
        # fields for the wildcarded file id, rather than a match of the instance_id field only.)
        result=sdquicksearch.run(
            parameter=['limit=4', 'fields=%s' % url_fields, 'type=File', 'instance_id=%s' % file_functional_id+'*'],
            post_pipeline_mode=None,
        )
        li = result.get_files()
        sdlog.info("SDNEXTUR-017", "sdquicksearch 2nd call %s sets of file urls: %s" % (len(li), li))
    # result looks like
    # [ {protocol11:url11, protocol12:url12, attached_parameters:dict, score:number, type:'File',
    #    size:number} }, {[another dict of the same format}, {another dict},... ]
    # with no more than limit=4 items in the list, and no more than three protocols.  
    # We'll return something like urlps = [ [url1,protocol1], [url2,protocol2],... ]
    # The return value could be an empty list.
    # Note: These nested lists are ugly; it's just a quick way to code something up.

    urlps = []
    for dic in li:
        urlps += [[dic[key], key] for key in list(dic.keys()) if key.find('url_') >=0 and dic[key].find('//None') < 0]
        # ... protocol keys are one of 'url_http', 'url_gridftp'
        # The search for //None bypasses an issue with the SOLR lookup where there is no
        # url_gridftp possibility.

    return prioritize_urlps(urlps)


url_fields = ','.join(URL_FIELDS)  # used for the sdquicksearch call above


def prioritize_urlps( urlps ):
    """Orders a list urlps so that the highest-priority urls come first.  urlps is a list of
    lists of the form [url,protocol].  HTTP urls are preferred over everything else.
    Then, prefer some data nodes over others."""
    def priprotocol(protocol):
        if protocol.find('http') > 0:
            return 0
        return 1

    def priurl(url):
        if url.find('llnl') >0:
            return 0
        if url.find('ceda') >0:
            return 1
        if url.find('dkrz') >0:
            return 2
        if url.find('ipsl') >0:
            return 3
        if url.find('nci') >0:
            return 4
        return 5
    return sorted(
        urlps,
        key=(lambda urlp: (priprotocol(urlp[1]), priurl(urlp[0]))),
    )


if __name__ == '__main__':

    file_functional_ids = [
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.land.Lmon.r1i1p1.v20110822.mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc",
        "cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v1.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20130101.sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc",
        "cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v1.psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.land.Lmon.r1i1p1.v20110822.mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20110901.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc",
        "cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.land.Lmon.r1i1p1.v1.mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.land.Lmon.r1i1p1.v20111018.mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20110901.psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.land.Lmon.r1i1p1.v20110822.mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc",
        "cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.seaIce.OImon.r1i1p1.v1.sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc",
        "cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v1.psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc",
        "cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v1.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20110901.tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20130101.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20110901.psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20110901.tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc",
        "cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.seaIce.OImon.r1i1p1.v1.sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20110901.psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc",
        "cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.ocnBgchem.Omon.r1i1p1.v20120731.dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc",
        # "cmip5.output2.MPI-M.MPI-ESM-P.past1000.mon.ocean.Omon.r1i1p1.v20131203.rhopoto_Omon_MPI-ESM-P_past1000_r1i1p1_179001-179912.nc",
    ]

    file_functional_ids = [file_functional_ids[24]]
    for file_functional_id in file_functional_ids:
        try:
            from pprint import pprint
            pprint(
                get_urls(file_functional_id),
            )

        except sdexception.SDException as e:
            print(e.msg)
