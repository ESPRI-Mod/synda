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

'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc': 86344659,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc': 88114316,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc': 795795708,






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


min_start_date = datetime.datetime.strptime('2021-06-11 22:30:19.913535', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = []


data.extend(
    [
{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 2.523913, 'size': 86344659, 'rate': 34210632.06219866, 'start_date': '2021-06-14 17:29:26.315015', 'end_date': '2021-06-14 17:29:28.838928', 'crea_date': '2021-06-14 17:29:10.838209', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 2.493127, 'size': 88114316, 'rate': 35342891.07614654, 'start_date': '2021-06-14 17:29:26.348101', 'end_date': '2021-06-14 17:29:28.841228', 'crea_date': '2021-06-14 17:29:10.858987', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 10.106789, 'size': 795795708, 'rate': 78738727.7996998, 'start_date': '2021-06-14 17:29:26.379545', 'end_date': '2021-06-14 17:29:36.486334', 'crea_date': '2021-06-14 17:29:10.864084', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
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

duration = (current["end_date"].max() - current["start_date"].min()).seconds

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
{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 1.401905, 'size': 86344659, 'rate': 61590948.744743764, 'start_date': '2021-06-14 17:31:04.393574', 'end_date': '2021-06-14 17:31:05.795479', 'crea_date': '2021-06-14 17:30:54.449308', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 1.709463, 'size': 88114316, 'rate': 51545026.713067204, 'start_date': '2021-06-14 17:31:04.549944', 'end_date': '2021-06-14 17:31:06.259407', 'crea_date': '2021-06-14 17:30:54.470677', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 6.629329, 'size': 795795708, 'rate': 120041667.56545043, 'start_date': '2021-06-14 17:31:04.716693', 'end_date': '2021-06-14 17:31:11.346022', 'crea_date': '2021-06-14 17:30:54.475998', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
    ]
)

big_file_chunksize = 1048576

data.extend(
    [

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

duration = (asyncio_single_thread_strategy["end_date"].max() - asyncio_single_thread_strategy["start_date"].min()).seconds

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
{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 1.401905, 'size': 86344659, 'rate': 61590948.744743764, 'start_date': '2021-06-14 17:31:04.393574', 'end_date': '2021-06-14 17:31:05.795479', 'crea_date': '2021-06-14 17:30:54.449308', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 1.709463, 'size': 88114316, 'rate': 51545026.713067204, 'start_date': '2021-06-14 17:31:04.549944', 'end_date': '2021-06-14 17:31:06.259407', 'crea_date': '2021-06-14 17:30:54.470677', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 6.629329, 'size': 795795708, 'rate': 120041667.56545043, 'start_date': '2021-06-14 17:31:04.716693', 'end_date': '2021-06-14 17:31:11.346022', 'crea_date': '2021-06-14 17:30:54.475998', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},

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

duration = (asyncio_multi_threads_strategy["end_date"].max() - asyncio_multi_threads_strategy["start_date"].min()).seconds

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
