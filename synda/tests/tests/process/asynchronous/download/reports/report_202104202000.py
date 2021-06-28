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

{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file size': 47212016, 'elapsed time': 29.660247, 'waiting_times': 29.648231, 'writing_times': 0.011142, 'start': '2021-04-20 19:48:24.579245', 'finish': '2021-04-20 19:48:54.239492', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file size': 47212396, 'elapsed time': 37.20022, 'waiting_times': 37.18804, 'writing_times': 0.011348, 'start': '2021-04-20 19:48:24.697691', 'finish': '2021-04-20 19:49:01.897911', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'file size': 78675024, 'elapsed time': 46.37908, 'waiting_times': 46.359376, 'writing_times': 0.018715, 'start': '2021-04-20 19:48:24.899800', 'finish': '2021-04-20 19:49:11.278880', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'file size': 78675404, 'elapsed time': 48.740484, 'waiting_times': 48.717013, 'writing_times': 0.019918, 'start': '2021-04-20 19:48:25.110207', 'finish': '2021-04-20 19:49:13.850691', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'file size': 78675024, 'elapsed time': 50.899653, 'waiting_times': 50.87216, 'writing_times': 0.022233, 'start': '2021-04-20 19:48:24.803025', 'finish': '2021-04-20 19:49:15.702678', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/psl/1/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file size': 27451904, 'elapsed time': 20.938832, 'waiting_times': 20.931923, 'writing_times': 0.006098, 'start': '2021-04-20 19:48:56.866102', 'finish': '2021-04-20 19:49:17.804934', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'file size': 78675404, 'elapsed time': 56.798539, 'waiting_times': 56.777245, 'writing_times': 0.020267, 'start': '2021-04-20 19:48:25.219438', 'finish': '2021-04-20 19:49:22.017977', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/tasmin/1/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file size': 27452120, 'elapsed time': 19.412727, 'waiting_times': 17.46429, 'writing_times': 1.945264, 'start': '2021-04-20 19:49:04.552870', 'finish': '2021-04-20 19:49:23.965597', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file size': 88114316, 'elapsed time': 58.900208, 'waiting_times': 58.862572, 'writing_times': 0.033883, 'start': '2021-04-20 19:48:25.320516', 'finish': '2021-04-20 19:49:24.220724', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file size': 88113936, 'elapsed time': 60.954244, 'waiting_times': 59.185065, 'writing_times': 1.762916, 'start': '2021-04-20 19:48:25.024380', 'finish': '2021-04-20 19:49:25.978624', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/mrsos/1/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file size': 27452324, 'elapsed time': 17.015721, 'waiting_times': 17.008199, 'writing_times': 0.006907, 'start': '2021-04-20 19:49:25.973151', 'finish': '2021-04-20 19:49:42.988872', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'file size': 47212548, 'elapsed time': 31.423057, 'waiting_times': 31.411278, 'writing_times': 0.010906, 'start': '2021-04-20 19:49:17.512414', 'finish': '2021-04-20 19:49:48.935471', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'file size': 78675556, 'elapsed time': 46.559571, 'waiting_times': 46.540029, 'writing_times': 0.018677, 'start': '2021-04-20 19:49:19.828492', 'finish': '2021-04-20 19:50:06.388063', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'file size': 88114468, 'elapsed time': 55.305216, 'waiting_times': 55.283201, 'writing_times': 0.020975, 'start': '2021-04-20 19:49:24.132589', 'finish': '2021-04-20 19:50:19.437805', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'file size': 78675556, 'elapsed time': 68.503757, 'waiting_times': 68.483939, 'writing_times': 0.018753, 'start': '2021-04-20 19:49:23.959650', 'finish': '2021-04-20 19:50:32.463407', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/sic/1/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'file size': 27451972, 'elapsed time': 26.160156, 'waiting_times': 26.149562, 'writing_times': 0.007189, 'start': '2021-04-20 19:50:08.924690', 'finish': '2021-04-20 19:50:35.084846', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/psl/1/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file size': 138079884, 'elapsed time': 82.916197, 'waiting_times': 82.878252, 'writing_times': 0.03447, 'start': '2021-04-20 19:49:13.781976', 'finish': '2021-04-20 19:50:36.698173', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/tasmin/1/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file size': 138080132, 'elapsed time': 82.99366, 'waiting_times': 82.954037, 'writing_times': 0.035466, 'start': '2021-04-20 19:49:15.655919', 'finish': '2021-04-20 19:50:38.649579', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/mrsos/1/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file size': 138080336, 'elapsed time': 98.151808, 'waiting_times': 98.117421, 'writing_times': 0.033106, 'start': '2021-04-20 19:49:26.272734', 'finish': '2021-04-20 19:51:04.424542', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc', 'file size': 54977076, 'elapsed time': 34.361454, 'waiting_times': 34.347477, 'writing_times': 0.012974, 'start': '2021-04-20 19:50:35.029961', 'finish': '2021-04-20 19:51:09.391415', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc', 'file size': 54977076, 'elapsed time': 37.465874, 'waiting_times': 37.452083, 'writing_times': 0.012926, 'start': '2021-04-20 19:50:38.580693', 'finish': '2021-04-20 19:51:16.046567', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc', 'file size': 54977076, 'elapsed time': 37.97086, 'waiting_times': 37.95019, 'writing_times': 0.014983, 'start': '2021-04-20 19:50:40.466551', 'finish': '2021-04-20 19:51:18.437411', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc', 'file size': 54977076, 'elapsed time': 43.655082, 'waiting_times': 43.637756, 'writing_times': 0.014052, 'start': '2021-04-20 19:50:36.616512', 'finish': '2021-04-20 19:51:20.271594', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc', 'file size': 54977076, 'elapsed time': 34.982274, 'waiting_times': 34.968848, 'writing_times': 0.012851, 'start': '2021-04-20 19:51:07.055238', 'finish': '2021-04-20 19:51:42.037512', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc', 'file size': 54977076, 'elapsed time': 35.080579, 'waiting_times': 35.066546, 'writing_times': 0.013217, 'start': '2021-04-20 19:51:11.967286', 'finish': '2021-04-20 19:51:47.047865', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/sic/1/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'file size': 138079984, 'elapsed time': 87.340686, 'waiting_times': 87.300927, 'writing_times': 0.035975, 'start': '2021-04-20 19:50:22.059283', 'finish': '2021-04-20 19:51:49.399969', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc', 'file size': 54977076, 'elapsed time': 33.649032, 'waiting_times': 33.635016, 'writing_times': 0.012956, 'start': '2021-04-20 19:51:18.387771', 'finish': '2021-04-20 19:51:52.036803', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc', 'file size': 54977076, 'elapsed time': 38.22305, 'waiting_times': 38.209063, 'writing_times': 0.013164, 'start': '2021-04-20 19:51:20.219426', 'finish': '2021-04-20 19:51:58.442476', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc', 'file size': 54977076, 'elapsed time': 38.359028, 'waiting_times': 38.337823, 'writing_times': 0.015279, 'start': '2021-04-20 19:51:22.463250', 'finish': '2021-04-20 19:52:00.822278', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc', 'file size': 54977076, 'elapsed time': 34.759743, 'waiting_times': 34.746234, 'writing_times': 0.012694, 'start': '2021-04-20 19:51:44.623265', 'finish': '2021-04-20 19:52:19.383008', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc', 'file size': 54977076, 'elapsed time': 33.094525, 'waiting_times': 33.080821, 'writing_times': 0.012733, 'start': '2021-04-20 19:51:49.318011', 'finish': '2021-04-20 19:52:22.412536', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc', 'file size': 54977076, 'elapsed time': 37.386876, 'waiting_times': 37.373145, 'writing_times': 0.012978, 'start': '2021-04-20 19:51:51.416992', 'finish': '2021-04-20 19:52:28.803868', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc', 'file size': 54977076, 'elapsed time': 35.472331, 'waiting_times': 35.458423, 'writing_times': 0.013019, 'start': '2021-04-20 19:51:54.287157', 'finish': '2021-04-20 19:52:29.759488', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc', 'file size': 54977076, 'elapsed time': 33.287739, 'waiting_times': 33.273626, 'writing_times': 0.013335, 'start': '2021-04-20 19:52:02.391741', 'finish': '2021-04-20 19:52:35.679480', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc', 'file size': 54977076, 'elapsed time': 35.224427, 'waiting_times': 35.210249, 'writing_times': 0.013206, 'start': '2021-04-20 19:52:00.779409', 'finish': '2021-04-20 19:52:36.003836', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc', 'file size': 34680756, 'elapsed time': 16.939179, 'waiting_times': 16.930193, 'writing_times': 0.008275, 'start': '2021-04-20 19:52:22.022375', 'finish': '2021-04-20 19:52:38.961554', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file size': 795795708, 'elapsed time': 256.581547, 'waiting_times': 256.358981, 'writing_times': 0.219449, 'start': '2021-04-20 19:49:45.599673', 'finish': '2021-04-20 19:54:02.181220', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},
{'name': 'aims3.llnl.gov , http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'file size': 795795032, 'elapsed time': 253.831217, 'waiting_times': 253.586434, 'writing_times': 0.244232, 'start': '2021-04-20 19:49:51.553426', 'finish': '2021-04-20 19:54:05.384643', 'strategy': 'asyncio aiohttp', 'sdget_status': 0, 'sdget_error_msg': None, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'process_name': 'small file task'},

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
