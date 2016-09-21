#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains xml functions."""

import argparse
import json
from lxml import etree
import sdapp
import sdlog
from sdexception import SDException
from sdtypes import Item

def parse_parameters(buffer):
    try:
        xmldoc = etree.fromstring(buffer) # in our case, xmldoc is the top level response element/tag
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
        xmldoc = etree.fromstring(buffer) # in our case, xmldoc is the top level response element/tag
    except Exception, e:
        raise


    # --- parse header and footer nodes (header name is "responseHeader" and footer name is "facet_counts") --- #

    # retrieve header & footer (those nodes always exist)
    header_node=xmldoc.xpath("./lst[@name='responseHeader']")[0]
    footer_node=xmldoc.xpath("./lst[@name='facet_counts']")[0]

    # parse footer
    fields_node=xmldoc.xpath("./lst[@name='facet_counts']/lst[@name='facet_fields']")[0]

    # --- parse body node --- #

    body_node=xmldoc.xpath("./result")[0]

    # retrieve "numFound" attribute
    l__num_found=int(body_node.attrib["numFound"]) # int/unicode conversion

    doc_nodes=xmldoc.xpath("./result/doc")

    for doc_node in doc_nodes: # file/dataset loop
        l__dict={}

        # process fields (list of 'str' and 'arr' tags)
        for n in doc_node.getchildren():
            l__name=n.attrib["name"]

            # top level type switch
            if n.tag=="str":

                """
                top level str tags samples:

                <str name="title">tas_Amon_HadGEM2-ES_rcp60_r1i1p1_203612-206111.nc</str>
                <str name="type">File</str>
                <str name="index_node">pcmdi11.llnl.gov</str>
                <str name="instance_id">cmip5.output1.MOHC.HadGEM2-ES.rcp60.mon.atmos.Amon.r1i1p1.v20110930.tas_Amon_HadGEM2-ES_rcp60_r1i1p1_203612-206111.nc_0</str>
                <str name="master_id">cmip5.output1.MOHC.HadGEM2-ES.rcp60.mon.atmos.Amon.r1i1p1.tas_Amon_HadGEM2-ES_rcp60_r1i1p1_203612-206111.nc_0</str>
                <str name="metadata_format">THREDDS</str>
                <str name="metadata_url">http://cmip-dn.badc.rl.ac.uk/thredds/catalog.xml</str>

                when using "Dataset" type, functional dataset id is returned in "id" attribute, not in dataset_id attribute
                (with "File" type, it's the contrary)
                <str name="id">cmip5.output1.MOHC.HadGEM2-ES.rcp60.mon.atmos.Amon.r1i1p1.v20110930.tas_Amon_HadGEM2-ES_rcp60_r1i1p1_203612-206111.nc_0|cmip-dn.badc.rl.ac.uk</str>

                <str name="version">1</str>
                <str name="data_node">cmip-dn.badc.rl.ac.uk</str>
                <str name="dataset_id">cmip5.output1.MOHC.HadGEM2-ES.rcp60.mon.atmos.Amon.r1i1p1.v20110930|cmip-dn.badc.rl.ac.uk</str>
                """

                l__value=n.text

                if l__name=="id":
                    # note: used for file AND dataset

                    # sample for the file case:    cmip5.output1.MOHC.HadCM3.historical.mon.atmos.Amon.r1i1p1.v20110823.tas_Amon_HadCM3_historical_r1i1p1_188412-190911.nc_0|cmip-dn.badc.rl.ac.uk
                    # sample for the dataset case: cmip5.output1.NCAR.CCSM4.abrupt4xCO2.fx.atmos.fx.r0i0p0.v20120413|pcmdi9.llnl.gov
                    #
                    l__dict[l__name]=l__value

                elif l__name=="dataset_id":
                    # note: only used as input facet parameter (not as part of output "fields" member)

                    # sample: cmip5.output1.MOHC.HadGEM2-ES.rcp60.mon.atmos.Amon.r1i1p1.v20110930|cmip-dn.badc.rl.ac.uk
                    #
                    l__dict[l__name]=l__value

                else:

                    l__dict[l__name]=l__value

            elif n.tag=="date":

                """
                top level date tag samples:

                <date name="timestamp">2011-06-03T22:45:27Z</date>
                """

                l__value=n.text
                l__dict[l__name]=l__value

            elif n.tag=="bool":

                """
                samples:

                <bool name="replica">false</bool>
                <bool name="latest">true</bool>
                """

                l__value=n.text
                l__dict[l__name]=l__value

            elif n.tag=="long":
                """
                top level long tag samples:

                <long name="size">33432404</long>
                """

                l__value=n.text
                l__dict[l__name]=l__value

            elif n.tag=="arr":

                for arr_n in n.getchildren():

                    # array child type switch
                    if arr_n.tag=="str":

                        """
                        array / str tag samples:

                        <arr name="checksum"> <str>ddbecc65df76b4b713b686974fe7153a</str> </arr>
                        <arr name="checksum_type"> <str>MD5</str> </arr>
                        <arr name="cmor_table"> <str>Amon</str> </arr>
                        <arr name="dataset_id_template_"> <str>cmip5.%(product)s.%(institute)s.%(model)s.%(experiment)s.%(time_frequency)s.%(realm)s.%(cmor_table)s.%(ensemble)s</str> </arr>
                        <arr name="description"> <str>HadGEM2-ES model output prepared for CMIP5 RCP6</str> </arr>
                        <arr name="drs_id"> <str>cmip5.output1.MOHC.HadGEM2-ES.rcp60.mon.atmos.Amon.r1i1p1</str> </arr>
                        <arr name="ensemble"> <str>r1i1p1</str> </arr>
                        <arr name="experiment"> <str>rcp60</str> </arr>
                        <arr name="cf_standard_name"> <str>air_temperature</str> </arr>
                        <arr name="forcing"> <str>GHG, Oz, SA, LU, Sl, Vl, BC, OC, (GHG = CO2, N2O, CH4, CFCs)</str> </arr>
                        <arr name="format"> <str>netCDF, CF-1.4</str> </arr>
                        <arr name="institute"> <str>MOHC</str> </arr>
                        <arr name="model"> <str>HadGEM2-ES</str> </arr>
                        <arr name="product"> <str>output1</str> </arr>
                        <arr name="project"> <str>CMIP5</str> </arr>
                        <arr name="realm"> <str>atmos</str> </arr>
                        <arr name="tracking_id"> <str>900265d1-f002-4ad8-8be0-04149277c3e7</str> </arr>
                        <arr name="time_frequency"> <str>mon</str> </arr>
                        <arr name="variable"> <str>tas</str> </arr>
                        <arr name="variable_long_name"> <str>Near-Surface Air Temperature</str> </arr>
                        """

                        l__value=arr_n.text

                        # TODO: maybe move transformation below in a downstream
                        #       step (e.g. in the generic pipeline) so to keep
                        #       original xml stream not altered when using dump
                        #       action in raw mode.

                        # WARNING
                        #
                        # this switch is a bit tricky.
                        #
                        # we pass here for all subitems of all arrays.
                        # 'l__name' keep the same value for all the subitems of one array.
                        # 
                        #
                        if l__name=="url":
                            # url array have three subitems (GRIDFTP, HTTPServer and openDAP), so we pass here three times
                            # url array entry sample => http://bmbf-ipcc-ar5.dkrz.de/thredds/fileServer/cmip5/output1/MPI-M/MPI-ESM-P/historical/mon/atmos/Amon/r1i1p1/v20120315/tasmin/tasmin_Amon_MPI-ESM-P_historical_r1i1p1_185001-200512.nc|application/netcdf|HTTPServer

                            url=l__value.split('|')[0] # keep only first field (i.e. keep only the file url)
                            protocol=l__value.split('|')[-1]

                            if protocol.upper()=="HTTPSERVER":
                                l__dict['url_http']=url
                            elif protocol.upper()=="GRIDFTP":
                                l__dict['url_gridftp']=url
                            elif protocol.upper()=="OPENDAP":
                                l__dict['url_opendap']=url

                        elif l__name=="experiment_family":
                            # not used

                            """
                            sample
                            <arr name="experiment_family">
                              <str>All</str>
                              <str>RCP</str>
                            </arr>
                            """

                            pass


                        else:
                            # we now use 'list' type here (needed for dataset type (e.g. variable))

                            if l__name not in l__dict:
                                l__dict[l__name]=[l__value]
                            else:
                                l__dict[l__name].append(l__value)

                    elif arr_n.tag=="float":
                        # type not used for now

                        """
                        sample:

                        <arr name="score"><float name="score">1.9600565</float></arr>
                        """

                        pass

        l__files.append(l__dict)

    sdlog.debug("SYNDAXML-014","files-count=%d"%len(l__files))

    return {'files':l__files,'num_found':l__num_found,'num_result':len(l__files)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',required=True)
    args = parser.parse_args()

    # read search-api output sample
    with open(args.file, 'r') as fh:
        buffer=fh.read()

    #result=parse_parameters(buffer)
    result=parse_metadata(buffer)

    print "%s\n"%json.dumps(result,indent=4, separators=(',', ': '))
