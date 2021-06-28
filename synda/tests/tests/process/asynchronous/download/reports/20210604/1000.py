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


min_start_date = datetime.datetime.strptime('2021-06-04 08:49:15.849304', "%Y-%m-%d %H:%M:%S.%f")


# # RUN current synda version 3.2

data = [

# {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 10.749319, 'size': 86344659, 'rate': 8032570.156304786, 'start_date': '2021-06-04 08:56:36.809881', 'end_date': '2021-06-04 08:56:47.559200', 'crea_date': '2021-06-04 08:56:15.698313', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
# {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 46.805128, 'size': 88114316, 'rate': 1882578.2508275588, 'start_date': '2021-06-04 08:56:36.822218', 'end_date': '2021-06-04 08:57:23.627346', 'crea_date': '2021-06-04 08:56:15.702014', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
# {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 105.493215, 'size': 795795708, 'rate': 7543572.42785709, 'start_date': '2021-06-04 08:56:36.828385', 'end_date': '2021-06-04 08:58:22.321600', 'crea_date': '2021-06-04 08:56:15.703587', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
# {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 30.665298, 'size': 27452120, 'rate': 895217.780045705, 'start_date': '2021-06-04 08:56:36.834561', 'end_date': '2021-06-04 08:57:07.499859', 'crea_date': '2021-06-04 08:56:15.705249', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
# {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 67.225589, 'size': 138080132, 'rate': 2053981.7360320934, 'start_date': '2021-06-04 08:56:36.840891', 'end_date': '2021-06-04 08:57:44.066480', 'crea_date': '2021-06-04 08:56:15.706806', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
# {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 73.020317, 'size': 337361584, 'rate': 4620105.716604873, 'start_date': '2021-06-04 08:56:36.846695', 'end_date': '2021-06-04 08:57:49.867012', 'crea_date': '2021-06-04 08:56:15.708506', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

]

downloading_duration = {'calculated from os': 103.103283}

data.extend(
    [
        {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 12.887389, 'size': 86344659, 'rate': 6699934.253555937, 'start_date': '2021-06-04 19:37:05.977754', 'end_date': '2021-06-04 19:37:18.865143', 'crea_date': '2021-06-04 19:33:29.627592', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
        {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 40.743715, 'size': 88114316, 'rate': 2162648.0550435814, 'start_date': '2021-06-04 19:37:05.997171', 'end_date': '2021-06-04 19:37:46.740886', 'crea_date': '2021-06-04 19:33:29.631050', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
        {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 103.364365, 'size': 795795708, 'rate': 7698936.746721174, 'start_date': '2021-06-04 19:37:06.007274', 'end_date': '2021-06-04 19:38:49.371639', 'crea_date': '2021-06-04 19:33:29.632655', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
        {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 36.589374, 'size': 27452120, 'rate': 750275.7494566592, 'start_date': '2021-06-04 19:37:06.015801', 'end_date': '2021-06-04 19:37:42.605175', 'crea_date': '2021-06-04 19:33:29.634361', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
        {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 34.715281, 'size': 138080132, 'rate': 3977502.933074343, 'start_date': '2021-06-04 19:37:06.023323', 'end_date': '2021-06-04 19:37:40.738604', 'crea_date': '2021-06-04 19:33:29.635904', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
        {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 80.574214, 'size': 337361584, 'rate': 4186967.1108426824, 'start_date': '2021-06-04 19:37:06.030615', 'end_date': '2021-06-04 19:38:26.604829', 'crea_date': '2021-06-04 19:33:29.637562', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': '', 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},
    ]
)

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

# {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 52.295316, 'size': 86344659, 'rate': 1651097.375527858, 'start_date': '2021-06-04 08:49:20.124700', 'end_date': '2021-06-04 08:50:12.598787', 'crea_date': '2021-06-04 08:44:10.742487', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
# {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 51.69517, 'size': 88114316, 'rate': 1704498.041112932, 'start_date': '2021-06-04 08:49:19.775401', 'end_date': '2021-06-04 08:50:11.652334', 'crea_date': '2021-06-04 08:44:10.746166', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
# {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 96.932527, 'size': 795795708, 'rate': 8209790.177037271, 'start_date': '2021-06-04 08:49:15.849304', 'end_date': '2021-06-04 08:50:54.429929', 'crea_date': '2021-06-04 08:44:10.747738', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
# {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 14.77927, 'size': 27452120, 'rate': 1857474.6925930711, 'start_date': '2021-06-04 08:49:20.421759', 'end_date': '2021-06-04 08:49:35.263277', 'crea_date': '2021-06-04 08:44:10.749399', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
# {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 62.016018, 'size': 138080132, 'rate': 2226523.6700621443, 'start_date': '2021-06-04 08:49:19.370658', 'end_date': '2021-06-04 08:50:21.677368', 'crea_date': '2021-06-04 08:44:10.750934', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
# {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 78.325333, 'size': 337361584, 'rate': 4307183.526433268, 'start_date': '2021-06-04 08:49:19.066329', 'end_date': '2021-06-04 08:50:38.108223', 'crea_date': '2021-06-04 08:44:10.752605', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

# {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 49.122725, 'size': 86344659, 'rate': 1757733.493001457, 'start_date': '2021-06-04 13:13:38.929033', 'end_date': '2021-06-04 13:14:28.051758', 'crea_date': '2021-06-04 13:13:25.692936', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
# {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 38.00824, 'size': 88114316, 'rate': 2318295.085486726, 'start_date': '2021-06-04 13:13:38.527225', 'end_date': '2021-06-04 13:14:16.535465', 'crea_date': '2021-06-04 13:13:25.696586', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
# {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 78.735813, 'size': 795795708, 'rate': 10107163.153316269, 'start_date': '2021-06-04 13:13:37.451983', 'end_date': '2021-06-04 13:14:56.187796', 'crea_date': '2021-06-04 13:13:25.698165', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
# {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 15.094515, 'size': 27452120, 'rate': 1818681.8191906135, 'start_date': '2021-06-04 13:13:39.293501', 'end_date': '2021-06-04 13:13:54.388016', 'crea_date': '2021-06-04 13:13:25.699835', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
# {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 48.962872, 'size': 138080132, 'rate': 2820098.7066281573, 'start_date': '2021-06-04 13:13:38.117794', 'end_date': '2021-06-04 13:14:27.080666', 'crea_date': '2021-06-04 13:13:25.701403', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
# {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 63.858674, 'size': 337361584, 'rate': 5282940.638573234, 'start_date': '2021-06-04 13:13:37.778570', 'end_date': '2021-06-04 13:14:41.637244', 'crea_date': '2021-06-04 13:13:25.703074', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

# {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 42.604297, 'size': 86344659, 'rate': 2026665.5027778065, 'start_date': '2021-06-04 14:34:26.241085', 'end_date': '2021-06-04 14:35:08.845382', 'crea_date': '2021-06-04 14:34:13.897161', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
# {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 48.004779, 'size': 88114316, 'rate': 1835532.16649534, 'start_date': '2021-06-04 14:34:25.862461', 'end_date': '2021-06-04 14:35:13.867240', 'crea_date': '2021-06-04 14:34:13.900683', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
# {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 85.920362, 'size': 795795708, 'rate': 9262015.306685975, 'start_date': '2021-06-04 14:34:24.792120', 'end_date': '2021-06-04 14:35:50.712482', 'crea_date': '2021-06-04 14:34:13.902271', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
# {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 15.953904, 'size': 27452120, 'rate': 1720714.8795680355, 'start_date': '2021-06-04 14:34:26.610294', 'end_date': '2021-06-04 14:34:42.564198', 'crea_date': '2021-06-04 14:34:13.903943', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
# {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 57.610244, 'size': 138080132, 'rate': 2396798.249977903, 'start_date': '2021-06-04 14:34:25.504565', 'end_date': '2021-06-04 14:35:23.114809', 'crea_date': '2021-06-04 14:34:13.905532', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
# {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 75.014655, 'size': 337361584, 'rate': 4497275.685664354, 'start_date': '2021-06-04 14:34:25.161937', 'end_date': '2021-06-04 14:35:40.176592', 'crea_date': '2021-06-04 14:34:13.907285', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

# {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 24.599795, 'size': 86344659, 'rate': 3509974.737594358, 'start_date': '2021-06-04 15:39:00.720366', 'end_date': '2021-06-04 15:39:25.320161', 'crea_date': '2021-06-04 15:38:32.059242', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
# {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 40.317894, 'size': 88114316, 'rate': 2185489.0535701094, 'start_date': '2021-06-04 15:39:00.834293', 'end_date': '2021-06-04 15:39:41.152187', 'crea_date': '2021-06-04 15:38:32.063903', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
# {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 71.253882, 'size': 795795708, 'rate': 11168454.064018574, 'start_date': '2021-06-04 15:39:06.902086', 'end_date': '2021-06-04 15:40:18.155968', 'crea_date': '2021-06-04 15:38:32.065508', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
# {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 23.532575, 'size': 27452120, 'rate': 1166558.2708224664, 'start_date': '2021-06-04 15:38:49.095444', 'end_date': '2021-06-04 15:39:12.628019', 'crea_date': '2021-06-04 15:38:32.067177', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
# {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 42.065487, 'size': 138080132, 'rate': 3282504.0632478595, 'start_date': '2021-06-04 15:39:04.901890', 'end_date': '2021-06-04 15:39:46.967377', 'crea_date': '2021-06-04 15:38:32.068748', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
# {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 60.028227, 'size': 337361584, 'rate': 5620049.114560721, 'start_date': '2021-06-04 15:39:05.374529', 'end_date': '2021-06-04 15:40:05.402756', 'crea_date': '2021-06-04 15:38:32.070446', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

# {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 28.677724, 'size': 86344659, 'rate': 3010861.6360210455, 'start_date': '2021-06-04 16:01:54.907950', 'end_date': '2021-06-04 16:02:23.585674', 'crea_date': '2021-06-04 16:01:16.079119', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
# {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 25.75888, 'size': 88114316, 'rate': 3420735.528873926, 'start_date': '2021-06-04 16:02:02.210806', 'end_date': '2021-06-04 16:02:27.969686', 'crea_date': '2021-06-04 16:01:16.082503', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
# {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 72.674928, 'size': 795795708, 'rate': 10950072.189958, 'start_date': '2021-06-04 16:02:04.568240', 'end_date': '2021-06-04 16:03:17.243168', 'crea_date': '2021-06-04 16:01:16.084096', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
# {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 24.115444, 'size': 27452120, 'rate': 1138362.619406883, 'start_date': '2021-06-04 16:01:42.119397', 'end_date': '2021-06-04 16:02:06.234841', 'crea_date': '2021-06-04 16:01:16.085758', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
# {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 49.54391, 'size': 138080132, 'rate': 2787025.3276336086, 'start_date': '2021-06-04 16:02:03.355640', 'end_date': '2021-06-04 16:02:52.899550', 'crea_date': '2021-06-04 16:01:16.087340', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
# {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 67.953104, 'size': 337361584, 'rate': 4964623.6027717, 'start_date': '2021-06-04 16:02:03.548446', 'end_date': '2021-06-04 16:03:11.501550', 'crea_date': '2021-06-04 16:01:16.089019', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

# {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 21.547451, 'size': 86344659, 'rate': 4007186.696932273, 'start_date': '2021-06-04 16:06:25.427932', 'end_date': '2021-06-04 16:06:46.975383', 'crea_date': '2021-06-04 16:06:04.549748', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
# {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 37.074795, 'size': 88114316, 'rate': 2376663.6066362606, 'start_date': '2021-06-04 16:06:33.467568', 'end_date': '2021-06-04 16:07:10.542363', 'crea_date': '2021-06-04 16:06:04.553510', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
# {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 72.938706, 'size': 795795708, 'rate': 10910471.979034012, 'start_date': '2021-06-04 16:06:45.482725', 'end_date': '2021-06-04 16:07:58.421431', 'crea_date': '2021-06-04 16:06:04.555078', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
# {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 33.369057, 'size': 27452120, 'rate': 822681.9235557062, 'start_date': '2021-06-04 16:06:20.309297', 'end_date': '2021-06-04 16:06:53.678354', 'crea_date': '2021-06-04 16:06:04.556729', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
# {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 58.145915, 'size': 138080132, 'rate': 2374717.6736319307, 'start_date': '2021-06-04 16:06:41.461251', 'end_date': '2021-06-04 16:07:39.607166', 'crea_date': '2021-06-04 16:06:04.558301', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
# {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 61.376024, 'size': 337361584, 'rate': 5496634.711952016, 'start_date': '2021-06-04 16:06:45.259186', 'end_date': '2021-06-04 16:07:46.635210', 'crea_date': '2021-06-04 16:06:04.559966', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

]

downloading_duration = {'calculated from os': 85.085474}

data.extend(
    [
        {'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 28.938831, 'size': 86344659, 'rate': 2983695.471320179, 'start_date': '2021-06-04 19:53:57.828268', 'end_date': '2021-06-04 19:54:26.767099', 'crea_date': '2021-06-04 19:53:30.362854', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
        {'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 28.569567, 'size': 88114316, 'rate': 3084202.0111820386, 'start_date': '2021-06-04 19:54:05.341299', 'end_date': '2021-06-04 19:54:33.910866', 'crea_date': '2021-06-04 19:53:30.366596', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
        {'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 73.840972, 'size': 795795708, 'rate': 10777156.45454938, 'start_date': '2021-06-04 19:54:09.416853', 'end_date': '2021-06-04 19:55:23.257825', 'crea_date': '2021-06-04 19:53:30.368192', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
        {'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 28.185796, 'size': 27452120, 'rate': 973970.0095750357, 'start_date': '2021-06-04 19:53:48.734336', 'end_date': '2021-06-04 19:54:16.920132', 'crea_date': '2021-06-04 19:53:30.369928', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
        {'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 49.625509, 'size': 138080132, 'rate': 2782442.634492676, 'start_date': '2021-06-04 19:54:05.820718', 'end_date': '2021-06-04 19:54:55.446227', 'crea_date': '2021-06-04 19:53:30.371512', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
        {'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 63.988847, 'size': 337361584, 'rate': 5272193.512097507, 'start_date': '2021-06-04 19:54:06.289337', 'end_date': '2021-06-04 19:55:10.278184', 'crea_date': '2021-06-04 19:53:30.373208', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},
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


# RUN STRATEGY : big file customized chunksize

data = [

{'file_id': 1, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'file_functional_id': 'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.1pctCO2.r1i1p1f1.Amon.tas.gr.v20180605.tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'filename': 'tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'local_path': 'CMIP6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Amon/tas/gr/v20180605/tas_Amon_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_185001-199912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '3b98f8f9aa97e156d18f05856da7c216287ecbd6c4e5b0af929ddd7c8750be87', 'checksum_type': 'sha256', 'duration': 43.020495, 'size': 86344659, 'rate': 2007058.7053914652, 'start_date': '2021-06-04 09:01:38.014271', 'end_date': '2021-06-04 09:02:21.214661', 'crea_date': '2021-06-04 09:00:23.953254', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'hdl:21.14100/ea6bf619-23fd-4270-9fdc-d89fb3389271', 'model': None, 'project': 'CMIP6', 'variable': 'tas', 'last_access_date': None, 'dataset_id': 1, 'insertion_group_id': 1, 'timestamp': '2018-05-13T14:08:21Z'},
{'file_id': 2, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'filename': 'tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '60bf5ebfebe4687b4461e19f9be4a188437a9d91f98498faa16a64d2c3f785a9', 'checksum_type': 'sha256', 'duration': 60.407163, 'size': 88114316, 'rate': 1458673.3033630466, 'start_date': '2021-06-04 09:01:37.645730', 'end_date': '2021-06-04 09:02:38.233641', 'crea_date': '2021-06-04 09:00:23.956945', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '5b206bf4-bf14-4785-92e7-6b97e73d4bf4', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 2, 'insertion_group_id': 1, 'timestamp': '2012-12-07T08:37:18Z'},
{'file_id': 3, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CNRM-CERFACS.CNRM-CM5.historical.mon.seaIce.OImon.r1i1p1.v20210408.evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'filename': 'evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20210408/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'c49041694c147cafcc51254b35aff9111f72bf0bba5c475f58fb4e49f21bef59', 'checksum_type': 'sha256', 'duration': 88.787228, 'size': 795795708, 'rate': 8962952.509340646, 'start_date': '2021-06-04 09:01:36.662153', 'end_date': '2021-06-04 09:03:07.089515', 'crea_date': '2021-06-04 09:00:23.958601', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'd246a2b8-8497-4149-93dc-ca7b12022327', 'model': 'CNRM-CM5', 'project': 'CMIP5', 'variable': 'evap', 'last_access_date': None, 'dataset_id': 3, 'insertion_group_id': 1, 'timestamp': '2013-01-18T10:04:52Z'},
{'file_id': 4, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.amip.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '35e7670dfd41f1a6ebc52d47c2edd2ffcf00ed6a4aedafb207ad7db5ec9e0541', 'checksum_type': 'sha256', 'duration': 20.374832, 'size': 27452120, 'rate': 1347354.4223579364, 'start_date': '2021-06-04 09:01:38.384181', 'end_date': '2021-06-04 09:01:58.818704', 'crea_date': '2021-06-04 09:00:23.960308', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '8510cc96-66bb-4afd-a24c-600d5928bdbd', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 4, 'insertion_group_id': 1, 'timestamp': '2020-02-21T16:04:23Z'},
{'file_id': 5, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file_functional_id': 'cmip5.output1.CSIRO-QCCCE.CSIRO-Mk3-6-0.historical.mon.atmos.Amon.r1i1p1.v20210408.tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'filename': 'tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v20210408/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': 'bcc0a42c5db47c4f3ac4131a32e8a6438a5b5eb405295d8985ffc8d5c39866ac', 'checksum_type': 'sha256', 'duration': 64.086699, 'size': 138080132, 'rate': 2154583.309088833, 'start_date': '2021-06-04 09:01:37.322727', 'end_date': '2021-06-04 09:02:41.694377', 'crea_date': '2021-06-04 09:00:23.961892', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': 'f11f3ffd-34ca-4172-8138-ae5907252456', 'model': 'CSIRO-Mk3.6.0', 'project': 'CMIP5', 'variable': 'tasmin', 'last_access_date': None, 'dataset_id': 5, 'insertion_group_id': 1, 'timestamp': '2020-02-23T20:20:19Z'},
{'file_id': 6, 'url': 'http://vesgint-data.ipsl.upmc.fr/thredds/fileServer/cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'file_functional_id': 'cmip5.output1.IPSL.IPSL-CM5A-LR.1pctCO2.yr.ocnBgchem.Oyr.r1i1p1.v20180314.calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'filename': 'calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'local_path': 'cmip5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/yr/ocnBgchem/Oyr/r1i1p1/v20180314/calc_Oyr_IPSL-CM5A-LR_1pctCO2_r1i1p1_1850-1949.nc', 'data_node': 'vesgint-data.ipsl.upmc.fr', 'checksum': '26aaaad19d92973a5ffe22b02b897161889daf73487a16c14427655b79f17d5e', 'checksum_type': 'sha256', 'duration': 79.506578, 'size': 337361584, 'rate': 4243190.846422795, 'start_date': '2021-06-04 09:01:36.991682', 'end_date': '2021-06-04 09:02:57.211430', 'crea_date': '2021-06-04 09:00:23.963598', 'status': 'done', 'error_msg': '', 'sdget_status': '0', 'sdget_error_msg': None, 'priority': 1000, 'tracking_id': '2ce09466-58b7-4ef0-bb6f-e3a2ba0cbe75', 'model': 'IPSL-CM5A-LR', 'project': 'CMIP5', 'variable': 'calc', 'last_access_date': None, 'dataset_id': 6, 'insertion_group_id': 1, 'timestamp': '2011-07-03T05:25:54Z'},

]

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
