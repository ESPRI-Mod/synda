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
'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc': 27452120,
'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc': 138080132,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361584,

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
    "asyncio single thread  (big file threshold size : {} Bytes)".format(big_file_size),
    "asyncio main gather  (big file threshold size : {} Bytes)".format(big_file_size),
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
    title_text="Same file downloaded ten times for each strategy | File size : {:5.2f} Mo".format(
        sizes * coeff_bytes_2_mo,
    ),
)


def alignment(start, end, min_date):
    delta = start.min() - min_date
    aligned_start = [date - delta for date in start]
    aligned_end = [date - delta for date in end]
    return aligned_start, aligned_end


min_start_date = datetime.datetime.strptime('2021-06-08 16:43:09.908201', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = []

data.extend(
    [

{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 12.666626, 'size': 86344659, 'rate': 6816705.490475521, 'start_date': '2021-06-08 16:51:35.871021', 'end_date': '2021-06-08 16:51:48.537647', 'crea_date': '2021-06-08 16:51:18.331564', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 48.914879, 'size': 88114316, 'rate': 1801380.6392120484, 'start_date': '2021-06-08 16:51:35.902488', 'end_date': '2021-06-08 16:52:24.817367', 'crea_date': '2021-06-08 16:51:18.335430', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 104.642052, 'size': 795795708, 'rate': 7604932.173921818, 'start_date': '2021-06-08 16:51:35.921626', 'end_date': '2021-06-08 16:53:20.563678', 'crea_date': '2021-06-08 16:51:18.337025', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 22.168649, 'size': 27452120, 'rate': 1238330.7616084318, 'start_date': '2021-06-08 16:51:35.930488', 'end_date': '2021-06-08 16:51:58.099137', 'crea_date': '2021-06-08 16:51:18.338712', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 59.603336, 'size': 138080132, 'rate': 2316651.0679872013, 'start_date': '2021-06-08 16:51:35.938993', 'end_date': '2021-06-08 16:52:35.542329', 'crea_date': '2021-06-08 16:51:18.340291', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 79.740054, 'size': 337361584, 'rate': 4230766.936776842, 'start_date': '2021-06-08 16:51:35.947390', 'end_date': '2021-06-08 16:52:55.687444', 'crea_date': '2021-06-08 16:51:18.341979', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},


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

data.extend(
    [

{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 34.099227, 'size': 86344659, 'rate': 2532158.8375009205, 'start_date': '2021-06-08 16:49:06.118143', 'end_date': '2021-06-08 16:49:40.217370', 'crea_date': '2021-06-08 16:48:47.787104', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 44.01652, 'size': 88114316, 'rate': 2001846.4885456641, 'start_date': '2021-06-08 16:49:05.769953', 'end_date': '2021-06-08 16:49:49.786473', 'crea_date': '2021-06-08 16:48:47.790622', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 81.469605, 'size': 795795708, 'rate': 9768007.442775745, 'start_date': '2021-06-08 16:49:04.649931', 'end_date': '2021-06-08 16:50:26.119536', 'crea_date': '2021-06-08 16:48:47.792191', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 13.380883, 'size': 27452120, 'rate': 2051592.5593251206, 'start_date': '2021-06-08 16:49:06.476136', 'end_date': '2021-06-08 16:49:19.857019', 'crea_date': '2021-06-08 16:48:47.793856', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 55.122048, 'size': 138080132, 'rate': 2504989.1469925065, 'start_date': '2021-06-08 16:49:05.428243', 'end_date': '2021-06-08 16:50:00.550291', 'crea_date': '2021-06-08 16:48:47.795416', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 69.872788, 'size': 337361584, 'rate': 4828225.603363644, 'start_date': '2021-06-08 16:49:05.053247', 'end_date': '2021-06-08 16:50:14.926035', 'crea_date': '2021-06-08 16:48:47.797093', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

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


# # RUN STRATEGY : big file customized chunksize

data = [
{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 41.26231, 'size': 86344659, 'rate': 2092579.3781298236, 'start_date': '2021-06-08 16:43:11.217767', 'end_date': '2021-06-08 16:43:52.480077', 'crea_date': '2021-06-08 16:42:56.518737', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 18.382109, 'size': 88114316, 'rate': 4793482.4018288655, 'start_date': '2021-06-08 16:43:10.821264', 'end_date': '2021-06-08 16:43:29.203373', 'crea_date': '2021-06-08 16:42:56.522203', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 71.794513, 'size': 795795708, 'rate': 11084352.755481469, 'start_date': '2021-06-08 16:43:09.908201', 'end_date': '2021-06-08 16:44:21.702714', 'crea_date': '2021-06-08 16:42:56.523825', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 24.023109, 'size': 27452120, 'rate': 1142738.019462843, 'start_date': '2021-06-08 16:43:11.569840', 'end_date': '2021-06-08 16:43:35.592949', 'crea_date': '2021-06-08 16:42:56.525546', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 47.947848, 'size': 138080132, 'rate': 2879798.3175386726, 'start_date': '2021-06-08 16:43:10.488372', 'end_date': '2021-06-08 16:43:58.436220', 'crea_date': '2021-06-08 16:42:56.527123', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 59.715425, 'size': 337361584, 'rate': 5649488.118019758, 'start_date': '2021-06-08 16:43:10.215473', 'end_date': '2021-06-08 16:44:09.930898', 'crea_date': '2021-06-08 16:42:56.528811', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},


]
#
# downloading_duration = {
#     'calculated from os': 0.000114,
#     "start": "2021-06-07 09:54:40.906789",
#     "end": "2021-06-07 09:54:40.906903",
# }

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
