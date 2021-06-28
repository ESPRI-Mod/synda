import asyncio
import os
import datetime
import httpx
import concurrent.futures
import uvloop
import requests

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
default_chunk_size=100 * 1024 *1024


def download_file(
        args,
):
    chunk_size = default_chunk_size
    index = args[0]
    local_path = args[1]
    url = args[2]
    destdir = os.path.dirname(local_path)
    if not os.path.exists(destdir):
        os.makedirs(destdir)
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    f = None
    socket = None
    downloaded_so_far = 0
    begin = datetime.datetime.now()
    try:
        with open(local_path, 'wb') as f:
            with requests.get(url, stream=True) as socket:
                socket.raise_for_status()
                for chunk in socket.iter_content(chunk_size=chunk_size):
                    downloaded_so_far += len(chunk)
                    f.write(chunk)

    except Exception as e:
        # remove the local file if something goes wrong
        if os.path.exists(local_path):
            os.unlink(local_path)
        raise
    finally:
        if f is not None:
            f.close()
        status_code = socket.status_code
        if socket is not None:
            socket.close()

    end = datetime.datetime.now()
    elapsed = end - begin
    speed = (downloaded_so_far // elapsed.total_seconds()) // 1024
    result = {
        "file_id": index + 1,
        "download speed": speed,
        "file size": downloaded_so_far,
        "duration": elapsed.total_seconds(),
        "start_date": begin.strftime(DATE_FORMAT),
        "end_date": end.strftime(DATE_FORMAT),
        "strategy": "asyncio - processes",
        "status_code": socket.status_code,
        "local_path": local_path,
    }

    if f is not None:
        f.close()
    status_code = socket.status_code
    if socket is not None:
        socket.close()

    print(result)
    return result


async def main(args):
    executor = concurrent.futures.ProcessPoolExecutor(
        max_workers=10,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
    finally:
        event_loop.close()


async def run_blocking_tasks(executor, args):

    loop = asyncio.get_event_loop()
    blocking_tasks = []
    for _args in args:
        blocking_tasks = [
            loop.run_in_executor(executor, download_file, _args),
        ]

    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]


if __name__ == '__main__':

    urls = [

        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/ph/ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        # 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/ph/ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/phyc/phyc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        # 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/phyc/phyc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/po4/po4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/po4/po4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/si/si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/si/si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/talk/talk_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/talk/talk_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/zooc/zooc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/zooc/zooc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20210408/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cordex/output/EUR-11/IPSL-INERIS/ECMWF-ERAINT/evaluation/r1i1p1/IPSL-INERIS-WRF331F/v1/mon/tas/v20140301/tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_198901-199012.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cordex/output/EUR-11/IPSL-INERIS/ECMWF-ERAINT/evaluation/r1i1p1/IPSL-INERIS-WRF331F/v1/mon/tas/v20140301/tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_199101-200012.nc',
    #     'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cordex/output/EUR-11/IPSL-INERIS/ECMWF-ERAINT/evaluation/r1i1p1/IPSL-INERIS-WRF331F/v1/mon/tas/v20140301/tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_200101-200812.nc',
    ]

    relative_paths = [

        'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc',
        'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc',
        'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc',
        'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc',
        'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.phyc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.phyc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.po4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.po4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.talk_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.talk_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.zooc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.zooc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc',
        # 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20210408.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc',
        # 'cordex.output.EUR-11.IPSL-INERIS.ECMWF-ERAINT.evaluation.r1i1p1.WRF331F.v1.mon.tas.v20140301.tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_198901-199012.nc',
        # 'cordex.output.EUR-11.IPSL-INERIS.ECMWF-ERAINT.evaluation.r1i1p1.WRF331F.v1.mon.tas.v20140301.tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_199101-200012.nc',
        # 'cordex.output.EUR-11.IPSL-INERIS.ECMWF-ERAINT.evaluation.r1i1p1.WRF331F.v1.mon.tas.v20140301.tas_EUR-11_ECMWF-ERAINT_evaluation_r1i1p1_IPSL-INERIS-WRF331F_v1_mon_200101-200812.nc',
    ]

    local_paths = [os.path.join(os.path.join(os.environ["ST_HOME"], "data"), relative_path) for relative_path in relative_paths]

    args = [(index, local_path, url) for index, local_path, url in zip(range(len(urls)), local_paths, urls)]
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Create a limited process pool.
    executor = concurrent.futures.ProcessPoolExecutor(
        max_workers=8,
    )

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        run_blocking_tasks(executor, args)
    )
    event_loop.close()
