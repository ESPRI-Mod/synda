# # -*- coding: utf-8 -*-
# ##################################
# #  @program        synda
# #  @description    climate models data transfer program
# #  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
# #                             All Rights Reserved"
# #  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
# ##################################
import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

durations = []

# install -s /home_local/journoud/DEV/WORKSPACES/synda/selection/sample/sample_selection_01_bis.txt
# Observations

files = {

'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc': 86344659,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc': 88114316,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc': 795795708,
'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc': 27452120,
'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc': 138080132,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361584,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602224,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361756,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602396,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361516,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602156,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361552,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602192,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361576,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602216,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361600,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602240,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361572,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602212,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361484,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602124,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361460,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602100,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361456,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602096,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361464,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602104,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361416,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602056,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.phyc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361724,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.phyc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602364,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.po4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361464,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.po4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602104,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361460,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602100,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.talk_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361472,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.talk_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602112,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.zooc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361560,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.zooc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602200,
'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20210408.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc': 5545240276,










}

hardware = "synda-dev"

sizes = []
for key in files.keys():
    sizes.append( files[key])

print(max(sizes))

sizes = 0
for key in files.keys():
    sizes += files[key]

coeff_bytes_2_mo = 1.0 / (8 * 1024 * 1024)
coeff_bytes_2_go = 1.0 / (8 * 1024 * 1024 * 1024)

# download speed unit : KiB/s
# file size unit : byte
# elapsed time unit : s

columns = [
    'file_id',
    'url',
    'file_functional_id',
    'filename',
    'local_path',
    'data_node',
    'checksum',
    'checksum_type',
    'duration',
    'size',
    'rate',
    'start_date',
    'end_date',
    'crea_date',
    'status',
    'error_msg',
    'sdget_status',
    'sdget_error_msg',
    'priority',
    'tracking_id',
    'model',
    'project',
    'variable',
    'last_access_date',
    'dataset_id',
    'insertion_group_id',
    'timestamp',
    'strategy',
]

big_file_size = 1

strategies = [
    "current version",
    "asyncio script wget (big file threshold size : {} Bytes)".format(big_file_size),
    "asyncio script wget (big file threshold size : {} Bytes)".format(big_file_size),
]

nb_strategies = len(strategies)

figs = make_subplots(
    rows=nb_strategies,
    cols=1,
    shared_xaxes=False,
    # vertical_spacing=0.05,
    subplot_titles=strategies,
)


figs.update_layout(
    title_text="Hardware : {} | Total Files size : {:5.2f} Mo".format(
        hardware,
        sizes * coeff_bytes_2_mo,
    ),
)


def alignment(start, end, min_date):
    delta = start.min() - min_date
    aligned_start = [date - delta for date in start]
    aligned_end = [date - delta for date in end]
    return aligned_start, aligned_end


min_start_date = datetime.datetime.strptime('2021-06-15 06:31:57.738044', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = []


data.extend(
    [
{'file_id': 29, 'status': 0, 'name': '4 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/ph/ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602056, 'expected_size': 135602056, 'duration': 1.002454, 'start_date': '2021-06-15 06:31:57.738044', 'end_date': '2021-06-15 06:31:58.740498', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 35, 'status': 0, 'name': '2 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/si/si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602100, 'expected_size': 135602100, 'duration': 1.001936, 'start_date': '2021-06-15 06:31:57.837241', 'end_date': '2021-06-15 06:31:58.839177', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 11, 'status': 0, 'name': '3 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602156, 'expected_size': 135602156, 'duration': 1.002079, 'start_date': '2021-06-15 06:31:57.932763', 'end_date': '2021-06-15 06:31:58.934842', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 15, 'status': 0, 'name': '0 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602216, 'expected_size': 135602216, 'duration': 1.002076, 'start_date': '2021-06-15 06:31:58.028954', 'end_date': '2021-06-15 06:31:59.031030', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 17, 'status': 0, 'name': '7 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602240, 'expected_size': 135602240, 'duration': 1.00188, 'start_date': '2021-06-15 06:31:58.124648', 'end_date': '2021-06-15 06:31:59.126528', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 26, 'status': 0, 'name': '1 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361464, 'expected_size': 337361464, 'duration': 1.00192, 'start_date': '2021-06-15 06:31:58.220665', 'end_date': '2021-06-15 06:31:59.222585', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},
{'file_id': 18, 'status': 0, 'name': '6 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361572, 'expected_size': 337361572, 'duration': 1.002006, 'start_date': '2021-06-15 06:31:58.318880', 'end_date': '2021-06-15 06:31:59.320886', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},
{'file_id': 14, 'status': 0, 'name': '5 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361576, 'expected_size': 337361576, 'duration': 1.002049, 'start_date': '2021-06-15 06:31:58.415531', 'end_date': '2021-06-15 06:31:59.417580', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},


   ]
)
downloading_duration = {
    'calculated from os': 53.054441,
    "start": "2021-06-07 12:30:35.492368",
    "end": "2021-06-07 12:31:28.546809",
}

for d in data:
    d["strategy"] = strategies[0]

current = pd.DataFrame(data, columns=columns)

current["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                         current["start_date"]]
current["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in current["end_date"]]

print(
    current["start_date"].min().strftime("%Y-%m-%d %H:%M:%S.%f"),
)
# dates alignment

current["start_date"], current["end_date"] = alignment(
    current["start_date"],
    current["end_date"],
    min_start_date,
)

current = current.sort_values(by=['size'])

current["size"] = current["size"] * coeff_bytes_2_go

color = '#ddd'

duration = (current["end_date"].max() - current["start_date"].min()).total_seconds()

current_duration = dict(
    duration=duration,
    # calculated_from_os=downloading_duration['calculated from os'],
    color=color,
)

# RUN STRATEGY : big file default chunksize

data = [

]

big_file_chunksize = 1

data.extend(
    [

  ]
)

big_file_chunksize = 1048576



data.extend(
    [
{'file_id': 29, 'status': 0, 'name': '4 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/ph/ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602056, 'expected_size': 135602056, 'duration': 1.002454, 'start_date': '2021-06-15 06:31:57.738044', 'end_date': '2021-06-15 06:31:58.740498', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 35, 'status': 0, 'name': '2 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/si/si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602100, 'expected_size': 135602100, 'duration': 1.001936, 'start_date': '2021-06-15 06:31:57.837241', 'end_date': '2021-06-15 06:31:58.839177', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 11, 'status': 0, 'name': '3 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602156, 'expected_size': 135602156, 'duration': 1.002079, 'start_date': '2021-06-15 06:31:57.932763', 'end_date': '2021-06-15 06:31:58.934842', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 15, 'status': 0, 'name': '0 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602216, 'expected_size': 135602216, 'duration': 1.002076, 'start_date': '2021-06-15 06:31:58.028954', 'end_date': '2021-06-15 06:31:59.031030', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 17, 'status': 0, 'name': '7 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602240, 'expected_size': 135602240, 'duration': 1.00188, 'start_date': '2021-06-15 06:31:58.124648', 'end_date': '2021-06-15 06:31:59.126528', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 26, 'status': 0, 'name': '1 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361464, 'expected_size': 337361464, 'duration': 1.00192, 'start_date': '2021-06-15 06:31:58.220665', 'end_date': '2021-06-15 06:31:59.222585', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},
{'file_id': 18, 'status': 0, 'name': '6 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361572, 'expected_size': 337361572, 'duration': 1.002006, 'start_date': '2021-06-15 06:31:58.318880', 'end_date': '2021-06-15 06:31:59.320886', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},
{'file_id': 14, 'status': 0, 'name': '5 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361576, 'expected_size': 337361576, 'duration': 1.002049, 'start_date': '2021-06-15 06:31:58.415531', 'end_date': '2021-06-15 06:31:59.417580', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},

    ]
)

for d in data:
    d["strategy"] = strategies[1]

asyncio_single_thread_strategy = pd.DataFrame(data, columns=columns)

asyncio_single_thread_strategy = asyncio_single_thread_strategy.sort_values(by=['size'])

# correction = asyncio_single_thread_strategy_db["download speed"].to_numpy() / asyncio_single_thread_strategy_db["download speed"].max()

asyncio_single_thread_strategy["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                                 asyncio_single_thread_strategy["start_date"]]
asyncio_single_thread_strategy["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                               asyncio_single_thread_strategy["end_date"]]

print(
    asyncio_single_thread_strategy["start_date"].min().strftime("%Y-%m-%d %H:%M:%S.%f"),
)

# dates alignment
asyncio_single_thread_strategy["start_date"], asyncio_single_thread_strategy["end_date"] = alignment(
    asyncio_single_thread_strategy["start_date"],
    asyncio_single_thread_strategy["end_date"],
    min_start_date,
)

# adf["duration"] = adf["duration"] * correction

asyncio_single_thread_strategy["size"] = asyncio_single_thread_strategy["size"] * coeff_bytes_2_go

duration = (asyncio_single_thread_strategy["end_date"].max() - asyncio_single_thread_strategy["start_date"].min()).total_seconds()

color = '#ff6666'

asyncio_single_thread_strategy_db_duration = dict(
    duration=duration,
    # calculated_from_os=downloading_duration['calculated from os'],
    color=color,
)

# DONWLOADS TIMELINE

fig = go.Figure()
fig.update_xaxes(title_text="Mo")
fig.update_yaxes(title_text="Elapsed time (in seconds)")
fig.update_layout(
    {
        "title": '{} Downloads ({} Mo)'.format(
            len(files),
            sizes * coeff_bytes_2_go,
        ),
    },
)


# # RUN STRATEGY : scheduler big file customized chunksize

data = [

]


data.extend(
    [
{'file_id': 29, 'status': 0, 'name': '3 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/ph/ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602056, 'expected_size': 135602056, 'duration': 1.00341, 'start_date': '2021-06-15 06:56:20.682062', 'end_date': '2021-06-15 06:56:21.685472', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/ph_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 35, 'status': 0, 'name': '7 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/si/si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602100, 'expected_size': 135602100, 'duration': 1.002054, 'start_date': '2021-06-15 06:56:20.782773', 'end_date': '2021-06-15 06:56:21.784827', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/si_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 11, 'status': 0, 'name': '4 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602156, 'expected_size': 135602156, 'duration': 1.001998, 'start_date': '2021-06-15 06:56:20.881028', 'end_date': '2021-06-15 06:56:21.883026', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 15, 'status': 0, 'name': '1 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602216, 'expected_size': 135602216, 'duration': 1.00195, 'start_date': '2021-06-15 06:56:20.976921', 'end_date': '2021-06-15 06:56:21.978871', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 17, 'status': 0, 'name': '0 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'observed_size': 135602240, 'expected_size': 135602240, 'duration': 1.002006, 'start_date': '2021-06-15 06:56:21.086158', 'end_date': '2021-06-15 06:56:22.088164', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'process_name': 'big file task'},
{'file_id': 26, 'status': 0, 'name': '5 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361464, 'expected_size': 337361464, 'duration': 1.002038, 'start_date': '2021-06-15 06:56:21.181872', 'end_date': '2021-06-15 06:56:22.183910', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},
{'file_id': 18, 'status': 0, 'name': '2 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361572, 'expected_size': 337361572, 'duration': 1.003441, 'start_date': '2021-06-15 06:56:21.276881', 'end_date': '2021-06-15 06:56:22.280322', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},
{'file_id': 14, 'status': 0, 'name': '6 , http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'observed_size': 337361576, 'expected_size': 337361576, 'duration': 1.002137, 'start_date': '2021-06-15 06:56:21.390701', 'end_date': '2021-06-15 06:56:22.392838', 'strategy': 'asyncio wget (script)', 'sdget_status': None, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'process_name': 'big file task'},

  ]
)
for d in data:
    d["strategy"] = strategies[2]

asyncio_multi_threads_strategy = pd.DataFrame(data, columns=columns)

asyncio_multi_threads_strategy = asyncio_multi_threads_strategy.sort_values(by=['size'])

asyncio_multi_threads_strategy["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                                 asyncio_multi_threads_strategy["start_date"]]
asyncio_multi_threads_strategy["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                               asyncio_multi_threads_strategy["end_date"]]

print(
    asyncio_multi_threads_strategy["start_date"].min().strftime("%Y-%m-%d %H:%M:%S.%f"),
)

# dates alignment
asyncio_multi_threads_strategy["start_date"], asyncio_multi_threads_strategy["end_date"] = alignment(
    asyncio_multi_threads_strategy["start_date"],
    asyncio_multi_threads_strategy["end_date"],
    min_start_date,
)

# adf["duration"] = adf["duration"] * correction

asyncio_multi_threads_strategy["size"] = asyncio_multi_threads_strategy["size"] * coeff_bytes_2_go

color = '#ff6666'

duration = (asyncio_multi_threads_strategy["end_date"].max() - asyncio_multi_threads_strategy["start_date"].min()).total_seconds()

asyncio_multi_threads_strategy_db_duration = dict(
    duration=duration,
    color=color,
)

# DONWLOADS TIMELINE

fig = go.Figure()
fig.update_xaxes(title_text="Mo")
fig.update_yaxes(title_text="Elapsed time (in seconds)")
fig.update_layout(
    {
        "title": '{} Downloads ({} Mo)'.format(
            len(files),
            sizes * coeff_bytes_2_go,
        ),
    },
)


VIEW_COLORS = {
    strategies[0]: 'rgb(120,120,120)',
    strategies[1]: 'rgb(120, 230, 120)',
    # strategies[2]: 'rgb(230, 120, 120)',
}

dmin = current["start_date"].min()
dmax = current["end_date"].max()

dmin = min(
    [
        dmin,
        asyncio_single_thread_strategy["start_date"].min(),
        asyncio_multi_threads_strategy["start_date"].min(),
    ],
)
dmax = max(
    [
        dmax,
        asyncio_single_thread_strategy["end_date"].max(),
        asyncio_multi_threads_strategy["end_date"].max(),
    ],
)

xrange = [dmin, dmax]

# current

row = 1
col = 1

current_fig = px.timeline(
    current,
    title="Downloads",
    x_start="start_date",
    x_end="end_date",
    y='file_id',
    color="strategy",
    color_discrete_map=VIEW_COLORS,
    text='duration',
    hover_data=dict(
        file_functional_id=True,
        size=True,
        start_date="|" + DATE_FORMAT,
        end_date="|" + DATE_FORMAT,
    ),

)

for trace in current_fig.data:
    figs.add_trace(trace, row=row, col=col)

figs.update_xaxes(type="date", range=xrange, row=row, col=col)
# figs.update_xaxes(type="date", row=row, col=col)

figs.update_yaxes(title_text="File", row=row, col=col)

# asyncio - aiohttp - DB

row = 2
col = 1

asyncio_fig = px.timeline(
    asyncio_single_thread_strategy,
    title="Downloads",
    x_start="start_date",
    x_end="end_date",
    y='file_id',
    color="strategy",
    color_discrete_map=VIEW_COLORS,
    text='duration',
    hover_data=dict(
        file_functional_id=True,
        size=True,
        start_date="|" + DATE_FORMAT,
        end_date="|" + DATE_FORMAT,
    ),
)

for trace in asyncio_fig.data:
    figs.add_trace(trace, row=row, col=col)

figs.update_xaxes(type="date", range=xrange, row=row, col=col)
# figs.update_xaxes(type="date", row=row, col=col)

figs.update_yaxes(title_text="File", row=row, col=col)

# STRATEGY : big file read

row = 3
col = 1

current_fig = px.timeline(
    asyncio_multi_threads_strategy,
    title="Downloads",
    x_start="start_date",
    x_end="end_date",
    y='file_id',
    color="strategy",
    color_discrete_map=VIEW_COLORS,
    text='duration',
    hover_data=dict(
        file_functional_id=True,
        size=True,
        start_date="|" + DATE_FORMAT,
        end_date="|" + DATE_FORMAT,
    ),
)

for trace in current_fig.data:
    figs.add_trace(trace, row=row, col=col)

figs.update_xaxes(type="date", range=xrange, row=row, col=col)
# figs.update_xaxes(type="date", row=row, col=col)

figs.update_yaxes(title_text="File", row=row, col=col)

titles = (
    '{} (duration : {} s)'.format(
        strategies[0],
        current_duration["duration"],
    ),
    '{} (duration : {} s)'.format(
        strategies[1],
        asyncio_single_thread_strategy_db_duration["duration"],
    ),
    '{} (duration : {} s)'.format(
        strategies[2],
        asyncio_multi_threads_strategy_db_duration["duration"],
    ),
)

# rotate all the subtitles of 90 degrees
for i, annotation in enumerate(figs['layout']['annotations']):
    annotation['text'] = titles[i]

figs.show()
