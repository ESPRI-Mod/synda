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
    'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc': 5545240276,
}

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

strategies = [
    "current version",
    "big file default chunk size",
    "big file customized chunk size",
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
        list(
            files.values(),
        )[0] * coeff_bytes_2_mo,
    ),
)


def alignment(start, end, min_date):
    aligned_start = []
    aligned_end = []
    for wstart, wend in zip(start, end):
        delta = wstart - min_date
        aligned_start.append(wstart - delta)
        aligned_end.append(wend - delta)
    return aligned_start, aligned_end


min_start_date = datetime.datetime.strptime('2021-05-31 11:44:39.117356', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = [
    {'file_id': 2,
     'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc',
     'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc',
     'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc',
     'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc',
     'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673',
     'checksum_type': 'sha256', 'duration': 337.586355, 'size': 5545240276, 'rate': 16426138.657174101,
     'start_date': '2021-05-31 11:58:36.097056', 'end_date': '2021-05-31 12:04:13.683411',
     'crea_date': '2021-05-31 11:58:29.123437', 'status': 'done', 'error_msg': '', 'sdget_status': '0',
     'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4',
     'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1,
     'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},
{'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673', 'checksum_type': 'sha256', 'duration': 315.067796, 'size': 5545240276, 'rate': 17600149.384991415, 'start_date': '2021-05-31 12:07:51.249090', 'end_date': '2021-05-31 12:13:06.316886', 'crea_date': '2021-05-31 12:07:32.775326', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4', 'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},
{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673', 'checksum_type': 'sha256', 'duration': 337.228961, 'size': 5545240276, 'rate': 16443547.01789684, 'start_date': '2021-05-31 11:44:39.117356', 'end_date': '2021-05-31 11:50:16.346317', 'crea_date': '2021-05-31 11:44:31.663208', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4', 'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},

]


for d in data:
    d["strategy"] = strategies[0]

current = pd.DataFrame(data, columns=columns)

current["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                         current["start_date"]]
current["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in current["end_date"]]

# dates alignment

current["start_date"], current["end_date"] = alignment(
    current["start_date"],
    current["end_date"],
    min_start_date,
)

current = current.sort_values(by=['size'])

current["size"] = current["size"] * coeff_bytes_2_go

color = '#ddd'

current_duration = dict(
    duration=current["duration"].mean(),
    color=color,
)

# RUN STRATEGY : big file default chunksize

data = [

{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673', 'checksum_type': 'sha256', 'duration': 299.881455, 'size': 5545240276, 'rate': 18491441.146302294, 'start_date': '2021-05-31 12:44:11.426811', 'end_date': '2021-05-31 12:49:11.308266', 'crea_date': '2021-05-31 12:43:58.899782', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4', 'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},
{'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673', 'checksum_type': 'sha256', 'duration': 303.063585, 'size': 5545240276, 'rate': 18297283.31102531, 'start_date': '2021-05-31 12:55:58.240511', 'end_date': '2021-05-31 13:01:01.304096', 'crea_date': '2021-05-31 12:55:46.903523', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4', 'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},
{'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673', 'checksum_type': 'sha256', 'duration': 439.230212, 'size': 5545240276, 'rate': 12624906.312227903, 'start_date': '2021-05-31 15:29:43.061242', 'end_date': '2021-05-31 15:37:02.291454', 'crea_date': '2021-05-31 15:29:27.620726', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4', 'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},


]

for d in data:
    d["strategy"] = strategies[1]

big_file_default_chunk_size_strategy = pd.DataFrame(data, columns=columns)

big_file_default_chunk_size_strategy = big_file_default_chunk_size_strategy.sort_values(by=['size'])

# correction = big_file_default_chunk_size_strategy_db["download speed"].to_numpy() / big_file_default_chunk_size_strategy_db["download speed"].max()

big_file_default_chunk_size_strategy["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                                 big_file_default_chunk_size_strategy["start_date"]]
big_file_default_chunk_size_strategy["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                               big_file_default_chunk_size_strategy["end_date"]]

# dates alignment
big_file_default_chunk_size_strategy["start_date"], big_file_default_chunk_size_strategy["end_date"] = alignment(
    big_file_default_chunk_size_strategy["start_date"],
    big_file_default_chunk_size_strategy["end_date"],
    min_start_date,
)

# adf["duration"] = adf["duration"] * correction

big_file_default_chunk_size_strategy["size"] = big_file_default_chunk_size_strategy["size"] * coeff_bytes_2_go

color = '#ff6666'

big_file_default_chunk_size_strategy_db_duration = dict(
    duration=big_file_default_chunk_size_strategy["duration"].mean(),
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

{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673', 'checksum_type': 'sha256', 'duration': 322.423069, 'size': 5545240276, 'rate': 17198646.155185625, 'start_date': '2021-05-31 12:29:52.380472', 'end_date': '2021-05-31 12:35:14.803541', 'crea_date': '2021-05-31 12:29:44.438074', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4', 'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},
{'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673', 'checksum_type': 'sha256', 'duration': 289.123247, 'size': 5545240276, 'rate': 19179503.3209488, 'start_date': '2021-05-31 13:03:16.166065', 'end_date': '2021-05-31 13:08:05.289312', 'crea_date': '2021-05-31 13:03:04.094250', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4', 'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},
{'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-MR.1pctCO2.day.ocean.day.r1i1p1.v20111119.omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'filename': 'omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-MR/1pctCO2/day/ocean/day/r1i1p1/v20111119/omldamax/omldamax_day_IPSL-CM5A-MR_1pctCO2_r1i1p1_18500101-19891231.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '68f40e5fe4081075b20d2d2ab1c704ade4a89c7419b9daaf4b5d8c4ecbc7d673', 'checksum_type': 'sha256', 'duration': 289.794983, 'size': 5545240276, 'rate': 19135045.81271512, 'start_date': '2021-05-31 15:07:29.179754', 'end_date': '2021-05-31 15:12:18.974737', 'crea_date': '2021-05-31 15:04:16.523284', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'cb9f173b-e5a7-496c-9f57-42251203caa4', 'model': 'IPSL-CM5A-MR', 'project': 'CMIP5', 'variable': 'omldamax', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2011-10-30T20:40:07Z'},

]

for d in data:
    d["strategy"] = strategies[2]

big_file_customized_chunk_size_strategy = pd.DataFrame(data, columns=columns)

big_file_customized_chunk_size_strategy = big_file_customized_chunk_size_strategy.sort_values(by=['size'])

big_file_customized_chunk_size_strategy["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                                 big_file_customized_chunk_size_strategy["start_date"]]
big_file_customized_chunk_size_strategy["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                               big_file_customized_chunk_size_strategy["end_date"]]

# dates alignment
big_file_customized_chunk_size_strategy["start_date"], big_file_customized_chunk_size_strategy["end_date"] = alignment(
    big_file_customized_chunk_size_strategy["start_date"],
    big_file_customized_chunk_size_strategy["end_date"],
    min_start_date,
)

# adf["duration"] = adf["duration"] * correction

big_file_customized_chunk_size_strategy["size"] = big_file_customized_chunk_size_strategy["size"] * coeff_bytes_2_go

color = '#ff6666'

big_file_customized_chunk_size_strategy_db_duration = dict(
    duration=big_file_customized_chunk_size_strategy["duration"].mean(),
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
    '{} (mean : {} s)'.format(
        strategies[0],
        current_duration["duration"],
    ),
    '{} (mean : {} s)'.format(
        strategies[1],
        big_file_default_chunk_size_strategy_db_duration["duration"],
    ),
    '{} (mean : {} s)'.format(
        strategies[2],
        big_file_customized_chunk_size_strategy_db_duration["duration"],
    ),
)

# rotate all the subtitles of 90 degrees
for i, annotation in enumerate(figs['layout']['annotations']):
    annotation['text'] = titles[i]

figs.show()
