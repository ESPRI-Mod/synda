#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains messages available as string."""

m0001="selection parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted."

def m0002(prog):
    buf="""  %s experiment=rcp45,rcp85 model=CCSM4
  %s project=ISI-MIP%%20Fasttrack searchapi_host=esg.pik-potsdam.de
  %s project=CMIP5 realm=atmos
  %s realm=atmos project=CMIP5
  %s atmos 50
  %s MIROC rcp45 2
  %s CCSM4 rcp45 atmos mon r1i1p1
  %s title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc project=EUCLIPSE
  %s title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc
  %s clt_day_CanESM2_esmControl_r1i1p1_19010101-22501231.nc
  %s pr_day_MPI-ESM-LR_abrupt4xCO2_r1i1p1_18500101-18591231.nc
  %s c20c.UCT-CSAG.HadAM3P-N96.NonGHG-Hist.HadCM3-p50-est1.v1-0.mon.atmos.run060.v20140528
  %s title=rlds_bced_1960_1999_gfdl-esm2m_rcp8p5_2051-2060.nc searchapi_host=esg.pik-potsdam.de
  %s tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
  %s tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613
  %s dataset_id=tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
  %s cmip5.output1.IPSL.IPSL-CM5A-LR.abrupt4xCO2.fx.land.fx.r0i0p0.v20110726.sftgif_fx_IPSL-CM5A-LR_abrupt4xCO2_r0i0p0.nc"""%((prog,)*17)

    return buf

def m0003(host):
    return """Request sent to %s. Please wait.."""%host
    #return """%s contacted. Waiting for reply.."""%host

def m0004(prog):
    return """  %s
  %s mo
  %s model
  %s model MR"""%((prog,)*4)

m0005="""
  If 'localsearch' option is false (default), search in ESGF archive.

  If 'localsearch' option is true, search in local repository.

  Without search filters, all records are returned.

  Filter name can be omitted (i.e. 'atmos' can be used intead of 'realm=atmos').

  For ease of use, limit can be set directly on the command line as a simple number (i.e. the number of row(s) to return)
"""

def m0006(name,description,example=None,note=None):
    return """%s
%s

Examples

%s 

Notes

%s 
"""%(name,description,example,note)

m0007='delete cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926.ua_6hrLev_MIROC4h_rcp45_r1i1p1_2029081100-2029082018.nc'
m0008='add cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926.ua_6hrLev_MIROC4h_rcp45_r1i1p1_2029081100-2029082018.nc'
m0009="<file> format follow Search-API 'instance_id' attribute."
m0010="""
            retry all
            retry cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926.ua_6hrLev_MIROC4h_rcp45_r1i1p1_2029081100-2029082018.nc
"""

m0011="""
        set                  Show all session parameters that differ from default values.
        set all              Show all session parameters.
        set option           Show all options
        set facet            Show all facets
        set default          Reset all session parameters
        set name=value       Set <name> to <value>
        set {name}?          Show session parameter value
        """

m0012="""
            daemon start
            daemon stop
            daemon status
        """

m0013="""
            sample small_dataset
            sample remote
            sample local
        """

m0014="""
            selection list [ filter ]
            selection edit <idx>
            selection cat <idx>
            selection print <idx>
        """

m0015="""
autoremove - Remove old datasets versions
cache - Manage cache
certificate - Manage X509 certificate
daemon - Start/stop the daemon (download background process)
dump - Display raw metadata
help - Show help
history - Show history
install - Install dataset
list - List installed dataset
param - Display ESGF parameters
pexec - Execute post-processing task
queue - Display download queue status
remove - Remove dataset
replica - Change replica
reset - Remove all 'waiting' and 'error' transfers
retry - Retry transfer
search - Search dataset
selection - Manage selection
show - Display detailed information about dataset
stat - Display summary information about dataset
test - Test file download
update - Update ESGF parameter local cache
upgrade - Perform an upgrade (retrieve new version for already installed datasets)
version - List all versions of a dataset
watch - Display running transfer

"""

m0016="synda - a fast and versatile data management tool for Earth Science Grid Federation (ESGF)"
