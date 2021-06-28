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

hardware = "laptop"

big_file_size = 78675404
big_file_chunksize = 16384

strategies = [
    "current version",
    "asyncio aiohttp  (big file threshold size : {} Bytes)".format(big_file_size),
    "asyncio httpx (big file threshold size : {} Bytes)".format(big_file_size),
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


min_start_date = datetime.datetime.strptime('2021-06-11 14:29:01.172049', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = []

data.extend(
    [

{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 13.999095, 'size': 86344659, 'rate': 6167874.351877746, 'start_date': '2021-06-11 14:29:01.172049', 'end_date': '2021-06-11 14:29:15.171144', 'crea_date': '2021-06-11 14:28:35.554015', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 63.336617, 'size': 88114316, 'rate': 1391206.543286011, 'start_date': '2021-06-11 14:29:01.193093', 'end_date': '2021-06-11 14:30:04.529710', 'crea_date': '2021-06-11 14:28:35.558401', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 319.105825, 'size': 795795708, 'rate': 2493830.0891248225, 'start_date': '2021-06-11 14:29:01.203015', 'end_date': '2021-06-11 14:34:20.308840', 'crea_date': '2021-06-11 14:28:35.559984', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 33.807758, 'size': 27452120, 'rate': 812006.5222899431, 'start_date': '2021-06-11 14:29:01.211718', 'end_date': '2021-06-11 14:29:35.019476', 'crea_date': '2021-06-11 14:28:35.561659', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 68.830967, 'size': 138080132, 'rate': 2006075.7246080823, 'start_date': '2021-06-11 14:29:01.219968', 'end_date': '2021-06-11 14:30:10.050935', 'crea_date': '2021-06-11 14:28:35.563243', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 152.93096, 'size': 337361584, 'rate': 2205973.1005415777, 'start_date': '2021-06-11 14:29:01.228081', 'end_date': '2021-06-11 14:31:34.159041', 'crea_date': '2021-06-11 14:28:35.564889', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},
{'file_id': 7, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '53b1f9391ec4f6044cf9e4a66c48bf637e373cd921d1ad583969d07a07498bbf', 'checksum_type': 'sha256', 'duration': 80.646888, 'size': 135602224, 'rate': 1681431.576132237, 'start_date': '2021-06-11 14:29:01.236196', 'end_date': '2021-06-11 14:30:21.883084', 'crea_date': '2021-06-11 14:28:35.565931', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'bd7bc92c-c46e-4e90-844b-8b0922216626', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:09:08Z'},
{'file_id': 8, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '579960549e32244e5279b666b753b85d48eea4404922a0e260d0e6df85117217', 'checksum_type': 'sha256', 'duration': 150.724593, 'size': 337361756, 'rate': 2238266.160055247, 'start_date': '2021-06-11 14:29:01.244579', 'end_date': '2021-06-11 14:31:31.969172', 'crea_date': '2021-06-11 14:28:35.567043', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '9d756a4e-4937-412c-8d6f-66226f962ead', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:07:11Z'},
{'file_id': 9, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'a676580f2c6eccf91d100c0641c707513b2f7073cd7f8eec09dc41ec10aa7828', 'checksum_type': 'sha256', 'duration': 74.216844, 'size': 135602396, 'rate': 1827110.7836382804, 'start_date': '2021-06-11 14:29:16.494488', 'end_date': '2021-06-11 14:30:30.711332', 'crea_date': '2021-06-11 14:28:35.568038', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd48ed243-dfec-417b-bfb3-5665211c4a82', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:05:18Z'},
{'file_id': 10, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c4dd7af8ba2abfadf645bfe79aa8fc36639fce0578165ed72b6412e1e3db3da0', 'checksum_type': 'sha256', 'duration': 144.754822, 'size': 337361516, 'rate': 2330571.868617959, 'start_date': '2021-06-11 14:29:36.110483', 'end_date': '2021-06-11 14:32:00.865305', 'crea_date': '2021-06-11 14:28:35.569028', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '149a852d-6e66-4e0b-95e9-fb533ab2e239', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:23:02Z'},
{'file_id': 11, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '1ce79e34db909bac7676076fedaf69609695718ccb9097aea9b63081eb094599', 'checksum_type': 'sha256', 'duration': 62.686106, 'size': 135602156, 'rate': 2163193.164367236, 'start_date': '2021-06-11 14:30:07.352680', 'end_date': '2021-06-11 14:31:10.038786', 'crea_date': '2021-06-11 14:28:35.570108', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'ca619221-b9cc-4b36-a9c2-b7e6647b8072', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T18:25:32Z'},
{'file_id': 12, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '7fe78416c8389ee90f5c7a5969bff5d99ae814bafe85ca2676bb65e5c1bb5196', 'checksum_type': 'sha256', 'duration': 141.544868, 'size': 337361552, 'rate': 2383424.8232864225, 'start_date': '2021-06-11 14:30:14.551716', 'end_date': '2021-06-11 14:32:36.096584', 'crea_date': '2021-06-11 14:28:35.571096', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '764fa350-8a49-49ef-b473-3ca558b56e1b', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3satcalc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:56:55Z'},
{'file_id': 13, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'f0da712ed0de6ddd025518cc8bc69bff990663fa3360d6932300f5442cd325a0', 'checksum_type': 'sha256', 'duration': 72.437804, 'size': 135602192, 'rate': 1871980.9893740015, 'start_date': '2021-06-11 14:30:28.257740', 'end_date': '2021-06-11 14:31:40.695544', 'crea_date': '2021-06-11 14:28:35.572118', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'aa9a0bda-efcf-4d69-bd61-1048bcadaaa5', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3satcalc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:34:30Z'},
{'file_id': 14, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '13fb7a062b3a500569a4ea8e2a0b1336f506aa5ba8c1f98fb426d734e3735a33', 'checksum_type': 'sha256', 'duration': 150.011329, 'size': 337361576, 'rate': 2248907.3208597465, 'start_date': '2021-06-11 14:30:35.012664', 'end_date': '2021-06-11 14:33:05.023993', 'crea_date': '2021-06-11 14:28:35.573187', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '45a68351-a1d1-4a2c-a16d-1e4599c2228b', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'detoc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T04:43:18Z'},
{'file_id': 15, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '048a8f917b330509597329093df804af76ff74f2e345e975f2a8869239950359', 'checksum_type': 'sha256', 'duration': 70.582742, 'size': 135602216, 'rate': 1921180.90283316, 'start_date': '2021-06-11 14:31:16.748179', 'end_date': '2021-06-11 14:32:27.330921', 'crea_date': '2021-06-11 14:28:35.574138', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'fc72f180-5fe8-43a2-bf13-45ecb88b06c1', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'detoc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T04:50:04Z'},
{'file_id': 16, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'b9dcdb2fd2c8d61dcf8f6cb04bbbcd89bd78a0df710408cbf832d238b483d526', 'checksum_type': 'sha256', 'duration': 136.568744, 'size': 337361600, 'rate': 2470269.478351503, 'start_date': '2021-06-11 14:31:34.272067', 'end_date': '2021-06-11 14:33:50.840811', 'crea_date': '2021-06-11 14:28:35.575120', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5ccdc46f-407b-47d0-880c-f20be1e30044', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dfe', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T12:33:03Z'},
{'file_id': 17, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '069324b0531127f459cce9f01c80e3e712daaa3cbb671b4942b50ff82ad0521b', 'checksum_type': 'sha256', 'duration': 60.442292, 'size': 135602240, 'rate': 2243499.303434754, 'start_date': '2021-06-11 14:31:39.932581', 'end_date': '2021-06-11 14:32:40.374873', 'crea_date': '2021-06-11 14:28:35.576203', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '2322558a-595e-4936-9b2a-5de75de05ca5', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dfe', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T12:13:24Z'},
{'file_id': 18, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '14b5ca1cd2a6e7573408c8b10e57850dc6f47fd5755d0170994fdc5d30fd3bf4', 'checksum_type': 'sha256', 'duration': 194.567906, 'size': 337361572, 'rate': 1733901.4379894699, 'start_date': '2021-06-11 14:31:46.307810', 'end_date': '2021-06-11 14:35:00.875716', 'crea_date': '2021-06-11 14:28:35.577218', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'ae7c9b91-7d8e-40d2-a9f8-842cd2a3c02e', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dissic', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-02T21:20:39Z'},
{'file_id': 19, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '59078396f94487e70b9aadd1cfc956038810902138283d59f5a809c4b86953c9', 'checksum_type': 'sha256', 'duration': 67.14077, 'size': 135602212, 'rate': 2019670.1944288097, 'start_date': '2021-06-11 14:32:04.151921', 'end_date': '2021-06-11 14:33:11.292691', 'crea_date': '2021-06-11 14:28:35.578307', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'c5750fce-25c2-4ac0-90da-3f1571cd3cef', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dissic', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-02T20:58:55Z'},
{'file_id': 20, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'd2b683d1efe94e2250fa842cffbb6501fab88edc22a7353cff6d12f45093cc24', 'checksum_type': 'sha256', 'duration': 156.149515, 'size': 337361484, 'rate': 2160502.9256735123, 'start_date': '2021-06-11 14:32:32.462462', 'end_date': '2021-06-11 14:35:08.611977', 'crea_date': '2021-06-11 14:28:35.579251', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '6d329e8d-e0e4-40c5-b16e-67497fc2fefd', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dissoc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-02T23:10:29Z'},
{'file_id': 21, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'e87d53ef00d8bf5f088704eeb755f873596ff94992ff84380a447005995b3557', 'checksum_type': 'sha256', 'duration': 71.09736, 'size': 135602124, 'rate': 1907273.6877993783, 'start_date': '2021-06-11 14:32:38.886812', 'end_date': '2021-06-11 14:33:49.984172', 'crea_date': '2021-06-11 14:28:35.580172', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '661f2700-b468-4e00-8237-8172312d52e8', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dissoc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-02T21:49:47Z'},
{'file_id': 22, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '9d365d1b86519153b0d046e6c5d337788b6b382626f33456c7f6522b597690c2', 'checksum_type': 'sha256', 'duration': 156.022907, 'size': 337361460, 'rate': 2162255.9564282442, 'start_date': '2021-06-11 14:32:44.086159', 'end_date': '2021-06-11 14:35:20.109066', 'crea_date': '2021-06-11 14:28:35.581211', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'ca64c733-5e26-49f0-b1d6-3862473009d0', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'nh4', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T11:32:17Z'},
{'file_id': 23, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'afb68a92eafb092040b3fa05584f1f8385f265b79d0537c4393adb3cc55244bb', 'checksum_type': 'sha256', 'duration': 80.709761, 'size': 135602100, 'rate': 1680120.202561373, 'start_date': '2021-06-11 14:33:07.087512', 'end_date': '2021-06-11 14:34:27.797273', 'crea_date': '2021-06-11 14:28:35.582186', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5d2fc455-3aba-4669-9dbc-811f6053b43a', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'nh4', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T11:22:10Z'},
{'file_id': 24, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '602a81220895c1494516855226ff1d96f0f0182dbc43b42401f198475fbb38d2', 'checksum_type': 'sha256', 'duration': 133.105914, 'size': 337361456, 'rate': 2534533.935133791, 'start_date': '2021-06-11 14:33:13.924246', 'end_date': '2021-06-11 14:35:27.030160', 'crea_date': '2021-06-11 14:28:35.583114', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'b1abc4e9-8dd8-4e2b-aac5-f78338ee96e6', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'no3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T11:12:54Z'},
{'file_id': 25, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'a867592c388719d2a0eb9f40152923cae10741d40b6f4e5c716081dfc7c1c8b1', 'checksum_type': 'sha256', 'duration': 71.749219, 'size': 135602096, 'rate': 1889945.255013856, 'start_date': '2021-06-11 14:33:52.660803', 'end_date': '2021-06-11 14:35:04.410022', 'crea_date': '2021-06-11 14:28:35.584101', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '4dc6a042-8602-4751-a760-ad191697f930', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'no3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T10:40:35Z'},
{'file_id': 26, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '1a13d1b44197ae60eaffa83b9c5a7fa322bc1de8bdc8800106427d3da044c88b', 'checksum_type': 'sha256', 'duration': 138.879572, 'size': 337361464, 'rate': 2429165.4931079424, 'start_date': '2021-06-11 14:33:52.669187', 'end_date': '2021-06-11 14:36:11.548759', 'crea_date': '2021-06-11 14:28:35.584959', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '25d54f2a-7af0-4172-8e79-6c3112664ef4', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'o2', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T10:01:36Z'},
{'file_id': 27, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '8dca30f1c92c13bcbe975c4a80d14c790475fc15897044953f1ca0f9c127d751', 'checksum_type': 'sha256', 'duration': 67.556623, 'size': 135602104, 'rate': 2007236.2705282057, 'start_date': '2021-06-11 14:34:27.452096', 'end_date': '2021-06-11 14:35:35.008719', 'crea_date': '2021-06-11 14:28:35.585834', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '02712118-9b66-4c53-acdc-358ff0f02b6d', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'o2', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T09:38:14Z'},

    ]
)
data.extend(
    [

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

    ]
)

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
        "title": 'Hardware : laptop | {} Downloads ({} Mo)'.format(
            len(files),
            sizes * coeff_bytes_2_go,
        ),
    },
)


# # RUN STRATEGY : big file customized chunksize

data = [
]

data.extend(
    [

{'file_id': 4, 'download speed': 23647.0, 'file size': 27452120, 'duration': 1.133686, 'start_date': '2021-06-11 19:46:45.193362', 'end_date': '2021-06-11 19:46:46.327048', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'file_id': 2, 'download speed': 38146.0, 'file size': 88114316, 'duration': 2.255753, 'start_date': '2021-06-11 19:46:45.186479', 'end_date': '2021-06-11 19:46:47.442232', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc'},
{'file_id': 7, 'download speed': 49938.0, 'file size': 135602224, 'duration': 2.651765, 'start_date': '2021-06-11 19:46:45.204297', 'end_date': '2021-06-11 19:46:47.856062', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 1, 'download speed': 29631.0, 'file size': 86344659, 'duration': 2.845694, 'start_date': '2021-06-11 19:46:45.186419', 'end_date': '2021-06-11 19:46:48.032113', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc'},
{'file_id': 5, 'download speed': 23763.0, 'file size': 138080132, 'duration': 5.674497, 'start_date': '2021-06-11 19:46:45.197144', 'end_date': '2021-06-11 19:46:50.871641', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'file_id': 9, 'download speed': 21155.0, 'file size': 135602396, 'duration': 6.2597, 'start_date': '2021-06-11 19:46:46.337303', 'end_date': '2021-06-11 19:46:52.597003', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 6, 'download speed': 24798.0, 'file size': 337361584, 'duration': 13.285088, 'start_date': '2021-06-11 19:46:45.200728', 'end_date': '2021-06-11 19:46:58.485816', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 13, 'download speed': 16731.0, 'file size': 135602192, 'duration': 7.914613, 'start_date': '2021-06-11 19:46:50.880085', 'end_date': '2021-06-11 19:46:58.794698', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 11, 'download speed': 11783.0, 'file size': 135602156, 'duration': 11.238212, 'start_date': '2021-06-11 19:46:47.864427', 'end_date': '2021-06-11 19:46:59.102639', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 8, 'download speed': 22015.0, 'file size': 337361756, 'duration': 14.964833, 'start_date': '2021-06-11 19:46:45.212046', 'end_date': '2021-06-11 19:47:00.176879', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 10, 'download speed': 23570.0, 'file size': 337361516, 'duration': 13.977549, 'start_date': '2021-06-11 19:46:47.458846', 'end_date': '2021-06-11 19:47:01.436395', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 14, 'download speed': 33807.0, 'file size': 337361576, 'duration': 9.744996, 'start_date': '2021-06-11 19:46:52.607919', 'end_date': '2021-06-11 19:47:02.352915', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 12, 'download speed': 22814.0, 'file size': 337361552, 'duration': 14.440547, 'start_date': '2021-06-11 19:46:48.044273', 'end_date': '2021-06-11 19:47:02.484820', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 3, 'download speed': 43997.0, 'file size': 795795708, 'duration': 17.663529, 'start_date': '2021-06-11 19:46:45.189984', 'end_date': '2021-06-11 19:47:02.853513', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc'},
{'file_id': 16, 'download speed': 31975.0, 'file size': 337361600, 'duration': 10.303263, 'start_date': '2021-06-11 19:46:58.795514', 'end_date': '2021-06-11 19:47:09.098777', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 17, 'download speed': 13064.0, 'file size': 135602240, 'duration': 10.136022, 'start_date': '2021-06-11 19:46:59.103338', 'end_date': '2021-06-11 19:47:09.239360', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 18, 'download speed': 36039.0, 'file size': 337361572, 'duration': 9.141573, 'start_date': '2021-06-11 19:47:00.180257', 'end_date': '2021-06-11 19:47:09.321830', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 15, 'download speed': 11989.0, 'file size': 135602216, 'duration': 11.04511, 'start_date': '2021-06-11 19:46:58.489351', 'end_date': '2021-06-11 19:47:09.534461', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 21, 'download speed': 17643.0, 'file size': 135602124, 'duration': 7.505695, 'start_date': '2021-06-11 19:47:02.487794', 'end_date': '2021-06-11 19:47:09.993489', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 19, 'download speed': 14502.0, 'file size': 135602212, 'duration': 9.130914, 'start_date': '2021-06-11 19:47:01.438735', 'end_date': '2021-06-11 19:47:10.569649', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 22, 'download speed': 42059.0, 'file size': 337361460, 'duration': 7.833024, 'start_date': '2021-06-11 19:47:02.864608', 'end_date': '2021-06-11 19:47:10.697632', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 20, 'download speed': 39320.0, 'file size': 337361484, 'duration': 8.378683, 'start_date': '2021-06-11 19:47:02.353434', 'end_date': '2021-06-11 19:47:10.732117', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 23, 'download speed': 49232.0, 'file size': 135602100, 'duration': 2.689761, 'start_date': '2021-06-11 19:47:09.099291', 'end_date': '2021-06-11 19:47:11.789052', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 25, 'download speed': 35269.0, 'file size': 135602096, 'duration': 3.754595, 'start_date': '2021-06-11 19:47:09.322271', 'end_date': '2021-06-11 19:47:13.076866', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 27, 'download speed': 32726.0, 'file size': 135602104, 'duration': 4.046437, 'start_date': '2021-06-11 19:47:10.002352', 'end_date': '2021-06-11 19:47:14.048789', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc'},
{'file_id': 24, 'download speed': 41187.0, 'file size': 337361456, 'duration': 7.99892, 'start_date': '2021-06-11 19:47:09.239927', 'end_date': '2021-06-11 19:47:17.238847', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},
{'file_id': 26, 'download speed': 42621.0, 'file size': 337361464, 'duration': 7.729688, 'start_date': '2021-06-11 19:47:09.538160', 'end_date': '2021-06-11 19:47:17.267848', 'strategy': 'asyncio - processes', 'status_code': 200, 'local_path': '/modfs/scratch/pjournoud/synda/data/cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc'},

    ]
)

data.extend(
    [

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
