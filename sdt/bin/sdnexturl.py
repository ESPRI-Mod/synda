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
    try:
        urls=get_urls(tr.file_functional_id)

        new_url=get_next_url(tr.url,urls)

        tr.url=new_url
    except sdexception.FileNotFoundException:
        sdlog.info("SDNEXTUR-001","File not found while trying to switch url (file_functional_id=%s)"%())

def get_next_url(urls,current_url):
    for k, in urls:
        print 
    else:
        sdlog.info("SDNEXTUR-001","(file_functional_id=%s)"%())

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
