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
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc': 47212396,
'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc': 47212396,

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


min_start_date = datetime.datetime.strptime('2021-06-07 12:06:25.898498', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = [

# {'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 13.654992, 'size': 47212396, 'rate': 3457519.1256062253, 'start_date': '2021-06-07 12:19:57.177422', 'end_date': '2021-06-07 12:20:10.832414', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 16.095962, 'size': 47212396, 'rate': 2933182.6205852125, 'start_date': '2021-06-07 12:19:57.196670', 'end_date': '2021-06-07 12:20:13.292632', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 19.16622, 'size': 47212396, 'rate': 2463312.8493777076, 'start_date': '2021-06-07 12:19:57.205352', 'end_date': '2021-06-07 12:20:16.371572', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 48.960666, 'size': 47212396, 'rate': 964292.3566440047, 'start_date': '2021-06-07 12:19:57.213776', 'end_date': '2021-06-07 12:20:46.174442', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 44.69077, 'size': 47212396, 'rate': 1056423.8655990935, 'start_date': '2021-06-07 12:19:57.222361', 'end_date': '2021-06-07 12:20:41.913131', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 26.251026, 'size': 47212396, 'rate': 1798497.1711200927, 'start_date': '2021-06-07 12:19:57.230603', 'end_date': '2021-06-07 12:20:23.481629', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 41.216224, 'size': 47212396, 'rate': 1145480.8669518102, 'start_date': '2021-06-07 12:19:57.239434', 'end_date': '2021-06-07 12:20:38.455658', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 32.990406, 'size': 47212396, 'rate': 1431094.7249330608, 'start_date': '2021-06-07 12:19:57.247887', 'end_date': '2021-06-07 12:20:30.238293', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 29.605114, 'size': 47212396, 'rate': 1594737.8550881445, 'start_date': '2021-06-07 12:20:12.177477', 'end_date': '2021-06-07 12:20:41.782591', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 30.981022, 'size': 47212396, 'rate': 1523913.4461090406, 'start_date': '2021-06-07 12:20:14.690849', 'end_date': '2021-06-07 12:20:45.671871', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 11, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 34.891446, 'size': 47212396, 'rate': 1353122.367012247, 'start_date': '2021-06-07 12:20:18.554969', 'end_date': '2021-06-07 12:20:53.446415', 'crea_date': '2021-06-07 12:19:10.350928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},

]


data.extend(
    [

{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 14.929816, 'size': 47212396, 'rate': 3162289.20704716, 'start_date': '2021-06-07 12:30:32.984620', 'end_date': '2021-06-07 12:30:47.914436', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 18.350559, 'size': 47212396, 'rate': 2572804.2399144354, 'start_date': '2021-06-07 12:30:33.019540', 'end_date': '2021-06-07 12:30:51.370099', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 20.82923, 'size': 47212396, 'rate': 2266641.445699145, 'start_date': '2021-06-07 12:30:33.040360', 'end_date': '2021-06-07 12:30:53.869590', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 30.612046, 'size': 47212396, 'rate': 1542281.6233844678, 'start_date': '2021-06-07 12:30:33.051399', 'end_date': '2021-06-07 12:31:03.663445', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 41.479676, 'size': 47212396, 'rate': 1138205.5153950576, 'start_date': '2021-06-07 12:30:33.060429', 'end_date': '2021-06-07 12:31:14.540105', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 44.705333, 'size': 47212396, 'rate': 1056079.7299060493, 'start_date': '2021-06-07 12:30:33.067859', 'end_date': '2021-06-07 12:31:17.773192', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 32.38163, 'size': 47212396, 'rate': 1457999.3656897445, 'start_date': '2021-06-07 12:30:33.075143', 'end_date': '2021-06-07 12:31:05.456773', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 35.891267, 'size': 47212396, 'rate': 1315428.513571282, 'start_date': '2021-06-07 12:30:33.082398', 'end_date': '2021-06-07 12:31:08.973665', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 32.538942, 'size': 47212396, 'rate': 1450950.556413297, 'start_date': '2021-06-07 12:30:50.498384', 'end_date': '2021-06-07 12:31:23.037326', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 34.954191, 'size': 47212396, 'rate': 1350693.4261473825, 'start_date': '2021-06-07 12:30:53.479730', 'end_date': '2021-06-07 12:31:28.433921', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 11, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 21.262707, 'size': 47212396, 'rate': 2220432.045646869, 'start_date': '2021-06-07 12:30:56.502749', 'end_date': '2021-06-07 12:31:17.765456', 'crea_date': '2021-06-07 12:29:54.471619', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},

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
    calculated_from_os=downloading_duration['calculated from os'],
    color=color,
)

# RUN STRATEGY : big file default chunksize

data = [

# {'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 14.237354, 'size': 47212396, 'rate': 3316093.425786842, 'start_date': '2021-06-07 12:06:25.898498', 'end_date': '2021-06-07 12:06:40.135852', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 42.414645, 'size': 47212396, 'rate': 1113115.4345391786, 'start_date': '2021-06-07 12:06:25.931821', 'end_date': '2021-06-07 12:07:08.346466', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 43.563696, 'size': 47212396, 'rate': 1083755.5197336792, 'start_date': '2021-06-07 12:06:25.925603', 'end_date': '2021-06-07 12:07:09.489299', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 48.282903, 'size': 47212396, 'rate': 977828.4458165243, 'start_date': '2021-06-07 12:06:25.937702', 'end_date': '2021-06-07 12:07:14.220605', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 25.852347, 'size': 47212396, 'rate': 1826232.4886788807, 'start_date': '2021-06-07 12:06:26.055080', 'end_date': '2021-06-07 12:06:51.907427', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 48.596269, 'size': 47212396, 'rate': 971523.060751845, 'start_date': '2021-06-07 12:06:25.946686', 'end_date': '2021-06-07 12:07:14.542955', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 47.334524, 'size': 47212396, 'rate': 997419.8958882526, 'start_date': '2021-06-07 12:06:25.993069', 'end_date': '2021-06-07 12:07:13.327593', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 25.01081, 'size': 47212396, 'rate': 1887679.6073377873, 'start_date': '2021-06-07 12:06:26.074064', 'end_date': '2021-06-07 12:06:51.084874', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 14.621166, 'size': 47212396, 'rate': 3229044.5235352637, 'start_date': '2021-06-07 12:06:41.260608', 'end_date': '2021-06-07 12:06:55.881774', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 20.794656, 'size': 47212396, 'rate': 2270410.0515055405, 'start_date': '2021-06-07 12:06:52.799816', 'end_date': '2021-06-07 12:07:13.594472', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 11, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 19.80517, 'size': 47212396, 'rate': 2383841.9968119436, 'start_date': '2021-06-07 12:06:52.855242', 'end_date': '2021-06-07 12:07:12.660412', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},

]


data.extend(
    [

# {'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 35.073057, 'size': 47212396, 'rate': 1346115.7948108146, 'start_date': '2021-06-07 12:35:03.780481', 'end_date': '2021-06-07 12:35:38.853538', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 13.938583, 'size': 47212396, 'rate': 3387173.2872703057, 'start_date': '2021-06-07 12:35:03.745022', 'end_date': '2021-06-07 12:35:17.683605', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 42.967156, 'size': 47212396, 'rate': 1098801.977957303, 'start_date': '2021-06-07 12:35:03.763750', 'end_date': '2021-06-07 12:35:46.730906', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 32.296688, 'size': 47212396, 'rate': 1461833.9812429063, 'start_date': '2021-06-07 12:35:03.792879', 'end_date': '2021-06-07 12:35:36.089567', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 49.100862, 'size': 47212396, 'rate': 961539.0458929214, 'start_date': '2021-06-07 12:35:03.810264', 'end_date': '2021-06-07 12:35:52.911126', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 49.470451, 'size': 47212396, 'rate': 954355.4797994464, 'start_date': '2021-06-07 12:35:03.802372', 'end_date': '2021-06-07 12:35:53.272823', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 28.697428, 'size': 47212396, 'rate': 1645178.6550348694, 'start_date': '2021-06-07 12:35:03.819290', 'end_date': '2021-06-07 12:35:32.516718', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 29.238905, 'size': 47212396, 'rate': 1614711.4948388115, 'start_date': '2021-06-07 12:35:03.757520', 'end_date': '2021-06-07 12:35:32.996425', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 13.176967, 'size': 47212396, 'rate': 3582948.6406090264, 'start_date': '2021-06-07 12:35:18.486881', 'end_date': '2021-06-07 12:35:31.663848', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 16.048026, 'size': 47212396, 'rate': 2941944.1369299875, 'start_date': '2021-06-07 12:35:33.139546', 'end_date': '2021-06-07 12:35:49.187572', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 11, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 19.176948, 'size': 47212396, 'rate': 2461934.8188251853, 'start_date': '2021-06-07 12:35:33.595906', 'end_date': '2021-06-07 12:35:52.772854', 'crea_date': '2021-06-07 12:34:31.344179', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},

    ]
)

downloading_duration = {
    'calculated from os': 36.042912,
    "start": "2021-06-07 12:35:17.836885",
    "end": "2021-06-07 12:35:53.879797",
}

data.extend(
    [
{'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 32.049973, 'size': 47212396, 'rate': 1473086.9196052053, 'start_date': '2021-06-07 12:41:21.313677', 'end_date': '2021-06-07 12:41:53.363650', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 14.268844, 'size': 47212396, 'rate': 3308775.118713191, 'start_date': '2021-06-07 12:41:21.262032', 'end_date': '2021-06-07 12:41:35.530876', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 40.472164, 'size': 47212396, 'rate': 1166539.9458254816, 'start_date': '2021-06-07 12:41:21.335945', 'end_date': '2021-06-07 12:42:01.808109', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 37.162241, 'size': 47212396, 'rate': 1270439.9608193703, 'start_date': '2021-06-07 12:41:21.294785', 'end_date': '2021-06-07 12:41:58.457026', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 29.706043, 'size': 47212396, 'rate': 1589319.5872637765, 'start_date': '2021-06-07 12:41:21.254045', 'end_date': '2021-06-07 12:41:50.960088', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 47.010668, 'size': 47212396, 'rate': 1004291.1111154599, 'start_date': '2021-06-07 12:41:21.340903', 'end_date': '2021-06-07 12:42:08.351571', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 44.365238, 'size': 47212396, 'rate': 1064175.424912631, 'start_date': '2021-06-07 12:41:21.330311', 'end_date': '2021-06-07 12:42:05.695549', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 17.737536, 'size': 47212396, 'rate': 2661722.349710806, 'start_date': '2021-06-07 12:41:21.270849', 'end_date': '2021-06-07 12:41:39.008385', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 18.959168, 'size': 47212396, 'rate': 2490214.549499219, 'start_date': '2021-06-07 12:41:37.405233', 'end_date': '2021-06-07 12:41:56.364401', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 22.9653, 'size': 47212396, 'rate': 2055814.4679146365, 'start_date': '2021-06-07 12:41:40.342402', 'end_date': '2021-06-07 12:42:03.307702', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
{'file_id': 11, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 15.815303, 'size': 47212396, 'rate': 2985234.996762313, 'start_date': '2021-06-07 12:41:52.977664', 'end_date': '2021-06-07 12:42:08.792967', 'crea_date': '2021-06-07 12:41:08.538588', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},

    ]
)

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


# # RUN STRATEGY : big file customized chunksize
#
# data = [
#
# {'file_id': 1, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 14.237354, 'size': 47212396, 'rate': 3316093.425786842, 'start_date': '2021-06-07 12:06:25.898498', 'end_date': '2021-06-07 12:06:40.135852', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 2, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_0.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 42.414645, 'size': 47212396, 'rate': 1113115.4345391786, 'start_date': '2021-06-07 12:06:25.931821', 'end_date': '2021-06-07 12:07:08.346466', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 3, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_1.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 43.563696, 'size': 47212396, 'rate': 1083755.5197336792, 'start_date': '2021-06-07 12:06:25.925603', 'end_date': '2021-06-07 12:07:09.489299', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 4, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_2.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 48.282903, 'size': 47212396, 'rate': 977828.4458165243, 'start_date': '2021-06-07 12:06:25.937702', 'end_date': '2021-06-07 12:07:14.220605', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 5, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_3.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 25.852347, 'size': 47212396, 'rate': 1826232.4886788807, 'start_date': '2021-06-07 12:06:26.055080', 'end_date': '2021-06-07 12:06:51.907427', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 6, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_4.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 48.596269, 'size': 47212396, 'rate': 971523.060751845, 'start_date': '2021-06-07 12:06:25.946686', 'end_date': '2021-06-07 12:07:14.542955', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 7, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_5.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 47.334524, 'size': 47212396, 'rate': 997419.8958882526, 'start_date': '2021-06-07 12:06:25.993069', 'end_date': '2021-06-07 12:07:13.327593', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 8, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_6.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 25.01081, 'size': 47212396, 'rate': 1887679.6073377873, 'start_date': '2021-06-07 12:06:26.074064', 'end_date': '2021-06-07 12:06:51.084874', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 9, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_7.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 14.621166, 'size': 47212396, 'rate': 3229044.5235352637, 'start_date': '2021-06-07 12:06:41.260608', 'end_date': '2021-06-07 12:06:55.881774', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 10, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_8.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 20.794656, 'size': 47212396, 'rate': 2270410.0515055405, 'start_date': '2021-06-07 12:06:52.799816', 'end_date': '2021-06-07 12:07:13.594472', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
# {'file_id': 11, 'url': 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.amip.mon.atmos.Amon.r1i1p1.v20111006.tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'filename': 'tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812_9.nc', 'data_node': 'aims3.llnl.gov', 'checksum': '40485ffdaf4e4a9a3ce4d8587eba88aa93d56991364aa9de18ca803edef54d62', 'checksum_type': 'sha256', 'duration': 19.80517, 'size': 47212396, 'rate': 2383841.9968119436, 'start_date': '2021-06-07 12:06:52.855242', 'end_date': '2021-06-07 12:07:12.660412', 'crea_date': '2021-06-07 11:51:43.851081', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'a63a520c-8416-4339-b43d-b9996a2cccf2', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2012-11-20T09:43:14Z'},
#
# ]
#
# downloading_duration = {
#     'calculated from os': 0.000114,
#     "start": "2021-06-07 09:54:40.906789",
#     "end": "2021-06-07 09:54:40.906903",
# }
#
# for d in data:
#     d["strategy"] = strategies[2]
#
# big_file_customized_chunk_size_strategy = pd.DataFrame(data, columns=columns)
#
# big_file_customized_chunk_size_strategy = big_file_customized_chunk_size_strategy.sort_values(by=['size'])
#
# big_file_customized_chunk_size_strategy["start_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
#                                  big_file_customized_chunk_size_strategy["start_date"]]
# big_file_customized_chunk_size_strategy["end_date"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in
#                                big_file_customized_chunk_size_strategy["end_date"]]
#
# print(
#     big_file_customized_chunk_size_strategy["start_date"].min().strftime("%Y-%m-%d %H:%M:%S.%f"),
# )
#
# # dates alignment
# big_file_customized_chunk_size_strategy["start_date"], big_file_customized_chunk_size_strategy["end_date"] = alignment(
#     big_file_customized_chunk_size_strategy["start_date"],
#     big_file_customized_chunk_size_strategy["end_date"],
#     min_start_date,
# )
#
# # adf["duration"] = adf["duration"] * correction
#
# big_file_customized_chunk_size_strategy["size"] = big_file_customized_chunk_size_strategy["size"] * coeff_bytes_2_go
#
# color = '#ff6666'
#
# duration = (big_file_customized_chunk_size_strategy["end_date"].max() - big_file_customized_chunk_size_strategy["start_date"].min()).seconds
#
# big_file_customized_chunk_size_strategy_db_duration = dict(
#     duration=duration,
#     color=color,
# )

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
        big_file_default_chunk_size_strategy["start_date"].min(),
        # big_file_customized_chunk_size_strategy["start_date"].min(),
    ],
)
dmax = max(
    [
        dmax,
        big_file_default_chunk_size_strategy["end_date"].max(),
        # big_file_customized_chunk_size_strategy["end_date"].max(),
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

# # STRATEGY : big file read
#
# row = 3
# col = 1
#
# current_fig = px.timeline(
#     big_file_customized_chunk_size_strategy,
#     title="Downloads",
#     x_start="start_date",
#     x_end="end_date",
#     y='file_id',
#     color="strategy",
#     color_discrete_map=VIEW_COLORS,
#     text='duration',
#     hover_data=dict(
#         file_functional_id=True,
#         size=True,
#         start_date="|" + DATE_FORMAT,
#         end_date="|" + DATE_FORMAT,
#     ),
# )
#
# for trace in current_fig.data:
#     figs.add_trace(trace, row=row, col=col)
#
# figs.update_xaxes(type="date", range=xrange, row=row, col=col)
# # figs.update_xaxes(type="date", row=row, col=col)
#
# figs.update_yaxes(title_text="File", row=row, col=col)

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
    # '{} (duration : {} s)'.format(
    #     strategies[2],
    #     big_file_customized_chunk_size_strategy_db_duration["duration"],
    # ),
)

# rotate all the subtitles of 90 degrees
for i, annotation in enumerate(figs['layout']['annotations']):
    annotation['text'] = titles[i]

figs.show()
