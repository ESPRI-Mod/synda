# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
CORDEX = dict(
    files=[
        "tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_198901-199012.nc",
        "tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_199101-200012.nc",
        "tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_200101-200812.nc",
    ],
    urls=[
        "http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cordex/output/EUR-11/IPSL-INERIS/ECMWF-ERAINT/evaluation/r1i1p1/IPSL-INERIS-WRF331F/v1/mon/tas/v20140301/tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_198901-199012.nc",
        "http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cordex/output/EUR-11/IPSL-INERIS/ECMWF-ERAINT/evaluation/r1i1p1/IPSL-INERIS-WRF331F/v1/mon/tas/v20140301/tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_199101-200012.nc"
        "http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cordex/output/EUR-11/IPSL-INERIS/ECMWF-ERAINT/evaluation/r1i1p1/IPSL-INERIS-WRF331F/v1/mon/tas/v20140301/tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_200101-200812.nc",
    ],

    dataset=dict(
        name="cordex.output.EUR-11.IPSL-INERIS.ECMWF-ERAINT.evaluation.r1i1p1.WRF331F.v1.mon.tas.v20140301",
        version="20140301",
    ),
)

SYNDA_DEV_DATA=dict(
    cordex=CORDEX,
)
