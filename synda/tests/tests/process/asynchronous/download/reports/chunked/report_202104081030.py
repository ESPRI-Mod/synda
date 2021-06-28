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

{'name': '( Batch 0 - Item 3)', 'file size': 34680756, 'elapsed time': 17.394291, 'waiting_times': 16.063422, 'downloading_chunk_lengths': 16320.355764705882, 'writing_times': 0.237941, 'writing_chunk_lengths': 16328.0395480226, 'downloaded mean chunk size observed': 16320.355764705882, 'start': '2021-04-08 10:10:27.123604', 'finish': '2021-04-08 10:10:44.517895', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc'},
{'name': '( Batch 0 - Item 7)', 'file size': 27452120, 'elapsed time': 22.733297, 'waiting_times': 21.570262, 'downloading_chunk_lengths': 15840.807847663013, 'writing_times': 0.186126, 'writing_chunk_lengths': 15849.953810623556, 'downloaded mean chunk size observed': 15840.807847663013, 'start': '2021-04-08 10:10:27.124284', 'finish': '2021-04-08 10:10:49.857581', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'name': '( Batch 0 - Item 5)', 'file size': 54977076, 'elapsed time': 30.373669, 'waiting_times': 28.942808, 'downloading_chunk_lengths': 16352.491374182035, 'writing_times': 0.369696, 'writing_chunk_lengths': 16357.356739065754, 'downloaded mean chunk size observed': 16352.491374182035, 'start': '2021-04-08 10:10:27.123947', 'finish': '2021-04-08 10:10:57.497616', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc'},
{'name': '( Batch 0 - Item 0)', 'file size': 54977076, 'elapsed time': 33.587124, 'waiting_times': 32.24408699999999, 'downloading_chunk_lengths': 16352.491374182035, 'writing_times': 0.374845, 'writing_chunk_lengths': 16357.356739065754, 'downloaded mean chunk size observed': 16352.491374182035, 'start': '2021-04-08 10:10:27.122873', 'finish': '2021-04-08 10:11:00.709997', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc'},
{'name': '( Batch 0 - Item 2)', 'file size': 54977076, 'elapsed time': 34.534547, 'waiting_times': 33.088978, 'downloading_chunk_lengths': 16362.225, 'writing_times': 0.383355, 'writing_chunk_lengths': 16367.096159571302, 'downloaded mean chunk size observed': 16362.225, 'start': '2021-04-08 10:10:27.123426', 'finish': '2021-04-08 10:11:01.657973', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc'},
{'name': '( Batch 0 - Item 4)', 'file size': 54977076, 'elapsed time': 36.869731, 'waiting_times': 35.504804, 'downloading_chunk_lengths': 16270.220775377331, 'writing_times': 0.376416, 'writing_chunk_lengths': 16275.03730017762, 'downloaded mean chunk size observed': 16270.220775377331, 'start': '2021-04-08 10:10:27.123774', 'finish': '2021-04-08 10:11:03.993505', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc'},
{'name': '( Batch 0 - Item 1)', 'file size': 78675556, 'elapsed time': 46.024854, 'waiting_times': 44.51992, 'downloading_chunk_lengths': 16363.468386023294, 'writing_times': 0.5160230000000001, 'writing_chunk_lengths': 16366.87247763678, 'downloaded mean chunk size observed': 16363.468386023294, 'start': '2021-04-08 10:10:27.123226', 'finish': '2021-04-08 10:11:13.148080', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc'},
{'name': '( Batch 0 - Item 6)', 'file size': 54977076, 'elapsed time': 49.521758, 'waiting_times': 48.107454000000004, 'downloading_chunk_lengths': 16352.491374182035, 'writing_times': 0.400051, 'writing_chunk_lengths': 16357.356739065754, 'downloaded mean chunk size observed': 16352.491374182035, 'start': '2021-04-08 10:10:27.124115', 'finish': '2021-04-08 10:11:16.645873', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc'},
{'name': '( Batch 0 - Item 8)', 'file size': 54977076, 'elapsed time': 37.544696, 'waiting_times': 32.398575, 'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.410326, 'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267, 'start': '2021-04-08 10:10:44.517997', 'finish': '2021-04-08 10:11:22.062693', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc'},
{'name': '( Batch 0 - Item 10)', 'file size': 47212396, 'elapsed time': 32.994671, 'waiting_times': 29.729085, 'downloading_chunk_lengths': 16370.456310679612, 'writing_times': 0.328164, 'writing_chunk_lengths': 16376.134582032604, 'downloaded mean chunk size observed': 16370.456310679612, 'start': '2021-04-08 10:10:57.497749', 'finish': '2021-04-08 10:11:30.492420', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc'},
{'name': '( Batch 0 - Item 15)', 'file size': 54977076, 'elapsed time': 39.273918, 'waiting_times': 35.933268999999996, 'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.403321, 'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267, 'start': '2021-04-08 10:11:16.645985', 'finish': '2021-04-08 10:11:55.919903', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc'},
{'name': '( Batch 0 - Item 16)', 'file size': 47212548, 'elapsed time': 35.554051, 'waiting_times': 31.950908, 'downloading_chunk_lengths': 16370.509015256588, 'writing_times': 0.30224, 'writing_chunk_lengths': 16376.187304890738, 'downloaded mean chunk size observed': 16370.509015256588, 'start': '2021-04-08 10:11:22.062882', 'finish': '2021-04-08 10:11:57.616933', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc'},
{'name': '( Batch 0 - Item 12)', 'file size': 78675556, 'elapsed time': 60.958677, 'waiting_times': 55.640997, 'downloading_chunk_lengths': 16326.116621705749, 'writing_times': 0.53978, 'writing_chunk_lengths': 16329.505188875051, 'downloaded mean chunk size observed': 16326.116621705749, 'start': '2021-04-08 10:11:01.658071', 'finish': '2021-04-08 10:12:02.616748', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc'},
{'name': '( Batch 0 - Item 13)', 'file size': 88114316, 'elapsed time': 58.633478, 'waiting_times': 55.3471, 'downloading_chunk_lengths': 16293.327662721893, 'writing_times': 0.6254040000000001, 'writing_chunk_lengths': 16296.34103939338, 'downloaded mean chunk size observed': 16293.327662721893, 'start': '2021-04-08 10:11:03.993642', 'finish': '2021-04-08 10:12:02.627120', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc'},
{'name': '( Batch 0 - Item 17)', 'file size': 54977076, 'elapsed time': 36.559991, 'waiting_times': 32.938239, 'downloading_chunk_lengths': 16333.058823529413, 'writing_times': 0.381443, 'writing_chunk_lengths': 16337.912630014858, 'downloaded mean chunk size observed': 16333.058823529413, 'start': '2021-04-08 10:11:30.492603', 'finish': '2021-04-08 10:12:07.052594', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc'},
{'name': '( Batch 0 - Item 18)', 'file size': 27452324, 'elapsed time': 25.918278, 'waiting_times': 20.250691999999997, 'downloading_chunk_lengths': 16215.19432959244, 'writing_times': 0.19692199999999999, 'writing_chunk_lengths': 16224.777777777777, 'downloaded mean chunk size observed': 16215.19432959244, 'start': '2021-04-08 10:11:55.920007', 'finish': '2021-04-08 10:12:21.838285', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'name': '( Batch 0 - Item 11)', 'file size': 138079884, 'elapsed time': 83.728781, 'waiting_times': 80.130851, 'downloading_chunk_lengths': 16381.526159686795, 'writing_times': 0.958379, 'writing_chunk_lengths': 16383.46986236355, 'downloaded mean chunk size observed': 16381.526159686795, 'start': '2021-04-08 10:11:00.710115', 'finish': '2021-04-08 10:12:24.438896', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'name': '( Batch 0 - Item 21)', 'file size': 47212016, 'elapsed time': 32.577007, 'waiting_times': 29.783643, 'downloading_chunk_lengths': 16263.181536341715, 'writing_times': 0.327862, 'writing_chunk_lengths': 16268.78566505858, 'downloaded mean chunk size observed': 16263.181536341715, 'start': '2021-04-08 10:12:02.627244', 'finish': '2021-04-08 10:12:35.204251', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc'},
{'name': '( Batch 0 - Item 20)', 'file size': 54977076, 'elapsed time': 36.139258, 'waiting_times': 33.368196, 'downloading_chunk_lengths': 16246.18085106383, 'writing_times': 0.365114, 'writing_chunk_lengths': 16250.983151049364, 'downloaded mean chunk size observed': 16246.18085106383, 'start': '2021-04-08 10:12:02.616872', 'finish': '2021-04-08 10:12:38.756130', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc'},
{'name': '( Batch 0 - Item 14)', 'file size': 138080336, 'elapsed time': 89.458864, 'waiting_times': 85.53916699999999, 'downloading_chunk_lengths': 16381.579784078776, 'writing_times': 0.981414, 'writing_chunk_lengths': 16383.523493118177, 'downloaded mean chunk size observed': 16381.579784078776, 'start': '2021-04-08 10:11:13.148195', 'finish': '2021-04-08 10:12:42.607059', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'name': '( Batch 0 - Item 19)', 'file size': 78675024, 'elapsed time': 55.285483, 'waiting_times': 50.538887, 'downloading_chunk_lengths': 16309.084577114429, 'writing_times': 0.5546070000000001, 'writing_chunk_lengths': 16312.466099937797, 'downloaded mean chunk size observed': 16309.084577114429, 'start': '2021-04-08 10:11:57.617116', 'finish': '2021-04-08 10:12:52.902599', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc'},
{'name': '( Batch 0 - Item 25)', 'file size': 27451904, 'elapsed time': 19.920095, 'waiting_times': 16.509755000000002, 'downloading_chunk_lengths': 16253.347542924808, 'writing_times': 0.200903, 'writing_chunk_lengths': 16262.976303317535, 'downloaded mean chunk size observed': 16253.347542924808, 'start': '2021-04-08 10:12:35.204369', 'finish': '2021-04-08 10:12:55.124464', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'name': '( Batch 0 - Item 23)', 'file size': 54977076, 'elapsed time': 37.856564, 'waiting_times': 34.544903000000005, 'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.357287, 'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267, 'start': '2021-04-08 10:12:21.838405', 'finish': '2021-04-08 10:12:59.694969', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc'},
{'name': '( Batch 0 - Item 22)', 'file size': 88114468, 'elapsed time': 63.082485, 'waiting_times': 59.301315, 'downloading_chunk_lengths': 16320.51639192443, 'writing_times': 0.577226, 'writing_chunk_lengths': 16323.539829566505, 'downloaded mean chunk size observed': 16320.51639192443, 'start': '2021-04-08 10:12:07.052697', 'finish': '2021-04-08 10:13:10.135182', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc'},
{'name': '( Batch 0 - Item 26)', 'file size': 54977076, 'elapsed time': 39.133661, 'waiting_times': 35.501459999999994, 'downloading_chunk_lengths': 16337.912630014858, 'writing_times': 0.37134100000000003, 'writing_chunk_lengths': 16342.769322235434, 'downloaded mean chunk size observed': 16337.912630014858, 'start': '2021-04-08 10:12:38.756243', 'finish': '2021-04-08 10:13:17.889904', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc'},
{'name': '( Batch 0 - Item 28)', 'file size': 78675404, 'elapsed time': 51.951348, 'waiting_times': 48.256786999999996, 'downloading_chunk_lengths': 16373.653277835589, 'writing_times': 0.543337, 'writing_chunk_lengths': 16377.061615320566, 'downloaded mean chunk size observed': 16373.653277835589, 'start': '2021-04-08 10:12:52.902711', 'finish': '2021-04-08 10:13:44.854059', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc'},
{'name': '( Batch 0 - Item 31)', 'file size': 54977076, 'elapsed time': 37.263692, 'waiting_times': 33.731368, 'downloading_chunk_lengths': 16313.672403560831, 'writing_times': 0.369146, 'writing_chunk_lengths': 16318.514692787177, 'downloaded mean chunk size observed': 16313.672403560831, 'start': '2021-04-08 10:13:10.135321', 'finish': '2021-04-08 10:13:47.399013', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc'},
{'name': '( Batch 0 - Item 24)', 'file size': 138079984, 'elapsed time': 86.856249, 'waiting_times': 82.92546899999999, 'downloading_chunk_lengths': 16373.76781690976, 'writing_times': 0.9445180000000001, 'writing_chunk_lengths': 16375.709677419354, 'downloaded mean chunk size observed': 16373.76781690976, 'start': '2021-04-08 10:12:24.439011', 'finish': '2021-04-08 10:13:51.295260', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'name': '( Batch 0 - Item 30)', 'file size': 88113936, 'elapsed time': 59.561244, 'waiting_times': 55.832083, 'downloading_chunk_lengths': 16212.315731370745, 'writing_times': 0.607881, 'writing_chunk_lengths': 16215.2992270887, 'downloaded mean chunk size observed': 16212.315731370745, 'start': '2021-04-08 10:12:59.695075', 'finish': '2021-04-08 10:13:59.256319', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc'},
{'name': '( Batch 0 - Item 35)', 'file size': 27451972, 'elapsed time': 19.938065, 'waiting_times': 17.385661, 'downloading_chunk_lengths': 16359.935637663886, 'writing_times': 0.188881, 'writing_chunk_lengths': 16369.691115086463, 'downloaded mean chunk size observed': 16359.935637663886, 'start': '2021-04-08 10:13:51.295409', 'finish': '2021-04-08 10:14:11.233474', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc'},
{'name': '( Batch 0 - Item 32)', 'file size': 54977076, 'elapsed time': 53.991415, 'waiting_times': 50.405482, 'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.36236, 'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267, 'start': '2021-04-08 10:13:17.890021', 'finish': '2021-04-08 10:14:11.881436', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc'},
{'name': '( Batch 0 - Item 27)', 'file size': 138080132, 'elapsed time': 95.143397, 'waiting_times': 91.23804099999998, 'downloading_chunk_lengths': 16379.612336892053, 'writing_times': 0.90373, 'writing_chunk_lengths': 16381.555581919563, 'downloaded mean chunk size observed': 16379.612336892053, 'start': '2021-04-08 10:12:42.607169', 'finish': '2021-04-08 10:14:17.750566', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc'},
{'name': '( Batch 0 - Item 33)', 'file size': 54977076, 'elapsed time': 36.064128, 'waiting_times': 30.411361, 'downloading_chunk_lengths': 16284.678909952607, 'writing_times': 0.36341999999999997, 'writing_chunk_lengths': 16289.504, 'downloaded mean chunk size observed': 16284.678909952607, 'start': '2021-04-08 10:13:44.854172', 'finish': '2021-04-08 10:14:20.918300', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc'},
{'name': '( Batch 0 - Item 34)', 'file size': 78675404, 'elapsed time': 46.462006, 'waiting_times': 42.217873, 'downloading_chunk_lengths': 16305.783212435234, 'writing_times': 0.519335, 'writing_chunk_lengths': 16309.163349917082, 'downloaded mean chunk size observed': 16305.783212435234, 'start': '2021-04-08 10:13:47.399132', 'finish': '2021-04-08 10:14:33.861138', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc'},
{'name': '( Batch 0 - Item 37)', 'file size': 54977076, 'elapsed time': 26.143093, 'waiting_times': 22.994616999999998, 'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.391887, 'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267, 'start': '2021-04-08 10:14:11.233673', 'finish': '2021-04-08 10:14:37.376766', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc'},
{'name': '( Batch 0 - Item 36)', 'file size': 78675024, 'elapsed time': 39.298007, 'waiting_times': 35.80628, 'downloading_chunk_lengths': 16039.760244648318, 'writing_times': 0.540606, 'writing_chunk_lengths': 16043.030995106035, 'downloaded mean chunk size observed': 16039.760244648318, 'start': '2021-04-08 10:13:59.256426', 'finish': '2021-04-08 10:14:38.554433', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc'},
{'name': '( Batch 0 - Item 9)', 'file size': 795795032, 'elapsed time': 292.026078, 'waiting_times': 283.76109199999996, 'downloading_chunk_lengths': 16383.485310769358, 'writing_times': 5.422355999999999, 'writing_chunk_lengths': 16383.822613851602, 'downloaded mean chunk size observed': 16383.485310769358, 'start': '2021-04-08 10:10:49.857677', 'finish': '2021-04-08 10:15:41.883755', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc'},
{'name': '( Batch 0 - Item 29)', 'file size': 795795708, 'elapsed time': 191.363348, 'waiting_times': 182.009168, 'downloading_chunk_lengths': 16359.249830403947, 'writing_times': 5.966702000000001, 'writing_chunk_lengths': 16359.586136008553, 'downloaded mean chunk size observed': 16359.249830403947, 'start': '2021-04-08 10:12:55.124650', 'finish': '2021-04-08 10:16:06.487998', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc'},


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
