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

{'name': '( Batch 0 - Item 7)', 'file size': 27452120, 'elapsed time': 11.102229, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.009207, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:19:59.518346', 'finish': '2021-04-08 15:20:10.620575', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 3)', 'file size': 34680756, 'elapsed time': 13.943769, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.009192, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:19:59.517546', 'finish': '2021-04-08 15:20:13.461315', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 6)', 'file size': 54977076, 'elapsed time': 21.094346, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.013984, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:19:59.518147', 'finish': '2021-04-08 15:20:20.612493', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 1)', 'file size': 78675556, 'elapsed time': 28.942806, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.019864, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:19:59.517129', 'finish': '2021-04-08 15:20:28.459935', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 8)', 'file size': 54977076, 'elapsed time': 20.776917, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.013617, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:20:10.620880', 'finish': '2021-04-08 15:20:31.397797', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 10)', 'file size': 47212396, 'elapsed time': 18.582788, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.011628, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:20:20.612636', 'finish': '2021-04-08 15:20:39.195424', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 4)', 'file size': 54977076, 'elapsed time': 42.596791, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013542, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:19:59.517760', 'finish': '2021-04-08 15:20:42.114551', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 12)', 'file size': 78675556, 'elapsed time': 31.926173, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.019973, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:20:31.397938', 'finish': '2021-04-08 15:21:03.324111', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 13)', 'file size': 88114316, 'elapsed time': 35.891412, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.024165, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:20:39.195571', 'finish': '2021-04-08 15:21:15.086983', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 11)', 'file size': 138079884, 'elapsed time': 52.934528, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.039654, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:20:28.460119', 'finish': '2021-04-08 15:21:21.394647', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 15)', 'file size': 54977076, 'elapsed time': 25.524371, 'waiting_times': 2e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.015875, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:21:03.324346', 'finish': '2021-04-08 15:21:28.848717', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 16)', 'file size': 47212548, 'elapsed time': 20.58307, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.011508, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:21:15.087161', 'finish': '2021-04-08 15:21:35.670231', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 14)', 'file size': 138080336, 'elapsed time': 57.287963, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.039044, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:20:42.114765', 'finish': '2021-04-08 15:21:39.402728', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 18)', 'file size': 27452324, 'elapsed time': 12.813864, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.0082, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:21:28.848860', 'finish': '2021-04-08 15:21:41.662724', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 17)', 'file size': 54977076, 'elapsed time': 22.365582, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.015013, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:21:21.394820', 'finish': '2021-04-08 15:21:43.760402', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 21)', 'file size': 47212016, 'elapsed time': 21.56822, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.011525, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:21:41.662929', 'finish': '2021-04-08 15:22:03.231149', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 20)', 'file size': 54977076, 'elapsed time': 24.005185, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.014689, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:21:39.402951', 'finish': '2021-04-08 15:22:03.408136', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 19)', 'file size': 78675024, 'elapsed time': 31.162733, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.019735, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:21:35.670368', 'finish': '2021-04-08 15:22:06.833101', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 25)', 'file size': 27451904, 'elapsed time': 13.112055, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.006856, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:22:06.833348', 'finish': '2021-04-08 15:22:19.945403', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 22)', 'file size': 88114468, 'elapsed time': 36.708128, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.024776, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:21:43.760612', 'finish': '2021-04-08 15:22:20.468740', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 23)', 'file size': 54977076, 'elapsed time': 24.362214, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013553, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:22:03.231355', 'finish': '2021-04-08 15:22:27.593569', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 26)', 'file size': 54977076, 'elapsed time': 23.767815, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.014062, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:22:19.945599', 'finish': '2021-04-08 15:22:43.713414', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 24)', 'file size': 138079984, 'elapsed time': 57.154175, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.037746, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:22:03.408347', 'finish': '2021-04-08 15:23:00.562522', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 28)', 'file size': 78675404, 'elapsed time': 33.222525, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.019761, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:22:27.593793', 'finish': '2021-04-08 15:23:00.816318', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 27)', 'file size': 138080132, 'elapsed time': 58.734701, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.034053, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:22:20.468933', 'finish': '2021-04-08 15:23:19.203634', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 31)', 'file size': 54977076, 'elapsed time': 24.556062, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.014968, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:23:00.816456', 'finish': '2021-04-08 15:23:25.372518', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 30)', 'file size': 88113936, 'elapsed time': 36.524294, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.021618, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:23:00.562673', 'finish': '2021-04-08 15:23:37.086967', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 32)', 'file size': 54977076, 'elapsed time': 27.959471, 'waiting_times': 2e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.014897, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:23:19.203887', 'finish': '2021-04-08 15:23:47.163358', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 33)', 'file size': 54977076, 'elapsed time': 24.210636, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013639, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:23:25.372834', 'finish': '2021-04-08 15:23:49.583470', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 35)', 'file size': 27451972, 'elapsed time': 12.949674, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.007496, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:23:47.163502', 'finish': '2021-04-08 15:24:00.113176', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 34)', 'file size': 78675404, 'elapsed time': 34.109612, 'waiting_times': 2e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.02015, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:23:37.087250', 'finish': '2021-04-08 15:24:11.196862', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 36)', 'file size': 78675024, 'elapsed time': 31.315491, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.019493, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:23:49.583615', 'finish': '2021-04-08 15:24:20.899106', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 37)', 'file size': 54977076, 'elapsed time': 21.612466, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.013756, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:24:00.113413', 'finish': '2021-04-08 15:24:21.725879', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 9)', 'file size': 795795032, 'elapsed time': 285.154298, 'waiting_times': 1e-06, 'downloading_chunk_lengths': 0, 'writing_times': 0.262282, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:20:13.461568', 'finish': '2021-04-08 15:24:58.615866', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},
{'name': '( Batch 0 - Item 29)', 'file size': 795795708, 'elapsed time': 160.011463, 'waiting_times': 0.0, 'downloading_chunk_lengths': 0, 'writing_times': 0.219483, 'writing_chunk_lengths': 0, 'downloaded mean chunk size observed': 0, 'start': '2021-04-08 15:22:43.713570', 'finish': '2021-04-08 15:25:23.725033', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'process_name': 'unchunked_process'},

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
