#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module translate search-api json output to python object."""

import argparse
import json
import sdapp
import sdlog
from sdexception import SDException
from sdtypes import Item

def parse_parameters(buffer):
    try:
        xmldoc = json.loads(buffer)
    except Exception, e:
        raise

    params={}
    parameter_nodes=xmldoc.xpath("./lst[@name='facet_counts']/lst[@name='facet_fields']")
    for parameter_node in parameter_nodes:
        for facet in parameter_node.xpath("./*"):
            facet_name=facet.attrib["name"]

            items=[]
            for n in facet.xpath("./*"):
                items.append(Item(n.attrib["name"], int(n.text)))

            params[facet_name]=items

    return params

def parse_metadata(buffer):
    """Parse result for both type (Dataset and File)."""
    xmldoc=None
    l__files=[] # can be real file or dataset, depending on "type" input facet

    if buffer is None:
        raise SDException("SYNDAXML-001","Buffer is empty")

    try:
        xmldoc = json.loads(buffer)
    except Exception, e:
        raise


    # --- parse header and footer nodes (header name is "responseHeader" and footer name is "facet_counts") --- #

    # retrieve header & footer (those nodes always exist)
    header_node=xmldoc["responseHeader"]
    footer_node=xmldoc["facet_counts"]

    # parse footer
    fields_node=footer_node["facet_fields"]

    # --- parse body node --- #

    body_node=xmldoc["response"]

    # retrieve "numFound" attribute
    l__num_found=int(body_node["numFound"]) # int/unicode conversion

    doc_nodes=body_node["docs"]

    for doc_node in doc_nodes: # file/dataset loop
        l__dict={}

        """
        SAMPLE

        {
        "id":"cmip5.output1.CCCma.CanCM4.decadal1970.mon.landIce.LImon.r5i2p1.v20120601|esgf2.dkrz.de",
        "data_node":"esgf2.dkrz.de",
        "instance_id":"cmip5.output1.CCCma.CanCM4.decadal1970.mon.landIce.LImon.r5i2p1.v20120601",
        "size":23697992,
        "type":"Dataset",
        "variable":["sbl",
          "snc",
          "snd",
          "snm",
          "snw",
          "tsn"],
        "score":1.0
        },
        """

        for attr_name,attr_value in doc_node.iteritems():

            # TODO: maybe move transformation below in a downstream
            #       step (e.g. in the generic pipeline) so to keep
            #       original xml stream not altered when using dump
            #       action in raw mode.

            if attr_name=="url":
                # url array have three subitems (GRIDFTP, HTTPServer and openDAP)
                # url array entry sample => http://bmbf-ipcc-ar5.dkrz.de/thredds/fileServer/cmip5/output1/MPI-M/MPI-ESM-P/historical/mon/atmos/Amon/r1i1p1/v20120315/tasmin/tasmin_Amon_MPI-ESM-P_historical_r1i1p1_185001-200512.nc|application/netcdf|HTTPServer

                for item in attr_value:
                    url=item.split('|')[0] # keep only first field (i.e. keep only the file url)
                    protocol=item.split('|')[-1]

                    if protocol.upper()=="HTTPSERVER":
                        l__dict['url_http']=url
                    elif protocol.upper()=="GRIDFTP":
                        l__dict['url_gridftp']=url
                    elif protocol.upper()=="OPENDAP":
                        l__dict['url_opendap']=url
            else:
                l__dict[attr_name]=attr_value

        l__files.append(l__dict)

    sdlog.debug("SYNDJSON-014","files-count=%d"%len(l__files))

    return {'files':l__files,'num_found':l__num_found,'num_result':len(l__files)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',required=True)
    args = parser.parse_args()

    # read search-api output sample
    with open(args.file, 'r') as fh:
        buffer=fh.read()

    #parse_parameters(buffer)
    print parse_metadata(buffer)
