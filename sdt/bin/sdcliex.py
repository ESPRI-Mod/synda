#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains command line examples.

Note
    sdcliex means 'SynDa Command LIne EXample'
"""

def autoremove():
    buf=""""""
    return buf

def cache():
    buf=""""""
    return buf

def certificate():
    buf="""  synda certificate renew
  synda certificate print
  synda certificate info"""
    return buf

def check():
    buf="""  synda check dataset_version
  synda check file_variable CMIP5 atmos orog
  synda check selection"""
    return buf

def config():
    buf=""""""
    return buf

def contact():
    buf=""""""
    return buf

def count():
    buf="""  synda count
  synda count CMIP5
  synda count obs4MIPs -f
  synda count -s selection.txt --timestamp_left_boundary 2012-01-01T01:00:00Z --timestamp_right_boundary 2015-01-01T01:00:00Z"""
    return buf

def daemon():
    buf="""  synda daemon start
  synda daemon stop"""
    return buf

def dump():
    buf="""  synda dump CORDEX IPSL-INERIS  evaluation limit=1 -f -F indent
  synda dump CMIP5 IPSL mon atmos limit=1 -d -F indent
  synda dump -R CMIP5 limit=1 -f -F indent
  synda dump omldamax_day_IPSL-CM5A-LR_decadal1995_r1i1p1_19960101-20051231.nc -F indent
  synda dump -R CMIP5 limit=1 -f -F value -C url_http,url_gridftp
  synda dump CORDEX IPSL-INERIS  evaluation limit=1 -f -C local_path -F value"""
    return buf

def facet():
    buf="""  synda facet experiment MPI-ESM-LR | column
  synda facet variable MPI-ESM-LR | column
  synda facet experiment fddtalk MPI-ESM-LR"""
    return buf

def get():
    buf="""  synda get cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601
  synda get http://esgf1.dkrz.de/thredds/fileServer/cmip5/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc
  synda get sfcWind_ARC-44_ECMWF-ERAINT_evaluation_r1i1p1_AWI-HIRHAM5_v1_sem_197903-198011.nc
  synda get clcalipso_cfDay_NICAM-09_aqua4K_r1i1p1_00000101-00000330.nc
  synda get -d CORDEX 1
  synda get -f CMIP5 fx 1
  synda get protocol=gridftp limit=1 -f
  synda get uo_Omon_FGOALS-gl_past1000_r1i1p1_100001-199912.nc wmo_Omon_FGOALS-gl_past1000_r1i1p1_100001-199912.nc
  synda get http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CCCma/CanESM2/esmFdbk2/mon/ocean/Omon/r1i1p1/zostoga/1/zostoga_Omon_CanESM2_esmFdbk2_r1i1p1_200601-210012.nc
  synda get gsiftp://esgf1.dkrz.de:2811//cmip5/cmip5/output2/MPI-M/MPI-ESM-P/past1000/mon/ocean/Omon/r1i1p1/v20131203/umo/umo_Omon_MPI-ESM-P_past1000_r1i1p1_112001-112912.nc
  synda get http://esgf1.dkrz.de/thredds/fileServer/cmip5/cmip5/output2/MPI-M/MPI-ESM-P/past1000/mon/ocean/Omon/r1i1p1/v20131203/umo/umo_Omon_MPI-ESM-P_past1000_r1i1p1_112001-112912.nc
  synda get cmip5.output2.MPI-M.MPI-ESM-P.past1000.mon.ocean.Omon.r1i1p1.v20131203.rhopoto_Omon_MPI-ESM-P_past1000_r1i1p1_179001-179912.nc"""
    return buf

def help():
    buf=""""""
    return buf

def history():
    buf=""""""
    return buf

def install():
    buf="""  synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
  synda install sfcWind_ARC-44_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4-SN_v1_sem_197012-198011.nc
  synda install MPI-ESM-LR rcp26"""
    return buf

def intro():
    buf=""""""
    return buf

def list():
    buf="""  synda list limit=5 -f
  synda list limit=5 -d
"""
    return buf

def metric():
    buf="""  synda metric -g data_node -m rate -p CMIP5
  synda metric -g project -m size"""
    return buf

def open():
    buf="""  synda open cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc
  synda open -g 1000x600+70+0 orog_fx_CanESM2_historicalGHG_r0i0p0.nc"""
    return buf

def param():
    buf="""  synda param | column
  synda param institute | column
  synda param institute NA
  synda param project"""
    return buf

def pexec():
    buf="""  synda pexec -s cdf_test.txt cdf"""
    return buf

def queue():
    buf="""  synda queue obs4MIPs
  synda queue CMIP5
  synda queue"""
    return buf

def remove():
    buf="""  synda remove cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529
  synda remove status=error -n
  synda remove data_node=vesg.ipsl.upmc.fr,tds.ucar.edu,esgnode2.nci.org.au status=error -n
  synda remove CMIP5 MIROC-ESM historicalNat mon"""
    return buf

def replica():
    buf="""  synda replica next
  synda replica next cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc"""
    return buf

def reset():
    buf=""""""
    return buf

def retry():
    buf=""""""
    return buf

def search(prog):
    buf="""  %s cmip5 output1 MOHC HadGEM2-A amip4xCO2 mon atmos Amon r1i1p1
  %s rcp85 3hr timeslice=20050101-21001231 -f
  %s project=CORDEX 'query=domain:EUR*11*'
  %s rcp85 3hr start=2005-01-01T00:00:00Z end=2100-12-31T23:59:59Z -d
  %s timeslice=00100101-20501231 model=GFDL-ESM2M "Air Temperature" -f
  %s experiment=rcp45,rcp85 model=CCSM4
  %s project=CMIP5 realm=atmos
  %s realm=atmos project=CMIP5
  %s CMIP5 frequency=day atmos tas -d
  %s CMIP5 frequency=day atmos tas -v
  %s CMIP5 frequency=day atmos tas -f
  %s project=ISI-MIP%%20Fast%%20Track searchapi_host=esg.pik-potsdam.de
  %s atmos 50
  %s MIROC rcp45 2
  %s CCSM4 rcp45 atmos mon r1i1p1
  %s variable=tas institute!=MPI-M
  %s title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc project=EUCLIPSE
  %s title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc
  %s clt_day_CanESM2_esmControl_r1i1p1_19010101-22501231.nc
  %s pr_day_MPI-ESM-LR_abrupt4xCO2_r1i1p1_18500101-18591231.nc
  %s c20c.UCT-CSAG.HadAM3P-N96.NonGHG-Hist.HadCM3-p50-est1.v1-0.mon.atmos.run060.v20140528
  %s title=rlds_bced_1960_1999_gfdl-esm2m_rcp8p5_2051-2060.nc searchapi_host=esg.pik-potsdam.de
  %s tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
  %s tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613
  %s dataset_id=tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
  %s http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CCCma/CanESM2/esmFdbk2/mon/ocean/Omon/r1i1p1/zostoga/1/zostoga_Omon_CanESM2_esmFdbk2_r1i1p1_200601-210012.nc
  %s gsiftp://esgf1.dkrz.de:2811//cmip5/cmip5/output2/MPI-M/MPI-ESM-P/past1000/mon/ocean/Omon/r1i1p1/v20131203/umo/umo_Omon_MPI-ESM-P_past1000_r1i1p1_112001-112912.nc
  %s cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc"""%((prog,)*28)

    return buf

def selection():
    buf=""""""
    return buf

def show():
    buf="""  synda show cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc
  synda show cmip5.output1.IPSL.IPSL-CM5A-LR.historical.mon.land.Lmon.r1i1p1.v20120430"""
    return buf

def stat():
    buf="""  synda stat cmip5.output1.MOHC.HadGEM2-A.amip4xCO2.mon.atmos.Amon.r1i1p1.v20131108
  synda stat cmip5.output1.CCCma.CanCM4.decadal1964.mon.ocean.Omon.r1i1p1.v20120622
  synda stat MPI-ESM-LR rcp26
  synda stat project=CORDEX 'query=domain:EUR*11*'
  synda stat ECMWF-ERAINT frequency=day"""
    return buf

def update():
    buf=""""""
    return buf

def upgrade():
    buf=""""""
    return buf

def variable():
    buf="""  synda variable
  synda variable -S
  synda variable -s
  synda variable sfcWind
  synda variable wind_speed
  synda variable Near-Surface Wind Speed
  synda variable Dissolved Inorganic Carbon Concentration
  synda variable cell_area
  export COLUMNS ; synda variable -s | cut -c 1-20 | column | less"""
    return buf

def version():
    buf="""  synda version cmip5.output1.MOHC.HadGEM2-A.amip4xCO2.mon.atmos.Amon.r1i1p1.v20131108
  synda version cmip5.output1.NCAR.CCSM4.rcp26.mon.atmos.Amon.r1i1p1.v20130426"""
    return buf

def watch():
    buf=""""""
    return buf
