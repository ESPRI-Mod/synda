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


# install -s /home_local/journoud/DEV/WORKSPACES/synda/selection/sample/sample_selection_01_bis.txt

durations = []


# Observations

files = {
    'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc': 47212396,

}

sizes = 0
for key in files.keys():
    sizes += files[key]

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

figs = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=False,
    # vertical_spacing=0.05,
    subplot_titles=(
        'synda current version',
        'synda new version',
    ),
)

# # RUN current synda version 3.2

data = [

{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 59.528319, 'size': 47212396, 'rate': 793108.1675597122, 'start_date': '2021-04-29 12:26:16.129529', 'end_date': '2021-04-29 12:27:15.657848', 'crea_date': '2021-04-29 12:26:01.575110', 'status': 'done', 'error_msg': '', 'sdget_status': 0, 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
]

strategy = "current version"

for d in data:
    d["strategy"] = strategy

current = pd.DataFrame(data, columns=columns)

current["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in current["start_date"]]
current["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in current["end_date"]]

current = current.sort_values(by=['size'])

current["size"] = current["size"] * coeff_bytes_2_go

color = '#ddd'

current_duration = dict(
    duration=current["duration"].max(),
    color=color,
)


# RUN asyncio aiohttp code

data = [

{'file_id': 1, 'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'size': 47212396, 'duration': 44.4346, 'waiting_times': 44.417783, 'writing_times': 0.01609, 'start_date': '2021-04-26 11:31:05.038960', 'end_date': '2021-04-26 11:31:49.473560', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'small file task'},
]


asyncio_aiohttp = pd.DataFrame(data, columns=columns)

asyncio_aiohttp = asyncio_aiohttp.sort_values(by=['size'])

# correction = asyncio_aiohttp["download speed"].to_numpy() / asyncio_aiohttp["download speed"].max()

asyncio_aiohttp["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in asyncio_aiohttp["start_date"]]
asyncio_aiohttp["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in asyncio_aiohttp["end_date"]]

# adf["duration"] = adf["duration"] * correction

asyncio_aiohttp["size"] = asyncio_aiohttp["size"] * coeff_bytes_2_go

color = '#ff6666'

asyncio_aiohttp_duration = dict(
    duration=asyncio_aiohttp["duration"].max(),
    color=color,
)


# RUN asyncio aiohttp DB

data = [

{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 44.52556, 'size': 47212396, 'rate': 1060343.6767555536, 'start_date': '2021-04-26 11:31:04.948469', 'end_date': '2021-04-26 11:31:49.581375', 'crea_date': '2021-04-26 11:30:45.891968', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},

]

strategy = "new version DB"

for d in data:
    d["strategy"] = strategy

asyncio_aiohttp_db = pd.DataFrame(data, columns=columns)

asyncio_aiohttp_db = asyncio_aiohttp_db.sort_values(by=['size'])

# correction = asyncio_aiohttp_db["download speed"].to_numpy() / asyncio_aiohttp_db["download speed"].max()

asyncio_aiohttp_db["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in asyncio_aiohttp_db["start_date"]]
asyncio_aiohttp_db["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in asyncio_aiohttp_db["end_date"]]

# adf["duration"] = adf["duration"] * correction

asyncio_aiohttp_db["size"] = asyncio_aiohttp_db["size"] * coeff_bytes_2_go

color = '#ff6666'

asyncio_aiohttp_db_duration = dict(
    duration=asyncio_aiohttp_db["duration"].max(),
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
 'sequential': 'rgb(0,0,0)',
 'current version': 'rgb(120,120,120)',
 'asyncio aiohttp': 'rgb(31, 230, 0)',
 'new version DB': 'rgb(120, 230, 120)',

}

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
)

for trace in current_fig.data:
    figs.add_trace(trace, row=row, col=col)

figs.update_xaxes(type="date", row=row, col=col)

figs.update_yaxes(title_text="File", row=row, col=col)

# asyncio - aiohttp - DB

row = 2
col = 1

asyncio_fig = px.timeline(
 asyncio_aiohttp_db,
 title="Downloads",
 x_start="start_date",
 x_end="end_date",
 y='file_id',
 color="strategy",
 color_discrete_map=VIEW_COLORS,
 text='duration',
)

for trace in asyncio_fig.data:
    figs.add_trace(trace, row=row, col=col)

figs.update_xaxes(type="date", row=row, col=col)

figs.update_yaxes(title_text="File", row=row, col=col)


titles = (
 'synda current version ({} s)'.format(current_duration["duration"]),
 'synda new version ({} s)'.format(asyncio_aiohttp_db_duration["duration"]),
)

# rotate all the subtitles of 90 degrees
for i, annotation in enumerate(figs['layout']['annotations']):
    annotation['text'] = titles[i]

figs.show()
