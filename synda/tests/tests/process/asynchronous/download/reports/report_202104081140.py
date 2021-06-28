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


# Observations

files = {
    'cmip5\/output1\/CSIRO\-QCCCE\/CSIRO\-Mk3\-6\-0\/amip\/mon\/atmos\/Amon\/r1i1p1\/v1\/psl\/psl_Amon_CSIRO\-Mk3\-6\-0_amip_r1i1p1_197901\-200912\.nc': 27451904,
    'cmip5\/output1\/CNRM\-CERFACS\/CNRM\-CM5\/historical\/mon\/ocnBgchem\/Omon\/r1i1p1\/v20120731\/dissic\/dissic_Omon_CNRM\-CM5_historical_r1i1p1_196001\-196912\.nc': 54977076,
'cmip5\/output1\/CNRM\-CERFACS\/CNRM\-CM5\/historical\/mon\/ocnBgchem\/Omon\/r1i1p1\/v20120731\/dissic\/dissic_Omon_CNRM\-CM5_historical_r1i1p1_191001\-191912\.nc': 54977076,
'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc': 27452120,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc': 34680756,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc': 78675556,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc': 47212396,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc': 78675556,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc': 88114316,
'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc': 138079884,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc': 47212548,
'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc': 27452324,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc': 54977076,
'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc': 138080336,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc': 47212016,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc': 78675024,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc': 88114468,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc': 78675404,
'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc': 138079984,
'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc': 138080132,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc': 88113936,
'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc': 27451972,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc': 78675404,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc': 54977076,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc': 78675024,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc': 795795032,
'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc': 795795708,

}

sizes = 0
for key in files.keys():
    sizes += files[key]

coeff_bytes_2_go = 1.0 / (8 * 1024 * 1024 * 1024)

# download speed unit : KiB/s
# file size unit : byte
# elapsed time unit : s

columns = [
    "name",
    "file size",
    "elapsed time",
    "waiting_times",
    "downloading_chunk_lengths",
    "writing_times",
    "writing_chunk_lengths",
    "downloaded mean chunk size observed",
    "start",
    "finish",
    "strategy",
    "sdget_status",
    "local_path",
    "sdget_error_msg",
    "process_name",
]

figs = make_subplots(
    rows=2,
    cols=2,
    shared_xaxes=False,
    vertical_spacing=0.05,
    subplot_titles=(
        '{} Downloads ({} Go)'.format(
            len(files),
            sizes * coeff_bytes_2_go,
        ),
        'synda version 3.2',
        'asyncio - aiohttp',
    ),
    specs=[

        [{"rowspan": 2}, {}],
        [None, {}],
    ],
)
figs.update_xaxes(title_text="Go", row=1, col=1)
figs.update_yaxes(title_text="Elapsed time (in seconds)", row=1, col=1)

# # RUN current synda version 3.2

data = [

{'index': 2, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 24.020677, 'start': '2021-04-08 14:44:52.488416', 'finish': '2021-04-08 14:45:16.509093', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc'},
{'index': 6, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 24.917701, 'start': '2021-04-08 14:44:52.494010', 'finish': '2021-04-08 14:45:17.411711', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc'},
{'index': 0, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 25.166313, 'start': '2021-04-08 14:44:52.485682', 'finish': '2021-04-08 14:45:17.651995', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc'},
{'index': 5, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 29.249886, 'start': '2021-04-08 14:44:52.492287', 'finish': '2021-04-08 14:45:21.742173', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc'},
{'index': 4, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 29.440942, 'start': '2021-04-08 14:44:52.490552', 'finish': '2021-04-08 14:45:21.931494', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc'},
{'index': 1, 'download speed': 0.0, 'file size': 78675556, 'elapsed time': 31.71801, 'start': '2021-04-08 14:44:52.487126', 'finish': '2021-04-08 14:45:24.205136', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc'},
{'index': 10, 'download speed': 0.0, 'file size': 47212396, 'elapsed time': 37.281076, 'start': '2021-04-08 14:45:17.652105', 'finish': '2021-04-08 14:45:54.933181', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc'},
{'index': 8, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 41.366375, 'start': '2021-04-08 14:45:16.509218', 'finish': '2021-04-08 14:45:57.875593', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc'},
{'index': 11, 'download speed': 0.0, 'file size': 138079884, 'elapsed time': 37.724356, 'start': '2021-04-08 14:45:21.742296', 'finish': '2021-04-08 14:45:59.466652', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'index': 12, 'download speed': 0.0, 'file size': 78675556, 'elapsed time': 37.813286, 'start': '2021-04-08 14:45:21.931635', 'finish': '2021-04-08 14:45:59.744921', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc'},
{'index': 13, 'download speed': 0.0, 'file size': 88114316, 'elapsed time': 42.766766, 'start': '2021-04-08 14:45:24.205254', 'finish': '2021-04-08 14:46:06.972020', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc'},
{'index': 16, 'download speed': 0.0, 'file size': 47212548, 'elapsed time': 30.142396, 'start': '2021-04-08 14:45:59.466770', 'finish': '2021-04-08 14:46:29.609166', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc'},
{'index': 15, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 32.53197, 'start': '2021-04-08 14:45:57.875749', 'finish': '2021-04-08 14:46:30.407719', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc'},
{'index': 17, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 31.285745, 'start': '2021-04-08 14:45:59.745063', 'finish': '2021-04-08 14:46:31.030808', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc'},
{'index': 20, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 26.454518, 'start': '2021-04-08 14:46:30.407834', 'finish': '2021-04-08 14:46:56.862352', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc'},
{'index': 19, 'download speed': 0.0, 'file size': 78675024, 'elapsed time': 28.811385, 'start': '2021-04-08 14:46:29.609286', 'finish': '2021-04-08 14:46:58.420671', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc'},
{'index': 3, 'download speed': 0.0, 'file size': 34680756, 'elapsed time': 142.510066, 'start': '2021-04-08 14:44:52.490254', 'finish': '2021-04-08 14:47:15.000320', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc'},
{'index': 22, 'download speed': 0.0, 'file size': 88114468, 'elapsed time': 27.854911, 'start': '2021-04-08 14:46:56.862467', 'finish': '2021-04-08 14:47:24.717378', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc'},
{'index': 25, 'download speed': 0.0, 'file size': 27451904, 'elapsed time': 17.918771, 'start': '2021-04-08 14:47:24.717492', 'finish': '2021-04-08 14:47:42.636263', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'index': 9, 'download speed': 0.0, 'file size': 795795032, 'elapsed time': 149.605791, 'start': '2021-04-08 14:45:17.411863', 'finish': '2021-04-08 14:47:47.017654', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc'},
{'index': 24, 'download speed': 0.0, 'file size': 138079984, 'elapsed time': 46.47029, 'start': '2021-04-08 14:47:15.000440', 'finish': '2021-04-08 14:48:01.470730', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'index': 26, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 25.066714, 'start': '2021-04-08 14:47:42.636394', 'finish': '2021-04-08 14:48:07.703108', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc'},
{'index': 27, 'download speed': 0.0, 'file size': 138080132, 'elapsed time': 23.835631, 'start': '2021-04-08 14:47:47.017776', 'finish': '2021-04-08 14:48:10.853407', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'index': 18, 'download speed': 0.0, 'file size': 27452324, 'elapsed time': 128.418849, 'start': '2021-04-08 14:46:06.972138', 'finish': '2021-04-08 14:48:15.390987', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'index': 30, 'download speed': 0.0, 'file size': 88113936, 'elapsed time': 11.715464, 'start': '2021-04-08 14:48:10.853525', 'finish': '2021-04-08 14:48:22.568989', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc'},
{'index': 31, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 18.561953, 'start': '2021-04-08 14:48:15.391128', 'finish': '2021-04-08 14:48:33.953081', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc'},
{'index': 28, 'download speed': 0.0, 'file size': 78675404, 'elapsed time': 33.750174, 'start': '2021-04-08 14:48:01.470845', 'finish': '2021-04-08 14:48:35.221019', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc'},
{'index': 33, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 7.484472, 'start': '2021-04-08 14:48:33.953193', 'finish': '2021-04-08 14:48:41.437665', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc'},
{'index': 35, 'download speed': 0.0, 'file size': 27451972, 'elapsed time': 5.227932, 'start': '2021-04-08 14:48:41.437789', 'finish': '2021-04-08 14:48:46.665721', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'index': 21, 'download speed': 0.0, 'file size': 47212016, 'elapsed time': 139.249786, 'start': '2021-04-08 14:46:31.030957', 'finish': '2021-04-08 14:48:50.280743', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc'},
{'index': 36, 'download speed': 0.0, 'file size': 78675024, 'elapsed time': 11.23966, 'start': '2021-04-08 14:48:46.665838', 'finish': '2021-04-08 14:48:57.905498', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc'},
{'index': 34, 'download speed': 0.0, 'file size': 78675404, 'elapsed time': 33.093104, 'start': '2021-04-08 14:48:35.221148', 'finish': '2021-04-08 14:49:08.314252', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc'},
{'index': 23, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 129.930953, 'start': '2021-04-08 14:46:58.420804', 'finish': '2021-04-08 14:49:08.351757', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc'},
{'index': 14, 'download speed': 0.0, 'file size': 138080336, 'elapsed time': 256.396906, 'start': '2021-04-08 14:45:54.933315', 'finish': '2021-04-08 14:50:11.330221', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'index': 32, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 149.239199, 'start': '2021-04-08 14:48:22.569131', 'finish': '2021-04-08 14:50:51.808330', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc'},
{'index': 37, 'download speed': 0.0, 'file size': 54977076, 'elapsed time': 137.799393, 'start': '2021-04-08 14:48:50.280888', 'finish': '2021-04-08 14:51:08.080281', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc'},
{'index': 7, 'download speed': 0.0, 'file size': 27452120, 'elapsed time': 381.352451, 'start': '2021-04-08 14:44:52.494274', 'finish': '2021-04-08 14:51:13.846725', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'index': 29, 'download speed': 0.0, 'file size': 795795708, 'elapsed time': 205.734123, 'start': '2021-04-08 14:48:07.703219', 'finish': '2021-04-08 14:51:33.437342', 'strategy': 'current32', 'status_code': 0, 'local_path': '/home_local/journoud/DEV/WORKSPACES/synda/data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc'},


]

current32 = pd.DataFrame(data, columns=columns)

current32["start"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in current32["start"]]
current32["finish"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in current32["finish"]]

current32 = current32.sort_values(by=['file size'])

current32["file size"] = current32["file size"] * coeff_bytes_2_go

color = '#ddd'

current32_duration = dict(
    duration=current32["elapsed time"].max(),
    color=color,
)

x = current32["file size"]
y = current32["elapsed time"]

figs.add_trace(
    go.Scatter(
        x=x,
        y=y,
        name='synda 3.2 - observations',
        marker=dict(color=color, size=10),
        mode="markers",
    ),
    row=1,
    col=1,
)

# RUN asyncio aiohttp

data = [

{'name': '( Batch 0 - Item 7)', 'file size': 27452120, 'elapsed time': 17.985888, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.007333, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:05.618882', 'finish': '2021-04-08 11:59:23.604770', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 3)', 'file size': 34680756, 'elapsed time': 23.017264, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.008441, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:05.618200', 'finish': '2021-04-08 11:59:28.635464', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 5)', 'file size': 54977076, 'elapsed time': 24.642668, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.015229, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:05.618544', 'finish': '2021-04-08 11:59:30.261212', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 0)', 'file size': 54977076, 'elapsed time': 34.903952, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.01358, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:05.617492', 'finish': '2021-04-08 11:59:40.521444', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 2)', 'file size': 54977076, 'elapsed time': 34.949295, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.014893, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:05.618027', 'finish': '2021-04-08 11:59:40.567322', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 4)', 'file size': 54977076, 'elapsed time': 35.477568, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.01339, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:05.618374', 'finish': '2021-04-08 11:59:41.095942', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 1)', 'file size': 78675556, 'elapsed time': 46.470145, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.01986, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:05.617837', 'finish': '2021-04-08 11:59:52.087982', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 6)', 'file size': 54977076, 'elapsed time': 51.657499, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013664, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:05.618717', 'finish': '2021-04-08 11:59:57.276216', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 10)', 'file size': 47212396, 'elapsed time': 27.381538, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.014465, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:30.261438', 'finish': '2021-04-08 11:59:57.642976', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 8)', 'file size': 54977076, 'elapsed time': 36.840011, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013678, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:23.604976', 'finish': '2021-04-08 12:00:00.444987', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 15)', 'file size': 54977076, 'elapsed time': 23.984408, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013347, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:57.276441', 'finish': '2021-04-08 12:00:21.260849', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 17)', 'file size': 54977076, 'elapsed time': 22.23163, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013858, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:00:00.445198', 'finish': '2021-04-08 12:00:22.676828', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 11)', 'file size': 138079884, 'elapsed time': 54.773112, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.033704, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:40.521666', 'finish': '2021-04-08 12:00:35.294778', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 14)', 'file size': 138080336, 'elapsed time': 57.596565, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.037929, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:52.088125', 'finish': '2021-04-08 12:00:49.684690', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 19)', 'file size': 78675024, 'elapsed time': 28.144762, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.021774, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:00:22.677114', 'finish': '2021-04-08 12:00:50.821876', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 20)', 'file size': 54977076, 'elapsed time': 19.423614, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.015241, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:00:35.294958', 'finish': '2021-04-08 12:00:54.718572', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 21)', 'file size': 47212016, 'elapsed time': 16.022117, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013194, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:00:49.684931', 'finish': '2021-04-08 12:01:05.707048', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 23)', 'file size': 54977076, 'elapsed time': 18.866272, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.014186, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:00:54.718722', 'finish': '2021-04-08 12:01:13.584994', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 22)', 'file size': 88114468, 'elapsed time': 30.858885, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.022201, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:00:50.822059', 'finish': '2021-04-08 12:01:21.680944', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 25)', 'file size': 27451904, 'elapsed time': 11.374885, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.007587, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:01:13.585198', 'finish': '2021-04-08 12:01:24.960083', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 26)', 'file size': 54977076, 'elapsed time': 18.552435, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013901, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:01:21.681099', 'finish': '2021-04-08 12:01:40.233534', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 24)', 'file size': 138079984, 'elapsed time': 46.339996, 'waiting_times': 2e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.034056, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:01:05.707258', 'finish': '2021-04-08 12:01:52.047254', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 28)', 'file size': 78675404, 'elapsed time': 27.560375, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.019642, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:01:40.233681', 'finish': '2021-04-08 12:02:07.794056', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 27)', 'file size': 138080132, 'elapsed time': 46.758061, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.03711, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:01:24.960240', 'finish': '2021-04-08 12:02:11.718301', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 31)', 'file size': 54977076, 'elapsed time': 19.536297, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013363, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:02:11.718552', 'finish': '2021-04-08 12:02:31.254849', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 30)', 'file size': 88113936, 'elapsed time': 32.126567, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.021329, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:02:07.794207', 'finish': '2021-04-08 12:02:39.920774', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 32)', 'file size': 54977076, 'elapsed time': 21.707289, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013482, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:02:31.255154', 'finish': '2021-04-08 12:02:52.962443', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 33)', 'file size': 54977076, 'elapsed time': 19.60345, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013612, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:02:39.921109', 'finish': '2021-04-08 12:02:59.524559', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 35)', 'file size': 27451972, 'elapsed time': 10.616705, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.0063, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:02:59.524786', 'finish': '2021-04-08 12:03:10.141491', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 34)', 'file size': 78675404, 'elapsed time': 27.294518, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.019489, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:02:52.962586', 'finish': '2021-04-08 12:03:20.257104', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 36)', 'file size': 78675024, 'elapsed time': 27.491727, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.019588, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:03:10.141687', 'finish': '2021-04-08 12:03:37.633414', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 37)', 'file size': 54977076, 'elapsed time': 19.4142, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.01379, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:03:20.257347', 'finish': '2021-04-08 12:03:39.671547', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 9)', 'file size': 795795032, 'elapsed time': 258.953567, 'waiting_times': 2e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.235164, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 11:59:28.635634', 'finish': '2021-04-08 12:03:47.589201', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 29)', 'file size': 795795708, 'elapsed time': 151.374635, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.218996, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 12:01:52.047410', 'finish': '2021-04-08 12:04:23.422045', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},

]


asyncio_aiohttp = pd.DataFrame(data, columns=columns)

asyncio_aiohttp = asyncio_aiohttp.sort_values(by=['file size'])

# correction = asyncio_aiohttp["download speed"].to_numpy() / asyncio_aiohttp["download speed"].max()

asyncio_aiohttp["start"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in asyncio_aiohttp["start"]]
asyncio_aiohttp["finish"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in asyncio_aiohttp["finish"]]

# adf["elapsed time"] = adf["elapsed time"] * correction

asyncio_aiohttp["file size"] = asyncio_aiohttp["file size"] * coeff_bytes_2_go

color = '#ff6666'

asyncio_aiohttp_duration = dict(
    duration=asyncio_aiohttp["elapsed time"].max(),
    color=color,
)

x2 = asyncio_aiohttp["file size"]
y2 = asyncio_aiohttp["elapsed time"]

figs.add_trace(
    go.Scatter(
        x=x2,
        y=y2,
        name='aiohttp - observations',
        marker=dict(color=color, size=10),
        mode="markers",
    ),
    row=1,
    col=1,
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
 'current32': 'rgb(120,120,120)',
 'asyncio aiohttp': 'rgb(31, 230, 0)',
}

# current32

row = 1
col = 2

current32_fig = px.timeline(
 current32,
 title="Downloads",
 x_start="start",
 x_end="finish",
 y=current32.index,
 color="strategy",
 color_discrete_map=VIEW_COLORS,
 text='elapsed time',
)

for trace in current32_fig.data:
    figs.add_trace(trace, row=row, col=col)

figs.update_xaxes(type="date", row=row, col=col)

figs.update_yaxes(title_text="File", row=row, col=col)

# asyncio - aiohttp

row = 2
col = 2

asyncio_fig = px.timeline(
 asyncio_aiohttp,
 title="Downloads",
 x_start="start",
 x_end="finish",
 y=asyncio_aiohttp.index,
 color="strategy",
 color_discrete_map=VIEW_COLORS,
 text='elapsed time',
)

for trace in asyncio_fig.data:
    figs.add_trace(trace, row=row, col=col)

figs.update_xaxes(type="date", row=row, col=col)

figs.update_yaxes(title_text="File", row=row, col=col)


titles = (
 '{} Downloads ({} Go)'.format(
     len(files),
     sizes * coeff_bytes_2_go,
 ),
 'synda version 3.2 ({} s)'.format(current32_duration["duration"]),
 'asyncio - aiohttp ({} s)'.format(asyncio_aiohttp_duration["duration"]),
)

# rotate all the subtitles of 90 degrees
for i, annotation in enumerate(figs['layout']['annotations']):
    annotation['text'] = titles[i]

figs.show()
