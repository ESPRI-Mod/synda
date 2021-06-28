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

{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file size': 47212396, 'elapsed time': 37.425474, 'waiting_times': 37.400196, 'writing_times': 0.012361, 'start': '2021-04-20 15:48:38.964371', 'finish': '2021-04-20 15:49:16.389845', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file size': 47212016, 'elapsed time': 43.820659, 'waiting_times': 43.801403, 'writing_times': 0.011467, 'start': '2021-04-20 15:48:38.877665', 'finish': '2021-04-20 15:49:22.698324', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'file size': 78675404, 'elapsed time': 46.133939, 'waiting_times': 46.103838, 'writing_times': 0.018642, 'start': '2021-04-20 15:48:39.597451', 'finish': '2021-04-20 15:49:25.731390', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'file size': 78675024, 'elapsed time': 49.053927, 'waiting_times': 49.00409, 'writing_times': 0.022866, 'start': '2021-04-20 15:48:39.052454', 'finish': '2021-04-20 15:49:28.106381', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'file size': 78675024, 'elapsed time': 51.128667, 'waiting_times': 51.085457, 'writing_times': 0.018877, 'start': '2021-04-20 15:48:39.181942', 'finish': '2021-04-20 15:49:30.310609', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'file size': 78675404, 'elapsed time': 52.172293, 'waiting_times': 52.128856, 'writing_times': 0.022557, 'start': '2021-04-20 15:48:39.451384', 'finish': '2021-04-20 15:49:31.623677', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file size': 88114316, 'elapsed time': 53.150956, 'waiting_times': 51.901146, 'writing_times': 1.222367, 'start': '2021-04-20 15:48:39.706287', 'finish': '2021-04-20 15:49:32.857243', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/psl/1/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file size': 27451904, 'elapsed time': 17.134606, 'waiting_times': 17.125122, 'writing_times': 0.005965, 'start': '2021-04-20 15:49:19.020958', 'finish': '2021-04-20 15:49:36.155564', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/tasmin/1/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file size': 27452120, 'elapsed time': 12.876657, 'waiting_times': 12.860924, 'writing_times': 0.009292, 'start': '2021-04-20 15:49:25.191336', 'finish': '2021-04-20 15:49:38.067993', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file size': 88113936, 'elapsed time': 61.379029, 'waiting_times': 61.331374, 'writing_times': 0.021171, 'start': '2021-04-20 15:48:39.315370', 'finish': '2021-04-20 15:49:40.694399', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file size': 47212548, 'elapsed time': 24.415616, 'waiting_times': 24.398157, 'writing_times': 0.010291, 'start': '2021-04-20 15:49:31.554675', 'finish': '2021-04-20 15:49:55.970291', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/mrsos/1/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file size': 27452324, 'elapsed time': 22.543345, 'waiting_times': 22.532656, 'writing_times': 0.007044, 'start': '2021-04-20 15:49:39.375627', 'finish': '2021-04-20 15:50:01.918972', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'file size': 78675556, 'elapsed time': 35.596956, 'waiting_times': 35.55416, 'writing_times': 0.01872, 'start': '2021-04-20 15:49:33.930265', 'finish': '2021-04-20 15:50:09.527221', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'file size': 78675556, 'elapsed time': 54.4216, 'waiting_times': 54.379007, 'writing_times': 0.018594, 'start': '2021-04-20 15:49:32.835266', 'finish': '2021-04-20 15:50:27.256866', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/sic/1/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file size': 27451972, 'elapsed time': 18.066558, 'waiting_times': 18.052499, 'writing_times': 0.009159, 'start': '2021-04-20 15:50:11.705452', 'finish': '2021-04-20 15:50:29.772010', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/tasmin/1/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file size': 138080132, 'elapsed time': 68.05256, 'waiting_times': 68.001531, 'writing_times': 0.033178, 'start': '2021-04-20 15:49:30.217897', 'finish': '2021-04-20 15:50:38.270457', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file size': 88114468, 'elapsed time': 68.32684, 'waiting_times': 68.278733, 'writing_times': 0.021105, 'start': '2021-04-20 15:49:38.021301', 'finish': '2021-04-20 15:50:46.348141', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/mrsos/1/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file size': 138080336, 'elapsed time': 82.695329, 'waiting_times': 82.660126, 'writing_times': 0.033441, 'start': '2021-04-20 15:49:42.874738', 'finish': '2021-04-20 15:51:05.570067', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/psl/1/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file size': 138079884, 'elapsed time': 102.71943, 'waiting_times': 102.653576, 'writing_times': 0.03272, 'start': '2021-04-20 15:49:28.031724', 'finish': '2021-04-20 15:51:10.751154', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc', 'file size': 54977076, 'elapsed time': 41.88043, 'waiting_times': 41.859401, 'writing_times': 0.01519, 'start': '2021-04-20 15:50:30.996559', 'finish': '2021-04-20 15:51:12.876989', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc', 'file size': 54977076, 'elapsed time': 33.583058, 'waiting_times': 33.562582, 'writing_times': 0.015042, 'start': '2021-04-20 15:50:40.767153', 'finish': '2021-04-20 15:51:14.350211', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc', 'file size': 54977076, 'elapsed time': 41.794485, 'waiting_times': 41.780319, 'writing_times': 0.013203, 'start': '2021-04-20 15:50:48.873408', 'finish': '2021-04-20 15:51:30.667893', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc', 'file size': 54977076, 'elapsed time': 37.618568, 'waiting_times': 37.604456, 'writing_times': 0.01311, 'start': '2021-04-20 15:51:08.042327', 'finish': '2021-04-20 15:51:45.660895', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc', 'file size': 54977076, 'elapsed time': 35.779402, 'waiting_times': 35.765084, 'writing_times': 0.013166, 'start': '2021-04-20 15:51:12.830004', 'finish': '2021-04-20 15:51:48.609406', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/sic/1/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file size': 138079984, 'elapsed time': 81.297377, 'waiting_times': 81.256091, 'writing_times': 0.037441, 'start': '2021-04-20 15:50:29.720710', 'finish': '2021-04-20 15:51:51.018087', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc', 'file size': 54977076, 'elapsed time': 36.704948, 'waiting_times': 35.108668, 'writing_times': 1.590768, 'start': '2021-04-20 15:51:15.895997', 'finish': '2021-04-20 15:51:52.600945', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc', 'file size': 54977076, 'elapsed time': 38.566216, 'waiting_times': 38.544218, 'writing_times': 0.016044, 'start': '2021-04-20 15:51:14.312499', 'finish': '2021-04-20 15:51:52.878715', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc', 'file size': 54977076, 'elapsed time': 36.718845, 'waiting_times': 36.70448, 'writing_times': 0.013444, 'start': '2021-04-20 15:51:33.307153', 'finish': '2021-04-20 15:52:10.025998', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc', 'file size': 54977076, 'elapsed time': 31.987777, 'waiting_times': 31.973768, 'writing_times': 0.013022, 'start': '2021-04-20 15:51:48.302622', 'finish': '2021-04-20 15:52:20.290399', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc', 'file size': 54977076, 'elapsed time': 33.581066, 'waiting_times': 33.565555, 'writing_times': 0.01447, 'start': '2021-04-20 15:51:50.927061', 'finish': '2021-04-20 15:52:24.508127', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc', 'file size': 54977076, 'elapsed time': 37.652656, 'waiting_times': 37.6375, 'writing_times': 0.013802, 'start': '2021-04-20 15:51:52.832385', 'finish': '2021-04-20 15:52:30.485041', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc', 'file size': 54977076, 'elapsed time': 38.059361, 'waiting_times': 38.043824, 'writing_times': 0.013274, 'start': '2021-04-20 15:51:52.594767', 'finish': '2021-04-20 15:52:30.654128', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc', 'file size': 54977076, 'elapsed time': 41.989156, 'waiting_times': 41.974987, 'writing_times': 0.013257, 'start': '2021-04-20 15:51:54.599776', 'finish': '2021-04-20 15:52:36.588932', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc', 'file size': 34680756, 'elapsed time': 18.135878, 'waiting_times': 18.12672, 'writing_times': 0.008273, 'start': '2021-04-20 15:52:27.149920', 'finish': '2021-04-20 15:52:45.285798', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc', 'file size': 54977076, 'elapsed time': 33.79165, 'waiting_times': 33.777493, 'writing_times': 0.013177, 'start': '2021-04-20 15:52:12.665468', 'finish': '2021-04-20 15:52:46.457118', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc', 'file size': 54977076, 'elapsed time': 26.126702, 'waiting_times': 26.11166, 'writing_times': 0.01408, 'start': '2021-04-20 15:52:22.933528', 'finish': '2021-04-20 15:52:49.060230', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file size': 795795708, 'elapsed time': 244.213551, 'waiting_times': 244.006003, 'writing_times': 0.20305, 'start': '2021-04-20 15:49:58.403302', 'finish': '2021-04-20 15:54:02.616853', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'small, aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file size': 795795032, 'elapsed time': 255.075922, 'waiting_times': 254.879859, 'writing_times': 0.194215, 'start': '2021-04-20 15:50:04.156096', 'finish': '2021-04-20 15:54:19.232018', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},

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
