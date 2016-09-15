#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains next url routine."""

import argparse
import sdlog
import sdconst
import sdquicksearch
import sdexception

def run(tr):

    if is_gridftp_url():
        # gridftp failure: fallback to HTTP

        try:
            urls=get_urls(tr.file_functional_id)
            urls=remove_unsupported_url(urls)
            new_url=get_next_url(tr.url,urls)
            tr.url=new_url

        except sdexception.FileNotFoundException:
            sdlog.info("SDNEXTUR-001","File not found while trying to switch url (file_functional_id=%s)"%(tr.file_functional_id,))

    else:
        # no fallback for HTTP failure

        pass

def is_gridftp_url(url):
    pass

def remove_unsupported_url(urls):

    # remove opendap url (opendap is not used in synda for now)
    try:
        del urls['url_opendap']
    except Exception as e:
        pass

    return urls

def get_next_url(urls,current_url):
    for k in urls:
        print k
    else:
        sdlog.info("SDNEXTUR-002","(file_functional_id=%s)"%())

def get_urls(file_functional_id):
    result=sdquicksearch.run(parameter=['limit=1','fields=%s'%url_fields,'type=File','instance_id=%s'%file_functional_id],post_pipeline_mode=None)
    li=result.get_files()
    if len(li)>0:
        file_=li[0]

        # remove non url attributes
        try:
            del file_['attached_parameters']
        except Exception as e:
            pass

        urls=file_

    else:
        raise sdexception.FileNotFoundException()

    return urls

url_fields=','.join(sdconst.URL_FIELDS)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    file_functional_id='cmip5.output1.LASG-CESS.FGOALS-g2.decadal1985.day.atmos.day.r1i1p1.v1.va_day_FGOALS-g2_decadal1985_r1i1p1_19880101-19881231.nc'
    print get_urls(file_functional_id)
