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
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602224,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361756,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602396,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361516,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc': 135602156,
'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc': 337361552,

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

{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 19.421419, 'size': 86344659, 'rate': 4445847.082543247, 'start_date': '2021-06-08 17:05:33.291239', 'end_date': '2021-06-08 17:05:52.712658', 'crea_date': '2021-06-08 17:04:16.477843', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 46.5722, 'size': 88114316, 'rate': 1891993.8504086128, 'start_date': '2021-06-08 17:05:33.305317', 'end_date': '2021-06-08 17:06:19.877517', 'crea_date': '2021-06-08 17:04:16.481661', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 178.858056, 'size': 795795708, 'rate': 4449314.30989052, 'start_date': '2021-06-08 17:05:33.316604', 'end_date': '2021-06-08 17:08:32.174660', 'crea_date': '2021-06-08 17:04:16.483239', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 33.939883, 'size': 27452120, 'rate': 808845.451824333, 'start_date': '2021-06-08 17:05:33.326354', 'end_date': '2021-06-08 17:06:07.266237', 'crea_date': '2021-06-08 17:04:16.484907', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 81.976209, 'size': 138080132, 'rate': 1684392.7486327162, 'start_date': '2021-06-08 17:05:33.334482', 'end_date': '2021-06-08 17:06:55.310691', 'crea_date': '2021-06-08 17:04:16.486466', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 143.823136, 'size': 337361584, 'rate': 2345669.7815294475, 'start_date': '2021-06-08 17:05:33.342466', 'end_date': '2021-06-08 17:07:57.165602', 'crea_date': '2021-06-08 17:04:16.488132', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},
{'file_id': 7, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '53b1f9391ec4f6044cf9e4a66c48bf637e373cd921d1ad583969d07a07498bbf', 'checksum_type': 'sha256', 'duration': 87.106308, 'size': 135602224, 'rate': 1556744.019043948, 'start_date': '2021-06-08 17:05:33.350601', 'end_date': '2021-06-08 17:07:00.456909', 'crea_date': '2021-06-08 17:04:16.489145', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'bd7bc92c-c46e-4e90-844b-8b0922216626', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:09:08Z'},
{'file_id': 8, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '579960549e32244e5279b666b753b85d48eea4404922a0e260d0e6df85117217', 'checksum_type': 'sha256', 'duration': 142.574255, 'size': 337361756, 'rate': 2366217.912203013, 'start_date': '2021-06-08 17:05:33.358400', 'end_date': '2021-06-08 17:07:55.932655', 'crea_date': '2021-06-08 17:04:16.490141', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '9d756a4e-4937-412c-8d6f-66226f962ead', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:07:11Z'},
{'file_id': 9, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'a676580f2c6eccf91d100c0641c707513b2f7073cd7f8eec09dc41ec10aa7828', 'checksum_type': 'sha256', 'duration': 77.170725, 'size': 135602396, 'rate': 1757174.0579086174, 'start_date': '2021-06-08 17:05:54.955878', 'end_date': '2021-06-08 17:07:12.126603', 'crea_date': '2021-06-08 17:04:16.491259', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd48ed243-dfec-417b-bfb3-5665211c4a82', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:05:18Z'},
{'file_id': 10, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c4dd7af8ba2abfadf645bfe79aa8fc36639fce0578165ed72b6412e1e3db3da0', 'checksum_type': 'sha256', 'duration': 115.081766, 'size': 337361516, 'rate': 2931494.082216291, 'start_date': '2021-06-08 17:06:08.384782', 'end_date': '2021-06-08 17:08:03.466548', 'crea_date': '2021-06-08 17:04:16.492232', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '149a852d-6e66-4e0b-95e9-fb533ab2e239', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:23:02Z'},
{'file_id': 11, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '1ce79e34db909bac7676076fedaf69609695718ccb9097aea9b63081eb094599', 'checksum_type': 'sha256', 'duration': 58.306826, 'size': 135602156, 'rate': 2325665.1974161654, 'start_date': '2021-06-08 17:06:21.524581', 'end_date': '2021-06-08 17:07:19.831407', 'crea_date': '2021-06-08 17:04:16.493215', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'ca619221-b9cc-4b36-a9c2-b7e6647b8072', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T18:25:32Z'},
{'file_id': 12, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '7fe78416c8389ee90f5c7a5969bff5d99ae814bafe85ca2676bb65e5c1bb5196', 'checksum_type': 'sha256', 'duration': 84.254932, 'size': 337361552, 'rate': 4004057.0206620074, 'start_date': '2021-06-08 17:06:59.494404', 'end_date': '2021-06-08 17:08:23.749336', 'crea_date': '2021-06-08 17:04:16.494206', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '764fa350-8a49-49ef-b473-3ca558b56e1b', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3satcalc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:56:55Z'},


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

{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 40.006095, 'size': 86344659, 'rate': 2158287.605926047, 'start_date': '2021-06-08 17:42:33.814568', 'end_date': '2021-06-08 17:43:13.820663', 'crea_date': '2021-06-08 17:40:50.779493', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 46.905181, 'size': 88114316, 'rate': 1878562.540884343, 'start_date': '2021-06-08 17:42:25.066930', 'end_date': '2021-06-08 17:43:11.972111', 'crea_date': '2021-06-08 17:40:50.783149', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 156.618306, 'size': 795795708, 'rate': 5081115.537030518, 'start_date': '2021-06-08 17:41:10.546794', 'end_date': '2021-06-08 17:43:47.165100', 'crea_date': '2021-06-08 17:40:50.784734', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 20.293938, 'size': 27452120, 'rate': 1352725.1339784323, 'start_date': '2021-06-08 17:42:58.267763', 'end_date': '2021-06-08 17:43:18.561701', 'crea_date': '2021-06-08 17:40:50.786421', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 71.197738, 'size': 138080132, 'rate': 1939389.3103738774, 'start_date': '2021-06-08 17:41:12.240504', 'end_date': '2021-06-08 17:42:23.438242', 'crea_date': '2021-06-08 17:40:50.787971', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 140.016132, 'size': 337361584, 'rate': 2409447.9627533206, 'start_date': '2021-06-08 17:41:11.312100', 'end_date': '2021-06-08 17:43:31.328232', 'crea_date': '2021-06-08 17:40:50.789667', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},
{'file_id': 7, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '53b1f9391ec4f6044cf9e4a66c48bf637e373cd921d1ad583969d07a07498bbf', 'checksum_type': 'sha256', 'duration': 79.868914, 'size': 135602224, 'rate': 1697809.7886744773, 'start_date': '2021-06-08 17:41:12.897864', 'end_date': '2021-06-08 17:42:32.766778', 'crea_date': '2021-06-08 17:40:50.790686', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'bd7bc92c-c46e-4e90-844b-8b0922216626', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:09:08Z'},
{'file_id': 8, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '579960549e32244e5279b666b753b85d48eea4404922a0e260d0e6df85117217', 'checksum_type': 'sha256', 'duration': 134.459259, 'size': 337361756, 'rate': 2509025.845516522, 'start_date': '2021-06-08 17:41:10.900082', 'end_date': '2021-06-08 17:43:25.359341', 'crea_date': '2021-06-08 17:40:50.791667', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '9d756a4e-4937-412c-8d6f-66226f962ead', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:07:11Z'},
{'file_id': 9, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'a676580f2c6eccf91d100c0641c707513b2f7073cd7f8eec09dc41ec10aa7828', 'checksum_type': 'sha256', 'duration': 50.516467, 'size': 135602396, 'rate': 2684320.659241669, 'start_date': '2021-06-08 17:41:12.599038', 'end_date': '2021-06-08 17:42:03.115505', 'crea_date': '2021-06-08 17:40:50.792906', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd48ed243-dfec-417b-bfb3-5665211c4a82', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:05:18Z'},
{'file_id': 10, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c4dd7af8ba2abfadf645bfe79aa8fc36639fce0578165ed72b6412e1e3db3da0', 'checksum_type': 'sha256', 'duration': 138.421759, 'size': 337361516, 'rate': 2437200.035870083, 'start_date': '2021-06-08 17:41:11.978640', 'end_date': '2021-06-08 17:43:30.400399', 'crea_date': '2021-06-08 17:40:50.793884', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '149a852d-6e66-4e0b-95e9-fb533ab2e239', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:23:02Z'},
{'file_id': 11, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '1ce79e34db909bac7676076fedaf69609695718ccb9097aea9b63081eb094599', 'checksum_type': 'sha256', 'duration': 51.801271, 'size': 135602156, 'rate': 2617738.008783607, 'start_date': '2021-06-08 17:42:04.902851', 'end_date': '2021-06-08 17:42:56.704122', 'crea_date': '2021-06-08 17:40:50.794875', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'ca619221-b9cc-4b36-a9c2-b7e6647b8072', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T18:25:32Z'},
{'file_id': 12, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '7fe78416c8389ee90f5c7a5969bff5d99ae814bafe85ca2676bb65e5c1bb5196', 'checksum_type': 'sha256', 'duration': 126.082753, 'size': 337361552, 'rate': 2675715.305803959, 'start_date': '2021-06-08 17:41:11.619328', 'end_date': '2021-06-08 17:43:17.702081', 'crea_date': '2021-06-08 17:40:50.795866', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '764fa350-8a49-49ef-b473-3ca558b56e1b', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3satcalc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:56:55Z'},

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

{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 38.749262, 'size': 86344659, 'rate': 2228291.702691009, 'start_date': '2021-06-08 17:46:49.540903', 'end_date': '2021-06-08 17:47:28.290165', 'crea_date': '2021-06-08 17:45:33.479555', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 34.197329, 'size': 88114316, 'rate': 2576643.222632972, 'start_date': '2021-06-08 17:46:48.535627', 'end_date': '2021-06-08 17:47:22.732956', 'crea_date': '2021-06-08 17:45:33.483129', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 153.229053, 'size': 795795708, 'rate': 5193504.054351886, 'start_date': '2021-06-08 17:45:51.205638', 'end_date': '2021-06-08 17:48:24.434691', 'crea_date': '2021-06-08 17:45:33.484712', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 17.447363, 'size': 27452120, 'rate': 1573425.164593641, 'start_date': '2021-06-08 17:47:23.681093', 'end_date': '2021-06-08 17:47:41.128456', 'crea_date': '2021-06-08 17:45:33.486397', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 56.108435, 'size': 138080132, 'rate': 2460951.4059695303, 'start_date': '2021-06-08 17:45:52.864240', 'end_date': '2021-06-08 17:46:48.972675', 'crea_date': '2021-06-08 17:45:33.487936', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 135.367192, 'size': 337361584, 'rate': 2492196.070669768, 'start_date': '2021-06-08 17:45:51.819342', 'end_date': '2021-06-08 17:48:07.186534', 'crea_date': '2021-06-08 17:45:33.489610', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},
{'file_id': 7, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '53b1f9391ec4f6044cf9e4a66c48bf637e373cd921d1ad583969d07a07498bbf', 'checksum_type': 'sha256', 'duration': 54.055269, 'size': 135602224, 'rate': 2508584.7597946464, 'start_date': '2021-06-08 17:45:53.558219', 'end_date': '2021-06-08 17:46:47.613488', 'crea_date': '2021-06-08 17:45:33.490626', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'bd7bc92c-c46e-4e90-844b-8b0922216626', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:09:08Z'},
{'file_id': 8, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '579960549e32244e5279b666b753b85d48eea4404922a0e260d0e6df85117217', 'checksum_type': 'sha256', 'duration': 137.322472, 'size': 337361756, 'rate': 2456711.935683768, 'start_date': '2021-06-08 17:45:51.515459', 'end_date': '2021-06-08 17:48:08.837931', 'crea_date': '2021-06-08 17:45:33.491609', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '9d756a4e-4937-412c-8d6f-66226f962ead', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:07:11Z'},
{'file_id': 9, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'a676580f2c6eccf91d100c0641c707513b2f7073cd7f8eec09dc41ec10aa7828', 'checksum_type': 'sha256', 'duration': 52.03334, 'size': 135602396, 'rate': 2606067.4944180017, 'start_date': '2021-06-08 17:45:53.216828', 'end_date': '2021-06-08 17:46:45.250168', 'crea_date': '2021-06-08 17:45:33.492717', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd48ed243-dfec-417b-bfb3-5665211c4a82', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:05:18Z'},
{'file_id': 10, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c4dd7af8ba2abfadf645bfe79aa8fc36639fce0578165ed72b6412e1e3db3da0', 'checksum_type': 'sha256', 'duration': 137.094706, 'size': 337361516, 'rate': 2460791.7099293387, 'start_date': '2021-06-08 17:45:52.490673', 'end_date': '2021-06-08 17:48:09.585379', 'crea_date': '2021-06-08 17:45:33.493677', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '149a852d-6e66-4e0b-95e9-fb533ab2e239', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:23:02Z'},
{'file_id': 11, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '1ce79e34db909bac7676076fedaf69609695718ccb9097aea9b63081eb094599', 'checksum_type': 'sha256', 'duration': 37.137103, 'size': 135602156, 'rate': 3651392.947909803, 'start_date': '2021-06-08 17:46:46.575194', 'end_date': '2021-06-08 17:47:23.712297', 'crea_date': '2021-06-08 17:45:33.494629', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'ca619221-b9cc-4b36-a9c2-b7e6647b8072', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T18:25:32Z'},
{'file_id': 12, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '7fe78416c8389ee90f5c7a5969bff5d99ae814bafe85ca2676bb65e5c1bb5196', 'checksum_type': 'sha256', 'duration': 113.031049, 'size': 337361552, 'rate': 2984680.359818655, 'start_date': '2021-06-08 17:45:52.136943', 'end_date': '2021-06-08 17:47:45.167992', 'crea_date': '2021-06-08 17:45:33.495586', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '764fa350-8a49-49ef-b473-3ca558b56e1b', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3satcalc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:56:55Z'},


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
