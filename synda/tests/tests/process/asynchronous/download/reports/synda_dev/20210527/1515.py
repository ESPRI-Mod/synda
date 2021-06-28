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
    'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc': 47212396,
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
    "small file",
]


figs = make_subplots(
    rows=4,
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


min_start_date = datetime.datetime.strptime('2021-05-04 11:28:07.778940', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = [

    {'file_id': 1,
     'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62',
     'checksum_type': 'sha256', 'duration': 8.396576, 'size': 47212396, 'rate': 5622815.299950837,
     'start_date': '2021-05-28 14:55:40.579153', 'end_date': '2021-05-28 14:55:48.975729',
     'crea_date': '2021-05-28 14:53:51.087421', 'status': 'done', 'error_msg': '', 'sdget_status': '0',
     'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2',
     'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1,
     'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.155084, 'size': 47212396, 'rate': 7670471.434670916, 'start_date': '2021-05-28 15:32:39.272041', 'end_date': '2021-05-28 15:32:45.427125', 'crea_date': '2021-05-28 15:32:27.873881', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.395242, 'size': 47212396, 'rate': 8750746.676423412, 'start_date': '2021-05-28 15:47:13.631461', 'end_date': '2021-05-28 15:47:19.026703', 'crea_date': '2021-05-28 15:47:03.454960', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.241282, 'size': 47212396, 'rate': 9007795.421043936, 'start_date': '2021-05-28 16:35:55.800313', 'end_date': '2021-05-28 16:36:01.041595', 'crea_date': '2021-05-28 16:35:42.787472', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.059473, 'size': 47212396, 'rate': 7791502.000256458, 'start_date': '2021-05-28 16:45:00.492963', 'end_date': '2021-05-28 16:45:06.552436', 'crea_date': '2021-05-28 16:44:51.615808', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.299159, 'size': 47212396, 'rate': 7495031.638350452, 'start_date': '2021-05-28 17:02:44.685158', 'end_date': '2021-05-28 17:02:50.984317', 'crea_date': '2021-05-28 17:00:19.697295', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.5842, 'size': 47212396, 'rate': 8454639.160488522, 'start_date': '2021-05-28 17:30:49.648858', 'end_date': '2021-05-28 17:30:55.233058', 'crea_date': '2021-05-28 17:30:44.631669', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.611622, 'size': 47212396, 'rate': 8413324.347220821, 'start_date': '2021-05-28 17:33:36.530165', 'end_date': '2021-05-28 17:33:42.141787', 'crea_date': '2021-05-28 17:33:15.576389', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.605603, 'size': 47212396, 'rate': 8422358.129892537, 'start_date': '2021-05-28 17:49:13.648462', 'end_date': '2021-05-28 17:49:19.254065', 'crea_date': '2021-05-28 17:49:04.125375', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.202001, 'size': 47212396, 'rate': 7612445.725178052, 'start_date': '2021-05-28 17:51:19.444780', 'end_date': '2021-05-28 17:51:25.646781', 'crea_date': '2021-05-28 17:50:59.850349', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},


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

    {'file_id': 1,
     'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62',
     'checksum_type': 'sha256', 'duration': 5.87478, 'size': 47212396, 'rate': 8036453.450171751,
     'start_date': '2021-05-26 17:19:53.465596', 'end_date': '2021-05-26 17:19:59.566240',
     'crea_date': '2021-05-26 17:19:44.312043', 'status': 'done', 'error_msg': '', 'sdget_status': '0',
     'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2',
     'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1,
     'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 2,
     'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62',
     'checksum_type': 'sha256', 'duration': 6.205918, 'size': 47212396, 'rate': 7607640.964640526,
     'start_date': '2021-05-28 15:00:23.230821', 'end_date': '2021-05-28 15:00:29.675768',
     'crea_date': '2021-05-28 14:59:43.096783', 'status': 'done', 'error_msg': '', 'sdget_status': '0',
     'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2',
     'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1,
     'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.232789, 'size': 47212396, 'rate': 7574842.658719876, 'start_date': '2021-05-28 15:45:16.545888', 'end_date': '2021-05-28 15:45:23.077352', 'crea_date': '2021-05-28 15:45:08.510024', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.91802, 'size': 47212396, 'rate': 9599878.813018247, 'start_date': '2021-05-28 16:31:29.649492', 'end_date': '2021-05-28 16:31:34.792974', 'crea_date': '2021-05-28 16:31:25.242393', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.162726, 'size': 47212396, 'rate': 11341701.567674644, 'start_date': '2021-05-28 16:43:14.859923', 'end_date': '2021-05-28 16:43:19.246282', 'crea_date': '2021-05-28 16:43:09.180269', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.257011, 'size': 47212396, 'rate': 7545519.098496071, 'start_date': '2021-05-28 17:07:03.954978', 'end_date': '2021-05-28 17:07:10.435663', 'crea_date': '2021-05-28 17:06:58.475623', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.059244, 'size': 47212396, 'rate': 7791796.468338295, 'start_date': '2021-05-28 17:27:04.191574', 'end_date': '2021-05-28 17:27:10.475777', 'crea_date': '2021-05-28 17:26:50.284038', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.755554, 'size': 47212396, 'rate': 8202928.162953557, 'start_date': '2021-05-28 17:38:07.077253', 'end_date': '2021-05-28 17:38:13.056736', 'crea_date': '2021-05-28 17:37:50.802582', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.331624, 'size': 47212396, 'rate': 10899467.728500905, 'start_date': '2021-05-28 17:45:22.191410', 'end_date': '2021-05-28 17:45:26.747849', 'crea_date': '2021-05-28 17:45:15.561429', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.246545, 'size': 47212396, 'rate': 8998759.374026144, 'start_date': '2021-05-28 18:04:22.172319', 'end_date': '2021-05-28 18:04:27.643698', 'crea_date': '2021-05-28 18:04:17.604726', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
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

    {'file_id': 1,
     'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62',
     'checksum_type': 'sha256', 'duration': 4.299734, 'size': 47212396, 'rate': 10980306.223594297,
     'start_date': '2021-05-28 11:29:59.387441', 'end_date': '2021-05-28 11:30:03.918139',
     'crea_date': '2021-05-28 11:29:51.953125', 'status': 'done', 'error_msg': '', 'sdget_status': '0',
     'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2',
     'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1,
     'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.577082, 'size': 47212396, 'rate': 7178319.503998886, 'start_date': '2021-05-28 15:26:45.617170', 'end_date': '2021-05-28 15:26:52.417758', 'crea_date': '2021-05-28 15:26:35.028566', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 7.105791, 'size': 47212396, 'rate': 6644213.993910038, 'start_date': '2021-05-28 15:43:20.798543', 'end_date': '2021-05-28 15:43:28.130903', 'crea_date': '2021-05-28 15:43:06.210317', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.417951, 'size': 47212396, 'rate': 10686491.543251611, 'start_date': '2021-05-28 16:28:41.654253', 'end_date': '2021-05-28 16:28:46.298166', 'crea_date': '2021-05-28 16:28:25.563106', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.611284, 'size': 47212396, 'rate': 8413831.1302725, 'start_date': '2021-05-28 16:41:21.906160', 'end_date': '2021-05-28 16:41:27.740337', 'crea_date': '2021-05-28 16:41:11.256524', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.811867, 'size': 47212396, 'rate': 8123447.422317131, 'start_date': '2021-05-28 17:12:33.521858', 'end_date': '2021-05-28 17:12:39.561048', 'crea_date': '2021-05-28 17:12:26.209348', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.172623, 'size': 47212396, 'rate': 9127360.722016664, 'start_date': '2021-05-28 17:25:01.310436', 'end_date': '2021-05-28 17:25:06.706817', 'crea_date': '2021-05-28 17:24:52.709923', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.652349, 'size': 47212396, 'rate': 7097101.490015031, 'start_date': '2021-05-28 17:39:35.153840', 'end_date': '2021-05-28 17:39:42.036695', 'crea_date': '2021-05-28 17:39:27.973118', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.165234, 'size': 47212396, 'rate': 7657843.319491198, 'start_date': '2021-05-28 17:43:32.170873', 'end_date': '2021-05-28 17:43:38.563495', 'crea_date': '2021-05-28 17:43:24.529953', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.186525, 'size': 47212396, 'rate': 7631488.759844986, 'start_date': '2021-05-28 17:58:30.047381', 'end_date': '2021-05-28 17:58:36.462573', 'crea_date': '2021-05-28 17:58:24.626462', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},

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

# RUN STRATEGY : small file

data = [

    {'file_id': 1,
     'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
     'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62',
     'checksum_type': 'sha256', 'duration': 6.127862, 'size': 47212396, 'rate': 7704546.218566932,
     'start_date': '2021-05-28 14:40:28.652046', 'end_date': '2021-05-28 14:40:35.004767',
     'crea_date': '2021-05-28 14:40:11.032392', 'status': 'done', 'error_msg': '', 'sdget_status': '0',
     'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2',
     'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1,
     'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.256607, 'size': 47212396, 'rate': 11091556.255956916, 'start_date': '2021-05-28 15:29:56.377870', 'end_date': '2021-05-28 15:30:00.866343', 'crea_date': '2021-05-28 15:29:47.894907', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 5.097173, 'size': 47212396, 'rate': 9262466.861532854, 'start_date': '2021-05-28 15:40:43.013033', 'end_date': '2021-05-28 15:40:48.335768', 'crea_date': '2021-05-28 15:40:07.026079', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.430241, 'size': 47212396, 'rate': 10656845.981968025, 'start_date': '2021-05-28 16:33:43.476424', 'end_date': '2021-05-28 16:33:48.134767', 'crea_date': '2021-05-28 16:33:37.216303', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.434636, 'size': 47212396, 'rate': 10646284.385009276, 'start_date': '2021-05-28 16:38:55.174591', 'end_date': '2021-05-28 16:38:59.833725', 'crea_date': '2021-05-28 16:38:45.206015', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.360694, 'size': 47212396, 'rate': 10826807.842971785, 'start_date': '2021-05-28 17:09:38.629048', 'end_date': '2021-05-28 17:09:43.214727', 'crea_date': '2021-05-28 17:09:25.950752', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.212045, 'size': 47212396, 'rate': 11208901.139470259, 'start_date': '2021-05-28 17:28:56.250289', 'end_date': '2021-05-28 17:29:00.687653', 'crea_date': '2021-05-28 17:28:46.921172', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.454822, 'size': 47212396, 'rate': 10598043.199032418, 'start_date': '2021-05-28 17:35:54.831881', 'end_date': '2021-05-28 17:35:59.511932', 'crea_date': '2021-05-28 17:35:15.114577', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 6.216212, 'size': 47212396, 'rate': 7595042.768811618, 'start_date': '2021-05-28 17:47:16.269992', 'end_date': '2021-05-28 17:47:22.709741', 'crea_date': '2021-05-28 17:47:08.168814', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
    {'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 4.805249, 'size': 47212396, 'rate': 9825171.598807888, 'start_date': '2021-05-28 18:06:40.193426', 'end_date': '2021-05-28 18:06:45.222316', 'crea_date': '2021-05-28 18:06:32.194846', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},


]

for d in data:
    d["strategy"] = strategies[3]

small_file_read_strategy = pd.DataFrame(data, columns=columns)

small_file_read_strategy = small_file_read_strategy.sort_values(by=['size'])

# correction = small_file_read_strategy_db["download speed"].to_numpy() / small_file_read_strategy_db["download speed"].max()

small_file_read_strategy["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                                 small_file_read_strategy["start_date"]]
small_file_read_strategy["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
                               small_file_read_strategy["end_date"]]

# dates alignment
small_file_read_strategy["start_date"], small_file_read_strategy["end_date"] = alignment(
    small_file_read_strategy["start_date"],
    small_file_read_strategy["end_date"],
    min_start_date,
)

# adf["duration"] = adf["duration"] * correction

small_file_read_strategy["size"] = small_file_read_strategy["size"] * coeff_bytes_2_go

color = '#ff6666'

small_file_read_strategy_db_duration = dict(
    duration=small_file_read_strategy["duration"].mean(),
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
    strategies[3]: 'rgb(120, 120, 230)',
}

dmin = current["start_date"].min()
dmax = current["end_date"].max()

dmin = min(
    [
        dmin,
        big_file_default_chunk_size_strategy["start_date"].min(),
        big_file_customized_chunk_size_strategy["start_date"].min(),
        small_file_read_strategy["start_date"].min(),
    ],
)
dmax = max(
    [
        dmax,
        big_file_default_chunk_size_strategy["end_date"].max(),
        big_file_customized_chunk_size_strategy["end_date"].max(),
        small_file_read_strategy["end_date"].max(),
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


# STRATEGY : small file

row = 4
col = 1

current_fig = px.timeline(
    small_file_read_strategy,
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
    '{} (mean : {} s)'.format(
        strategies[3],
        small_file_read_strategy_db_duration["duration"],
    ),
)

# rotate all the subtitles of 90 degrees
for i, annotation in enumerate(figs['layout']['annotations']):
    annotation['text'] = titles[i]

figs.show()
