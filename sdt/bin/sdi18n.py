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

m0001="search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted."

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
    import StringIO                                                                                                                              
    buf = StringIO.StringIO()                                                                                                                    
    buf.write("%s\n%s\n"%(name,description))
    if example is not None:
        buf.write("\nExample\n%s\n"%example)
    if note is not None:
        buf.write("\nNotes\n%s\n"%note)
    return buf.getvalue()

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
Synda subcommands list

"""

m0016="synda - a fast and versatile data management tool for Earth Science Grid Federation (ESGF)"

m0017="action parameter"

m0018="""
Introduction to synda command

A session might go like


Search for a dataset

$ synda search cmip5.output1.NIMR-KMA.HadGEM2-AO.historical.mon.landIce.LImon.r1i1p1.v20130815
new  cmip5.output1.NIMR-KMA.HadGEM2-AO.historical.mon.landIce.LImon.r1i1p1.v20130815


Print dataset file(s)

$ synda search cmip5.output1.NIMR-KMA.HadGEM2-AO.historical.mon.landIce.LImon.r1i1p1.v20130815 -f
new  195.2 MB  cmip5.output1.NIMR-KMA.HadGEM2-AO.historical.mon.landIce.LImon.r1i1p1.v20130815.snw_LImon_HadGEM2-AO_historical_r1i1p1_186001-200512.nc


Install the dataset

$ sudo synda install cmip5.output1.NIMR-KMA.HadGEM2-AO.historical.mon.landIce.LImon.r1i1p1.v20130815 
1 file(s) will be added to the download queue.
Once downloaded, 195.2 MB of additional disk space will be used.
Do you want to continue? [Y/n] 
1 file(s) enqueued
You can follow the download using 'synda watch' and 'synda log' commands.


Check download progress

$ synda watch
Daemon not running


We see here that the daemon is not running, let 's see the log for more info

$ tail /var/log/synda/sdt/transfer.log
2015-12-11 20:02:31,844 ERROR SDTSCHED-928 OpenID not set in configuration file
2015-12-11 20:02:31,845 ERROR SDTSCHED-920 Error occured while retrieving ESGF certificate
2015-12-11 20:02:31,845 INFO SDDAEMON-010 Exception occured (SDTSCHED-264)
2015-12-11 20:02:31,846 INFO SDDAEMON-034 Daemon stopped

We see in the log that credentials (openid) are not set in the configuration file.

Let's do it

$ vi /etc/synda/sdt/sdt.conf


Then start the daemon

$ sudo systemctl start synda


Check download progress

$ synda watch
No current download

$ synda queue
status      count  size
error           1  181.9 MB

The last command tells us that the download failed.

Let's see why 

$ tail /var/log/synda/sdt/transfer.log
2015-12-12 00:30:36,329 INFO SDDOWNLO-102 Transfer failed (sdget_status=1,error_msg='Error occurs during download.',file_id=1,status=error,local_path=/srv/synda/sdt/cmip5/output1/NCAR/CCSM4/decadal1961/mon/seaIce/OImon/r10i2p1/v20120525/sic/sic_OImon_CCSM4_decadal1961_r10i2p1_196101-199012.nc,url=http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/NCAR/CCSM4/decadal1961/mon/seaIce/OImon/r10i2p1/sic/1/sic_OImon_CCSM4_decadal1961_r10i2p1_196101-199012.nc)





"""
