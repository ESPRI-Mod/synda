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

hardware = "synda-dev"

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

{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 1.675211, 'size': 86344659, 'rate': 51542557.325614505, 'start_date': '2021-06-11 16:25:30.946723', 'end_date': '2021-06-11 16:25:32.621934', 'crea_date': '2021-06-11 16:24:31.609453', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 2.745096, 'size': 88114316, 'rate': 32098810.387687713, 'start_date': '2021-06-11 16:25:30.978720', 'end_date': '2021-06-11 16:25:33.723816', 'crea_date': '2021-06-11 16:24:31.630787', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 11.271647, 'size': 795795708, 'rate': 70601546.34012225, 'start_date': '2021-06-11 16:25:31.013095', 'end_date': '2021-06-11 16:25:42.284742', 'crea_date': '2021-06-11 16:24:31.635962', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 4.006154, 'size': 27452120, 'rate': 6852487.448061157, 'start_date': '2021-06-11 16:25:31.046263', 'end_date': '2021-06-11 16:25:35.052417', 'crea_date': '2021-06-11 16:24:31.641763', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 7.57541, 'size': 138080132, 'rate': 18227413.697740454, 'start_date': '2021-06-11 16:25:31.078379', 'end_date': '2021-06-11 16:25:38.653789', 'crea_date': '2021-06-11 16:24:31.646867', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 10.908879, 'size': 337361584, 'rate': 30925412.59280628, 'start_date': '2021-06-11 16:25:31.109637', 'end_date': '2021-06-11 16:25:42.018516', 'crea_date': '2021-06-11 16:24:31.652080', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},
{'file_id': 7, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '53b1f9391ec4f6044cf9e4a66c48bf637e373cd921d1ad583969d07a07498bbf', 'checksum_type': 'sha256', 'duration': 9.29085, 'size': 135602224, 'rate': 14595244.1380498, 'start_date': '2021-06-11 16:25:31.141085', 'end_date': '2021-06-11 16:25:40.431935', 'crea_date': '2021-06-11 16:24:31.655993', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'bd7bc92c-c46e-4e90-844b-8b0922216626', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:09:08Z'},
{'file_id': 8, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '579960549e32244e5279b666b753b85d48eea4404922a0e260d0e6df85117217', 'checksum_type': 'sha256', 'duration': 11.944816, 'size': 337361756, 'rate': 28243361.471620828, 'start_date': '2021-06-11 16:25:31.172948', 'end_date': '2021-06-11 16:25:43.117764', 'crea_date': '2021-06-11 16:24:31.659816', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '9d756a4e-4937-412c-8d6f-66226f962ead', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:07:11Z'},
{'file_id': 9, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/chl_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'a676580f2c6eccf91d100c0641c707513b2f7073cd7f8eec09dc41ec10aa7828', 'checksum_type': 'sha256', 'duration': 2.02972, 'size': 135602396, 'rate': 66808424.807362586, 'start_date': '2021-06-11 16:25:43.001528', 'end_date': '2021-06-11 16:25:45.031248', 'crea_date': '2021-06-11 16:24:31.663717', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd48ed243-dfec-417b-bfb3-5665211c4a82', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'chl', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T14:05:18Z'},
{'file_id': 10, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c4dd7af8ba2abfadf645bfe79aa8fc36639fce0578165ed72b6412e1e3db3da0', 'checksum_type': 'sha256', 'duration': 4.683557, 'size': 337361516, 'rate': 72031047.34286354, 'start_date': '2021-06-11 16:25:43.069698', 'end_date': '2021-06-11 16:25:47.753255', 'crea_date': '2021-06-11 16:24:31.667470', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '149a852d-6e66-4e0b-95e9-fb533ab2e239', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:23:02Z'},
{'file_id': 11, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '1ce79e34db909bac7676076fedaf69609695718ccb9097aea9b63081eb094599', 'checksum_type': 'sha256', 'duration': 4.160227, 'size': 135602156, 'rate': 32594893.499801815, 'start_date': '2021-06-11 16:25:43.107627', 'end_date': '2021-06-11 16:25:47.267854', 'crea_date': '2021-06-11 16:24:31.671399', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'ca619221-b9cc-4b36-a9c2-b7e6647b8072', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T18:25:32Z'},
{'file_id': 12, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '7fe78416c8389ee90f5c7a5969bff5d99ae814bafe85ca2676bb65e5c1bb5196', 'checksum_type': 'sha256', 'duration': 7.707755, 'size': 337361552, 'rate': 43769106.82812311, 'start_date': '2021-06-11 16:25:43.150510', 'end_date': '2021-06-11 16:25:50.858265', 'crea_date': '2021-06-11 16:24:31.675094', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '764fa350-8a49-49ef-b473-3ca558b56e1b', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3satcalc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:56:55Z'},
{'file_id': 13, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/co3satcalc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'f0da712ed0de6ddd025518cc8bc69bff990663fa3360d6932300f5442cd325a0', 'checksum_type': 'sha256', 'duration': 6.306808, 'size': 135602192, 'rate': 21500922.81230061, 'start_date': '2021-06-11 16:25:43.187324', 'end_date': '2021-06-11 16:25:49.494132', 'crea_date': '2021-06-11 16:24:31.678722', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'aa9a0bda-efcf-4d69-bd61-1048bcadaaa5', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'co3satcalc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T19:34:30Z'},
{'file_id': 14, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '13fb7a062b3a500569a4ea8e2a0b1336f506aa5ba8c1f98fb426d734e3735a33', 'checksum_type': 'sha256', 'duration': 4.531283, 'size': 337361576, 'rate': 74451667.66233757, 'start_date': '2021-06-11 16:25:49.870527', 'end_date': '2021-06-11 16:25:54.401810', 'crea_date': '2021-06-11 16:24:31.682483', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '45a68351-a1d1-4a2c-a16d-1e4599c2228b', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'detoc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T04:43:18Z'},
{'file_id': 15, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/detoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '048a8f917b330509597329093df804af76ff74f2e345e975f2a8869239950359', 'checksum_type': 'sha256', 'duration': 3.072413, 'size': 135602216, 'rate': 44135412.78467446, 'start_date': '2021-06-11 16:25:50.473899', 'end_date': '2021-06-11 16:25:53.546312', 'crea_date': '2021-06-11 16:24:31.686100', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'fc72f180-5fe8-43a2-bf13-45ecb88b06c1', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'detoc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T04:50:04Z'},
{'file_id': 16, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'b9dcdb2fd2c8d61dcf8f6cb04bbbcd89bd78a0df710408cbf832d238b483d526', 'checksum_type': 'sha256', 'duration': 6.502651, 'size': 337361600, 'rate': 51880625.3018961, 'start_date': '2021-06-11 16:25:50.508058', 'end_date': '2021-06-11 16:25:57.010709', 'crea_date': '2021-06-11 16:24:31.689914', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5ccdc46f-407b-47d0-880c-f20be1e30044', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dfe', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T12:33:03Z'},
{'file_id': 17, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dfe_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '069324b0531127f459cce9f01c80e3e712daaa3cbb671b4942b50ff82ad0521b', 'checksum_type': 'sha256', 'duration': 5.502325, 'size': 135602240, 'rate': 24644534.810284745, 'start_date': '2021-06-11 16:25:50.541662', 'end_date': '2021-06-11 16:25:56.043987', 'crea_date': '2021-06-11 16:24:31.693466', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '2322558a-595e-4936-9b2a-5de75de05ca5', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dfe', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T12:13:24Z'},
{'file_id': 18, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '14b5ca1cd2a6e7573408c8b10e57850dc6f47fd5755d0170994fdc5d30fd3bf4', 'checksum_type': 'sha256', 'duration': 8.183145, 'size': 337361572, 'rate': 41226395.47508935, 'start_date': '2021-06-11 16:25:50.608341', 'end_date': '2021-06-11 16:25:58.791486', 'crea_date': '2021-06-11 16:24:31.697141', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'ae7c9b91-7d8e-40d2-a9f8-842cd2a3c02e', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dissic', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-02T21:20:39Z'},
{'file_id': 19, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissic_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '59078396f94487e70b9aadd1cfc956038810902138283d59f5a809c4b86953c9', 'checksum_type': 'sha256', 'duration': 1.973526, 'size': 135602212, 'rate': 68710628.59065449, 'start_date': '2021-06-11 16:25:58.742895', 'end_date': '2021-06-11 16:26:00.716421', 'crea_date': '2021-06-11 16:24:31.700881', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'c5750fce-25c2-4ac0-90da-3f1571cd3cef', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dissic', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-02T20:58:55Z'},
{'file_id': 20, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'd2b683d1efe94e2250fa842cffbb6501fab88edc22a7353cff6d12f45093cc24', 'checksum_type': 'sha256', 'duration': 5.421206, 'size': 337361484, 'rate': 62229969.49387277, 'start_date': '2021-06-11 16:25:58.795887', 'end_date': '2021-06-11 16:26:04.217093', 'crea_date': '2021-06-11 16:24:31.704434', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '6d329e8d-e0e4-40c5-b16e-67497fc2fefd', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dissoc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-02T23:10:29Z'},
{'file_id': 21, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/dissoc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'e87d53ef00d8bf5f088704eeb755f873596ff94992ff84380a447005995b3557', 'checksum_type': 'sha256', 'duration': 4.310854, 'size': 135602124, 'rate': 31455976.936356463, 'start_date': '2021-06-11 16:25:58.833056', 'end_date': '2021-06-11 16:26:03.143910', 'crea_date': '2021-06-11 16:24:31.708001', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '661f2700-b468-4e00-8237-8172312d52e8', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'dissoc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-02T21:49:47Z'},
{'file_id': 22, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '9d365d1b86519153b0d046e6c5d337788b6b382626f33456c7f6522b597690c2', 'checksum_type': 'sha256', 'duration': 7.532078, 'size': 337361460, 'rate': 44789958.36208812, 'start_date': '2021-06-11 16:25:58.866043', 'end_date': '2021-06-11 16:26:06.398121', 'crea_date': '2021-06-11 16:24:31.711813', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'ca64c733-5e26-49f0-b1d6-3862473009d0', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'nh4', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T11:32:17Z'},
{'file_id': 23, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/nh4_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'afb68a92eafb092040b3fa05584f1f8385f265b79d0537c4393adb3cc55244bb', 'checksum_type': 'sha256', 'duration': 6.881473, 'size': 135602100, 'rate': 19705388.65734124, 'start_date': '2021-06-11 16:25:58.900124', 'end_date': '2021-06-11 16:26:05.781597', 'crea_date': '2021-06-11 16:24:31.715427', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5d2fc455-3aba-4669-9dbc-811f6053b43a', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'nh4', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T11:22:10Z'},
{'file_id': 24, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '602a81220895c1494516855226ff1d96f0f0182dbc43b42401f198475fbb38d2', 'checksum_type': 'sha256', 'duration': 9.904017, 'size': 337361456, 'rate': 34063093.389278315, 'start_date': '2021-06-11 16:25:58.933597', 'end_date': '2021-06-11 16:26:08.837614', 'crea_date': '2021-06-11 16:24:31.719023', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'b1abc4e9-8dd8-4e2b-aac5-f78338ee96e6', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'no3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T11:12:54Z'},
{'file_id': 25, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/no3_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'a867592c388719d2a0eb9f40152923cae10741d40b6f4e5c716081dfc7c1c8b1', 'checksum_type': 'sha256', 'duration': 2.950505, 'size': 135602096, 'rate': 45958944.65523698, 'start_date': '2021-06-11 16:26:07.274451', 'end_date': '2021-06-11 16:26:10.224956', 'crea_date': '2021-06-11 16:24:31.722824', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '4dc6a042-8602-4751-a760-ad191697f930', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'no3', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T10:40:35Z'},
{'file_id': 26, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '1a13d1b44197ae60eaffa83b9c5a7fa322bc1de8bdc8800106427d3da044c88b', 'checksum_type': 'sha256', 'duration': 5.327969, 'size': 337361464, 'rate': 63318961.502966695, 'start_date': '2021-06-11 16:26:07.313889', 'end_date': '2021-06-11 16:26:12.641858', 'crea_date': '2021-06-11 16:24:31.726397', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '25d54f2a-7af0-4172-8e79-6c3112664ef4', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'o2', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T10:01:36Z'},
{'file_id': 27, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'filename': 'o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/o2_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1950-1989.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '8dca30f1c92c13bcbe975c4a80d14c790475fc15897044953f1ca0f9c127d751', 'checksum_type': 'sha256', 'duration': 4.612305, 'size': 135602104, 'rate': 29400073.065419566, 'start_date': '2021-06-11 16:26:07.355678', 'end_date': '2021-06-11 16:26:11.967983', 'crea_date': '2021-06-11 16:24:31.730424', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '02712118-9b66-4c53-acdc-358ff0f02b6d', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'o2', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T09:38:14Z'},

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
