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

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

durations = []

# install -s /home_local/journoud/DEV/WORKSPACES/synda/selection/sample/sample_selection_01_bis.txt
# Observations

files = {

'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc': 47212396,

}


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

big_file_size = 78675404
big_file_chunksize = 16384

strategies = [
    "current version",
    "small & big file (threshold size : {} Bytes,  server-side chunk size)".format(big_file_size),
    "small & big file (threshold size : {} Bytes,  customized chunk size : {} Bytes)".format(
        big_file_size,
        big_file_chunksize,
    ),
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
    title_text="Same file downloaded ten times for each stratégy | File size : {:5.2f} Mo".format(
        sizes * coeff_bytes_2_mo,
    ),
)


def alignment(start, end, min_date):
    delta = start.min() - min_date
    aligned_start = [date - delta for date in start]
    aligned_end = [date - delta for date in end]
    return aligned_start, aligned_end


min_start_date = datetime.datetime.strptime('2021-06-07 09:25:24.816623', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = [

{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 34.171327, 'size': 47212396, 'rate': 1381637.7689985526, 'start_date': '2021-06-07 09:54:18.904911', 'end_date': '2021-06-07 09:54:53.076238', 'crea_date': '2021-06-07 09:54:07.998581', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'}

]

downloading_duration = {
    'calculated from os': 0.000114,
    "start": "2021-06-07 09:54:40.906789",
    "end": "2021-06-07 09:54:40.906903",
}

# data.extend(
#     [
# {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 44.711363, 'size': 86344659, 'rate': 1931156.9410219053, 'start_date': '2021-06-07 09:25:35.750337', 'end_date': '2021-06-07 09:26:20.461700', 'crea_date': '2021-06-07 09:25:04.373959', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
# {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 43.48877, 'size': 88114316, 'rate': 2026139.5298142484, 'start_date': '2021-06-07 09:25:36.227683', 'end_date': '2021-06-07 09:26:19.716453', 'crea_date': '2021-06-07 09:25:04.377870', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
# {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 80.000784, 'size': 795795708, 'rate': 9947348.865981113, 'start_date': '2021-06-07 09:25:53.528719', 'end_date': '2021-06-07 09:27:13.529503', 'crea_date': '2021-06-07 09:25:04.379479', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
# {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 27.545397, 'size': 27452120, 'rate': 996613.6991962758, 'start_date': '2021-06-07 09:25:24.816623', 'end_date': '2021-06-07 09:25:52.362020', 'crea_date': '2021-06-07 09:25:04.381167', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
# {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 41.586971, 'size': 138080132, 'rate': 3320273.84249745, 'start_date': '2021-06-07 09:25:46.570165', 'end_date': '2021-06-07 09:26:28.157136', 'crea_date': '2021-06-07 09:25:04.382743', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
# {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 70.551801, 'size': 337361584, 'rate': 4781757.222611511, 'start_date': '2021-06-07 09:25:49.518283', 'end_date': '2021-06-07 09:27:00.070084', 'crea_date': '2021-06-07 09:25:04.384448', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},
#
#    ]
# )

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

duration = (current["end_date"].max() - current["start_date"].min()).seconds

current_duration = dict(
    duration=duration,
    calculated_from_os=downloading_duration['calculated from os'],
    color=color,
)

# RUN STRATEGY : big file default chunksize

data = [

{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 34.171327, 'size': 47212396, 'rate': 1381637.7689985526, 'start_date': '2021-06-07 09:54:18.904911', 'end_date': '2021-06-07 09:54:53.076238', 'crea_date': '2021-06-07 09:54:07.998581', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'}

]

downloading_duration = {
    'calculated from os': 0.000114,
    "start": "2021-06-07 09:54:40.906789",
    "end": "2021-06-07 09:54:40.906903",
}

# data.extend(
#     [
#
#     ]
# )
#
# downloading_duration = {
#     'calculated from os': 82.082709,
#     "start": "2021-06-07 09:25:35.518941",
#     "end": "2021-06-07 09:25:35.518941",
# }

for d in data:
    d["strategy"] = strategies[1]

big_file_default_chunk_size_strategy = pd.DataFrame(data, columns=columns)

big_file_default_chunk_size_strategy = big_file_default_chunk_size_strategy.sort_values(by=['size'])

# correction = big_file_default_chunk_size_strategy_db["download speed"].to_numpy() / big_file_default_chunk_size_strategy_db["download speed"].max()

big_file_default_chunk_size_strategy["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                                 big_file_default_chunk_size_strategy["start_date"]]
big_file_default_chunk_size_strategy["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                               big_file_default_chunk_size_strategy["end_date"]]

print(
    big_file_default_chunk_size_strategy["start_date"].min().strftime("%Y-%m-%d %H:%M:%S.%f"),
)

# dates alignment
big_file_default_chunk_size_strategy["start_date"], big_file_default_chunk_size_strategy["end_date"] = alignment(
    big_file_default_chunk_size_strategy["start_date"],
    big_file_default_chunk_size_strategy["end_date"],
    min_start_date,
)

# adf["duration"] = adf["duration"] * correction

big_file_default_chunk_size_strategy["size"] = big_file_default_chunk_size_strategy["size"] * coeff_bytes_2_go

duration = (big_file_default_chunk_size_strategy["end_date"].max() - big_file_default_chunk_size_strategy["start_date"].min()).seconds

color = '#ff6666'

big_file_default_chunk_size_strategy_db_duration = dict(
    duration=duration,
    calculated_from_os=downloading_duration['calculated from os'],
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


# RUN STRATEGY : big file customized chunksize

data = [

{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 34.171327, 'size': 47212396, 'rate': 1381637.7689985526, 'start_date': '2021-06-07 09:54:18.904911', 'end_date': '2021-06-07 09:54:53.076238', 'crea_date': '2021-06-07 09:54:07.998581', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'}

]

downloading_duration = {
    'calculated from os': 0.000114,
    "start": "2021-06-07 09:54:40.906789",
    "end": "2021-06-07 09:54:40.906903",
}

for d in data:
    d["strategy"] = strategies[2]

big_file_customized_chunk_size_strategy = pd.DataFrame(data, columns=columns)

big_file_customized_chunk_size_strategy = big_file_customized_chunk_size_strategy.sort_values(by=['size'])

big_file_customized_chunk_size_strategy["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                                 big_file_customized_chunk_size_strategy["start_date"]]
big_file_customized_chunk_size_strategy["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                               big_file_customized_chunk_size_strategy["end_date"]]

print(
    big_file_customized_chunk_size_strategy["start_date"].min().strftime("%Y-%m-%d %H:%M:%S.%f"),
)

# dates alignment
big_file_customized_chunk_size_strategy["start_date"], big_file_customized_chunk_size_strategy["end_date"] = alignment(
    big_file_customized_chunk_size_strategy["start_date"],
    big_file_customized_chunk_size_strategy["end_date"],
    min_start_date,
)

# adf["duration"] = adf["duration"] * correction

big_file_customized_chunk_size_strategy["size"] = big_file_customized_chunk_size_strategy["size"] * coeff_bytes_2_go

color = '#ff6666'

duration = (big_file_customized_chunk_size_strategy["end_date"].max() - big_file_customized_chunk_size_strategy["start_date"].min()).seconds

big_file_customized_chunk_size_strategy_db_duration = dict(
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
    strategies[2]: 'rgb(230, 120, 120)',
}

dmin = current["start_date"].min()
dmax = current["end_date"].max()

dmin = min(
    [
        dmin,
        big_file_default_chunk_size_strategy["start_date"].min(),
        big_file_customized_chunk_size_strategy["start_date"].min(),
    ],
)
dmax = max(
    [
        dmax,
        big_file_default_chunk_size_strategy["end_date"].max(),
        big_file_customized_chunk_size_strategy["end_date"].max(),
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
    big_file_default_chunk_size_strategy,
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
    big_file_customized_chunk_size_strategy,
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
    '{} (duration : {} s / calculated from os :  {} s)'.format(
        strategies[0],
        current_duration["duration"],
        current_duration['calculated_from_os'],
    ),
    '{} (duration : {} s / calculated from os :  {} s)'.format(
        strategies[1],
        big_file_default_chunk_size_strategy_db_duration["duration"],
        big_file_default_chunk_size_strategy_db_duration['calculated_from_os'],
    ),
    '{} (duration : {} s)'.format(
        strategies[2],
        big_file_customized_chunk_size_strategy_db_duration["duration"],
    ),
)

# rotate all the subtitles of 90 degrees
for i, annotation in enumerate(figs['layout']['annotations']):
    annotation['text'] = titles[i]

figs.show()
