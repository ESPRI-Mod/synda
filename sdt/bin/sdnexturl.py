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
import sdutils
import sdconst
import sdquicksearch
import sdexception

def run(tr):
    """
    Returns
        True: url has been switched to a new one
        False: nothing changed (same url)
    """
    transfer_protocol=sdutils.get_transfer_protocol(tr.url)
    if transfer_protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP:
        # GRIDFTP url

        try:
            next_url(tr)
            return True
        except sdexception.FileNotFoundException as e:
            sdlog.info("SDNEXTUR-001","Cannot switch url for %s (FileNotFoundException)"%(tr.file_functional_id,))
            return False
        except sdexception.HttpUrlNotFoundException as e:
            sdlog.info("SDNEXTUR-002","Cannot switch url for %s (HttpUrlNotFoundException)"%(tr.file_functional_id,))
            return False
        except Exception as e:
            sdlog.info("SDNEXTUR-003","Unknown exception (file_functional_id=%s,exception=%s)"%(tr.file_functional_id,str(e)))
            return False

    else:
        # most likely HTTP url
        #
        # nothing to do
        # (i.e. no fallback for now in this module for http url)

        return False

def next_url(tr):
    urls=get_urls(tr.file_functional_id)
    urls=remove_unsupported_url(urls)

    if 'url_http' in urls:
        old_url=tr.url
        new_url=urls['url_http']

        tr.url=new_url

        sdlog.info("SDNEXTUR-004","Url successfully switched (file_functional_id=%s,old_url=%s,new_url=%s)"%(tr.file_functional_id,old_url,new_url))
    else:
        sdlog.info("SDNEXTUR-006","Http url not found (file_functional_id=%s)"%(tr.file_functional_id,))
        raise sdexception.HttpUrlNotFoundException()

def remove_unsupported_url(urls):

    # remove opendap url (opendap is not used in synda for now)
    try:
        del urls['url_opendap']
    except Exception as e:
        pass

    return urls

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
        sdlog.info("SDNEXTUR-090","File not found (file_functional_id=%s)"%(tr.file_functional_id,))
        raise sdexception.FileNotFoundException()

    return urls

url_fields=','.join(sdconst.URL_FIELDS)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    file_functional_id='cmip5.output1.LASG-CESS.FGOALS-g2.decadal1985.day.atmos.day.r1i1p1.v1.va_day_FGOALS-g2_decadal1985_r1i1p1_19880101-19881231.nc'
    print get_urls(file_functional_id)
