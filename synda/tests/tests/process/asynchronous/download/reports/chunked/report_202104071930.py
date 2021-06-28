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
    "status_code",
    "local_path",
    "error",
]

figs = make_subplots(
    rows=3,
    cols=2,
    shared_xaxes=False,
    vertical_spacing=0.05,
    subplot_titles=(
        '{} Downloads ({} Go)'.format(
            len(files),
            sizes * coeff_bytes_2_go,
        ),
        'sequential',
        'synda version 3.2',
        'asyncio - aiohttp',
    ),
    specs=[

        [{"rowspan": 3}, {}],
        [None, {}],
        [None, {}],
    ],
)
figs.update_xaxes(title_text="Go", row=1, col=1)
figs.update_yaxes(title_text="Elapsed time (in seconds)", row=1, col=1)

# # RUN current synda version 3.2

data = [

    {'name': '( Batch 0 - Item 7)', 'file size': 27452120, 'elapsed time': 14.482775, 'waiting_times': 12.41061,
     'downloading_chunk_lengths': 16167.326266195525, 'writing_times': 0.23220200000000002,
     'writing_chunk_lengths': 16176.853270477313, 'downloaded mean chunk size observed': 16167.326266195525,
     'start': '2021-04-07 16:12:34.181200', 'finish': '2021-04-07 16:12:34.181443', 'strategy': 'asyncio aiohttp',
     'status_code': 0,
     'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc',
     'error': ''},
    {'name': '( Batch 0 - Item 3)', 'file size': 34680756, 'elapsed time': 17.572938, 'waiting_times': 15.173625,
     'downloading_chunk_lengths': 16343.428840716306, 'writing_times': 0.305191,
     'writing_chunk_lengths': 16351.134370579915, 'downloaded mean chunk size observed': 16343.428840716306,
     'start': '2021-04-07 16:12:37.270535', 'finish': '2021-04-07 16:12:37.270758', 'strategy': 'asyncio aiohttp',
     'status_code': 0,
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc',
     'error': ''},
    {'name': '( Batch 0 - Item 2)', 'file size': 54977076, 'elapsed time': 25.733103, 'waiting_times': 22.448647,
     'downloading_chunk_lengths': 16362.225, 'writing_times': 0.455523, 'writing_chunk_lengths': 16367.096159571302,
     'downloaded mean chunk size observed': 16362.225, 'start': '2021-04-07 16:12:45.430597',
     'finish': '2021-04-07 16:12:45.430698', 'strategy': 'asyncio aiohttp', 'status_code': 0,
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc',
     'error': ''},
    # {'name': '( Batch 0 - Item 5)', 'file size': 54977076, 'elapsed time': 26.033518,
    #  'waiting_times': 22.755588000000003, 'downloading_chunk_lengths': 16357.356739065754, 'writing_times': 0.452496,
    #  'writing_chunk_lengths': 16362.225, 'downloaded mean chunk size observed': 16357.356739065754,
    #  'start': '2021-04-07 16:12:45.731664', 'finish': '2021-04-07 16:12:45.731759', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 6)', 'file size': 54977076, 'elapsed time': 26.33185, 'waiting_times': 23.057369,
    #  'downloading_chunk_lengths': 16362.225, 'writing_times': 0.446608, 'writing_chunk_lengths': 16367.096159571302,
    #  'downloaded mean chunk size observed': 16362.225, 'start': '2021-04-07 16:12:46.030164',
    #  'finish': '2021-04-07 16:12:46.030303', 'strategy': 'asyncio aiohttp', 'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 8)', 'file size': 54977076, 'elapsed time': 27.23817, 'waiting_times': 22.411502,
    #  'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.484661,
    #  'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267,
    #  'start': '2021-04-07 16:13:01.420278', 'finish': '2021-04-07 16:13:01.420479', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 1)', 'file size': 78675556, 'elapsed time': 43.341593,
    #  'waiting_times': 38.863316999999995, 'downloading_chunk_lengths': 16363.468386023294, 'writing_times': 0.639116,
    #  'writing_chunk_lengths': 16366.87247763678, 'downloaded mean chunk size observed': 16363.468386023294,
    #  'start': '2021-04-07 16:13:03.038575', 'finish': '2021-04-07 16:13:03.038745', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 10)', 'file size': 47212396, 'elapsed time': 23.734101, 'waiting_times': 19.669936,
    #  'downloading_chunk_lengths': 16302.622928176796, 'writing_times': 0.373077,
    #  'writing_chunk_lengths': 16308.254231433506, 'downloaded mean chunk size observed': 16302.622928176796,
    #  'start': '2021-04-07 16:13:09.165645', 'finish': '2021-04-07 16:13:09.165766', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 12)', 'file size': 78675556, 'elapsed time': 40.999731,
    #  'waiting_times': 34.511472999999995, 'downloading_chunk_lengths': 16329.505188875051, 'writing_times': 0.616518,
    #  'writing_chunk_lengths': 16332.8951629645, 'downloaded mean chunk size observed': 16329.505188875051,
    #  'start': '2021-04-07 16:13:27.030895', 'finish': '2021-04-07 16:13:27.031037', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 15)', 'file size': 54977076, 'elapsed time': 29.69844, 'waiting_times': 24.77328,
    #  'downloading_chunk_lengths': 16270.220775377331, 'writing_times': 0.436472,
    #  'writing_chunk_lengths': 16275.03730017762, 'downloaded mean chunk size observed': 16270.220775377331,
    #  'start': '2021-04-07 16:13:38.864983', 'finish': '2021-04-07 16:13:38.865169', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 13)', 'file size': 88114316, 'elapsed time': 44.758084,
    #  'waiting_times': 38.705814000000004, 'downloading_chunk_lengths': 16320.488238562697, 'writing_times': 0.66581,
    #  'writing_chunk_lengths': 16323.511670989255, 'downloaded mean chunk size observed': 16320.488238562697,
    #  'start': '2021-04-07 16:13:46.179445', 'finish': '2021-04-07 16:13:46.179574', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 11)', 'file size': 138079884, 'elapsed time': 70.187194,
    #  'waiting_times': 60.74850599999999, 'downloading_chunk_lengths': 16235.142151675485,
    #  'writing_times': 1.1044500000000002, 'writing_chunk_lengths': 16237.051269990592,
    #  'downloaded mean chunk size observed': 16235.142151675485, 'start': '2021-04-07 16:13:55.919847',
    #  'finish': '2021-04-07 16:13:55.919965', 'strategy': 'asyncio aiohttp', 'status_code': 0,
    #  'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 16)', 'file size': 47212548, 'elapsed time': 29.125515,
    #  'waiting_times': 22.339762999999998, 'downloading_chunk_lengths': 16308.306735751295,
    #  'writing_times': 0.35249600000000003, 'writing_chunk_lengths': 16313.94194885971,
    #  'downloaded mean chunk size observed': 16308.306735751295, 'start': '2021-04-07 16:13:56.157693',
    #  'finish': '2021-04-07 16:13:56.157896', 'strategy': 'asyncio aiohttp', 'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 18)', 'file size': 27452324, 'elapsed time': 14.503392,
    #  'waiting_times': 10.939351000000002, 'downloading_chunk_lengths': 16330.948245092208, 'writing_times': 0.191739,
    #  'writing_chunk_lengths': 16340.669047619047, 'downloaded mean chunk size observed': 16330.948245092208,
    #  'start': '2021-04-07 16:14:00.684284', 'finish': '2021-04-07 16:14:00.684411', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 17)', 'file size': 54977076, 'elapsed time': 28.175753, 'waiting_times': 23.308389,
    #  'downloading_chunk_lengths': 16222.211861906168, 'writing_times': 0.43904, 'writing_chunk_lengths': 16227.0,
    #  'downloaded mean chunk size observed': 16222.211861906168, 'start': '2021-04-07 16:14:07.041839',
    #  'finish': '2021-04-07 16:14:07.041989', 'strategy': 'asyncio aiohttp', 'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 14)', 'file size': 138080336, 'elapsed time': 66.057268,
    #  'waiting_times': 57.79632499999999, 'downloading_chunk_lengths': 16369.927208061648,
    #  'writing_times': 1.0376139999999998, 'writing_chunk_lengths': 16371.8681527152,
    #  'downloaded mean chunk size observed': 16369.927208061648, 'start': '2021-04-07 16:14:09.097859',
    #  'finish': '2021-04-07 16:14:09.097995', 'strategy': 'asyncio aiohttp', 'status_code': 0,
    #  'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 21)', 'file size': 47212016, 'elapsed time': 25.386819, 'waiting_times': 21.063736,
    #  'downloading_chunk_lengths': 16336.337716262975, 'writing_times': 0.368019,
    #  'writing_chunk_lengths': 16341.992384908273, 'downloaded mean chunk size observed': 16336.337716262975,
    #  'start': '2021-04-07 16:14:26.071723', 'finish': '2021-04-07 16:14:26.071835', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 20)', 'file size': 54977076, 'elapsed time': 30.518844, 'waiting_times': 23.997687,
    #  'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.4226,
    #  'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267,
    #  'start': '2021-04-07 16:14:26.677728', 'finish': '2021-04-07 16:14:26.677857', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 19)', 'file size': 78675024, 'elapsed time': 37.912639, 'waiting_times': 32.290392,
    #  'downloading_chunk_lengths': 16356.553846153845, 'writing_times': 0.588597,
    #  'writing_chunk_lengths': 16359.955084217094, 'downloaded mean chunk size observed': 16356.553846153845,
    #  'start': '2021-04-07 16:14:33.834646', 'finish': '2021-04-07 16:14:33.834773', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 23)', 'file size': 54977076, 'elapsed time': 26.580983,
    #  'waiting_times': 21.950802000000003, 'downloading_chunk_lengths': 16284.678909952607, 'writing_times': 0.415231,
    #  'writing_chunk_lengths': 16289.504, 'downloaded mean chunk size observed': 16284.678909952607,
    #  'start': '2021-04-07 16:14:35.680974', 'finish': '2021-04-07 16:14:35.681151', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 22)', 'file size': 88114468, 'elapsed time': 40.019592,
    #  'waiting_times': 33.805966000000005, 'downloading_chunk_lengths': 16375.11020256458, 'writing_times': 0.681475,
    #  'writing_chunk_lengths': 16378.153903345725, 'downloaded mean chunk size observed': 16375.11020256458,
    #  'start': '2021-04-07 16:14:47.062442', 'finish': '2021-04-07 16:14:47.062600', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 26)', 'file size': 54977076, 'elapsed time': 23.502095, 'waiting_times': 19.263563,
    #  'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.40448,
    #  'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267,
    #  'start': '2021-04-07 16:14:57.338091', 'finish': '2021-04-07 16:14:57.338199', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 28)', 'file size': 78675404, 'elapsed time': 34.593275,
    #  'waiting_times': 29.196816999999996, 'downloading_chunk_lengths': 16370.246358718268, 'writing_times': 0.594093,
    #  'writing_chunk_lengths': 16373.653277835589, 'downloaded mean chunk size observed': 16370.246358718268,
    #  'start': '2021-04-07 16:15:21.657165', 'finish': '2021-04-07 16:15:21.657314', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 24)', 'file size': 138079984, 'elapsed time': 59.714179, 'waiting_times': 49.896574,
    #  'downloading_chunk_lengths': 16348.565474780962, 'writing_times': 1.042343,
    #  'writing_chunk_lengths': 16350.501361752516, 'downloaded mean chunk size observed': 16348.565474780962,
    #  'start': '2021-04-07 16:15:25.786807', 'finish': '2021-04-07 16:15:25.786907', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 27)', 'file size': 138080132, 'elapsed time': 56.769706, 'waiting_times': 48.814622,
    #  'downloading_chunk_lengths': 16379.612336892053, 'writing_times': 1.027411,
    #  'writing_chunk_lengths': 16381.555581919563, 'downloaded mean chunk size observed': 16379.612336892053,
    #  'start': '2021-04-07 16:15:32.451685', 'finish': '2021-04-07 16:15:32.451830', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 31)', 'file size': 54977076, 'elapsed time': 24.789811, 'waiting_times': 20.686036,
    #  'downloading_chunk_lengths': 16284.678909952607, 'writing_times': 0.401834, 'writing_chunk_lengths': 16289.504,
    #  'downloaded mean chunk size observed': 16284.678909952607, 'start': '2021-04-07 16:15:50.578650',
    #  'finish': '2021-04-07 16:15:50.578881', 'strategy': 'asyncio aiohttp', 'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 32)', 'file size': 54977076, 'elapsed time': 24.131426, 'waiting_times': 19.857544,
    #  'downloading_chunk_lengths': 16260.596273291925, 'writing_times': 0.410896,
    #  'writing_chunk_lengths': 16265.407100591716, 'downloaded mean chunk size observed': 16260.596273291925,
    #  'start': '2021-04-07 16:15:56.585239', 'finish': '2021-04-07 16:15:56.585396', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 30)', 'file size': 88113936, 'elapsed time': 38.930994, 'waiting_times': 31.328128,
    #  'downloading_chunk_lengths': 16314.37437511572, 'writing_times': 0.650115,
    #  'writing_chunk_lengths': 16317.395555555555, 'downloaded mean chunk size observed': 16314.37437511572,
    #  'start': '2021-04-07 16:16:00.589599', 'finish': '2021-04-07 16:16:00.589736', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 35)', 'file size': 27451972, 'elapsed time': 13.41979, 'waiting_times': 10.151075,
    #  'downloading_chunk_lengths': 16359.935637663886, 'writing_times': 0.196615,
    #  'writing_chunk_lengths': 16369.691115086463, 'downloaded mean chunk size observed': 16359.935637663886,
    #  'start': '2021-04-07 16:16:14.010928', 'finish': '2021-04-07 16:16:14.011038', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 33)', 'file size': 54977076, 'elapsed time': 26.830872, 'waiting_times': 20.701585,
    #  'downloading_chunk_lengths': 16318.514692787177, 'writing_times': 0.412029,
    #  'writing_chunk_lengths': 16323.359857482184, 'downloaded mean chunk size observed': 16318.514692787177,
    #  'start': '2021-04-07 16:16:17.410583', 'finish': '2021-04-07 16:16:17.410906', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 34)', 'file size': 78675404, 'elapsed time': 32.937345, 'waiting_times': 27.49104,
    #  'downloading_chunk_lengths': 16363.436772046589, 'writing_times': 0.614391,
    #  'writing_chunk_lengths': 16366.84085708342, 'downloaded mean chunk size observed': 16363.436772046589,
    #  'start': '2021-04-07 16:16:29.523601', 'finish': '2021-04-07 16:16:29.523835', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 37)', 'file size': 54977076, 'elapsed time': 22.149596, 'waiting_times': 17.870914,
    #  'downloading_chunk_lengths': 16207.864386792453, 'writing_times': 0.43131200000000003,
    #  'writing_chunk_lengths': 16212.644057800058, 'downloaded mean chunk size observed': 16207.864386792453,
    #  'start': '2021-04-07 16:16:39.561490', 'finish': '2021-04-07 16:16:39.561583', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 36)', 'file size': 78675024, 'elapsed time': 30.138778, 'waiting_times': 24.758598,
    #  'downloading_chunk_lengths': 16373.574193548387, 'writing_times': 0.606517,
    #  'writing_chunk_lengths': 16376.982514571191, 'downloaded mean chunk size observed': 16373.574193548387,
    #  'start': '2021-04-07 16:16:44.150284', 'finish': '2021-04-07 16:16:44.150427', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 9)', 'file size': 795795032, 'elapsed time': 281.549931, 'waiting_times': 244.128514,
    #  'downloading_chunk_lengths': 16374.383374485597, 'writing_times': 6.024555,
    #  'writing_chunk_lengths': 16374.72030288689, 'downloaded mean chunk size observed': 16374.383374485597,
    #  'start': '2021-04-07 16:17:18.821285', 'finish': '2021-04-07 16:17:18.821517', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc',
    #  'error': ''},
    # {'name': '( Batch 0 - Item 29)', 'file size': 795795708, 'elapsed time': 168.204501, 'waiting_times': 131.158258,
    #  'downloading_chunk_lengths': 16353.870820574999, 'writing_times': 5.931449,
    #  'writing_chunk_lengths': 16354.206905055487, 'downloaded mean chunk size observed': 16353.870820574999,
    #  'start': '2021-04-07 16:17:45.543554', 'finish': '2021-04-07 16:17:45.543703', 'strategy': 'asyncio aiohttp',
    #  'status_code': 0,
    #  'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc',
    #  'error': ''},

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

# # RUN sequential

data = [

    {'name': '( Batch 0 - Item 7)', 'file size': 27452120, 'elapsed time': 8.144824, 'waiting_times': 5.89828,
     'downloading_chunk_lengths': 16330.826888756692, 'writing_times': 0.17867,
     'writing_chunk_lengths': 16340.547619047618, 'downloaded mean chunk size observed': 16330.826888756692,
     'start': '2021-04-07 18:47:19.892113', 'finish': '2021-04-07 18:47:28.036937', 'strategy': 'asyncio aiohttp',
     'status_code': 0,
     'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc',
     'error': ''},
    {'name': '( Batch 0 - Item 4)', 'file size': 54977076, 'elapsed time': 18.716171,
     'waiting_times': 15.245208000000002, 'downloading_chunk_lengths': 16357.356739065754,
     'writing_times': 0.36255899999999996, 'writing_chunk_lengths': 16362.225,
     'downloaded mean chunk size observed': 16357.356739065754, 'start': '2021-04-07 18:47:19.891583',
     'finish': '2021-04-07 18:47:38.607754', 'strategy': 'asyncio aiohttp', 'status_code': 0,
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc',
     'error': ''},
    {'name': '( Batch 0 - Item 5)', 'file size': 54977076, 'elapsed time': 18.817544,
     'waiting_times': 15.245101000000002, 'downloading_chunk_lengths': 16357.356739065754, 'writing_times': 0.370234,
     'writing_chunk_lengths': 16362.225, 'downloaded mean chunk size observed': 16357.356739065754,
     'start': '2021-04-07 18:47:19.891761', 'finish': '2021-04-07 18:47:38.709305', 'strategy': 'asyncio aiohttp',
     'status_code': 0,
     'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc',
     'error': ''},

]


sequential = pd.DataFrame(data, columns=columns)

sequential["start"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in sequential["start"]]
sequential["finish"] = [datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") for str_date in sequential["finish"]]

sequential = sequential.sort_values(by=['file size'])

sequential["file size"] = sequential["file size"] * coeff_bytes_2_go

color = '#000'

sequential_duration = dict(
    duration=sequential["elapsed time"].sum(),
    color=color,
)

x = sequential["file size"]
y = sequential["elapsed time"]

figs.add_trace(
    go.Scatter(
        x=x,
        y=y,
        name='sequential - observations',
        marker=dict(color=color, size=10),
        mode="markers",
    ),
    row=1,
    col=1,
)

# RUN asyncio aiohttp

data = [

{'name': '( Batch 0 - Item 7)', 'file size': 27452120, 'elapsed time': 20.284264, 'waiting_times': 18.066634, 'downloading_chunk_lengths': 16330.826888756692, 'writing_times': 0.205897, 'writing_chunk_lengths': 16340.547619047618, 'downloaded mean chunk size observed': 16330.826888756692, 'start': '2021-04-07 19:16:03.156157', 'finish': '2021-04-07 19:16:23.440421', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'error': ''},
{'name': '( Batch 0 - Item 3)', 'file size': 34680756, 'elapsed time': 25.247112, 'waiting_times': 22.538896, 'downloading_chunk_lengths': 16320.355764705882, 'writing_times': 0.274862, 'writing_chunk_lengths': 16328.0395480226, 'downloaded mean chunk size observed': 16320.355764705882, 'start': '2021-04-07 19:16:03.155448', 'finish': '2021-04-07 19:16:28.402560', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_200001-200512.nc', 'error': ''},
{'name': '( Batch 0 - Item 2)', 'file size': 54977076, 'elapsed time': 26.865872, 'waiting_times': 23.386480999999996, 'downloading_chunk_lengths': 16303.996441281139, 'writing_times': 0.402932, 'writing_chunk_lengths': 16308.83298724414, 'downloaded mean chunk size observed': 16303.996441281139, 'start': '2021-04-07 19:16:03.155244', 'finish': '2021-04-07 19:16:30.021116', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc', 'error': ''},
{'name': '( Batch 0 - Item 5)', 'file size': 54977076, 'elapsed time': 36.330191, 'waiting_times': 32.920662, 'downloading_chunk_lengths': 16352.491374182035, 'writing_times': 0.39119800000000005, 'writing_chunk_lengths': 16357.356739065754, 'downloaded mean chunk size observed': 16352.491374182035, 'start': '2021-04-07 19:16:03.155805', 'finish': '2021-04-07 19:16:39.485996', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_187001-187912.nc', 'error': ''},
{'name': '( Batch 0 - Item 4)', 'file size': 54977076, 'elapsed time': 36.590894, 'waiting_times': 33.192409, 'downloading_chunk_lengths': 16347.628902765387, 'writing_times': 0.38644, 'writing_chunk_lengths': 16352.491374182035, 'downloaded mean chunk size observed': 16347.628902765387, 'start': '2021-04-07 19:16:03.155627', 'finish': '2021-04-07 19:16:39.746521', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_196001-196912.nc', 'error': ''},
{'name': '( Batch 0 - Item 6)', 'file size': 54977076, 'elapsed time': 36.600914, 'waiting_times': 33.04594, 'downloading_chunk_lengths': 16323.359857482184, 'writing_times': 0.409059, 'writing_chunk_lengths': 16328.2079002079, 'downloaded mean chunk size observed': 16323.359857482184, 'start': '2021-04-07 19:16:03.155981', 'finish': '2021-04-07 19:16:39.756895', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_185001-185912.nc', 'error': ''},
{'name': '( Batch 0 - Item 0)', 'file size': 54977076, 'elapsed time': 36.905375, 'waiting_times': 33.366254999999995, 'downloading_chunk_lengths': 16362.225, 'writing_times': 0.39404, 'writing_chunk_lengths': 16367.096159571302, 'downloaded mean chunk size observed': 16362.225, 'start': '2021-04-07 19:16:03.154703', 'finish': '2021-04-07 19:16:40.060078', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_191001-191912.nc', 'error': ''},
{'name': '( Batch 0 - Item 1)', 'file size': 78675556, 'elapsed time': 58.386835, 'waiting_times': 53.882406, 'downloading_chunk_lengths': 16339.679335410177, 'writing_times': 0.568756, 'writing_chunk_lengths': 16343.073535521396, 'downloaded mean chunk size observed': 16339.679335410177, 'start': '2021-04-07 19:16:03.155055', 'finish': '2021-04-07 19:17:01.541890', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'error': ''},
{'name': '( Batch 0 - Item 8)', 'file size': 54977076, 'elapsed time': 39.198514, 'waiting_times': 30.876663, 'downloading_chunk_lengths': 16250.983151049364, 'writing_times': 0.392656, 'writing_chunk_lengths': 16255.7882909521, 'downloaded mean chunk size observed': 16250.983151049364, 'start': '2021-04-07 19:16:23.440550', 'finish': '2021-04-07 19:17:02.639064', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_198001-198912.nc', 'error': ''},
{'name': '( Batch 0 - Item 10)', 'file size': 47212396, 'elapsed time': 33.367849, 'waiting_times': 28.505034, 'downloading_chunk_lengths': 16285.7523283891, 'writing_times': 0.347949, 'writing_chunk_lengths': 16291.37198067633, 'downloaded mean chunk size observed': 16285.7523283891, 'start': '2021-04-07 19:16:30.021221', 'finish': '2021-04-07 19:17:03.389070', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'error': ''},
{'name': '( Batch 0 - Item 12)', 'file size': 78675556, 'elapsed time': 54.421487, 'waiting_times': 47.222308, 'downloading_chunk_lengths': 16278.823918890957, 'writing_times': 0.571081, 'writing_chunk_lengths': 16282.192880794702, 'downloaded mean chunk size observed': 16278.823918890957, 'start': '2021-04-07 19:16:39.746625', 'finish': '2021-04-07 19:17:34.168112', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'error': ''},
{'name': '( Batch 0 - Item 16)', 'file size': 47212548, 'elapsed time': 35.07534, 'waiting_times': 29.087044, 'downloading_chunk_lengths': 16376.187304890738, 'writing_times': 0.32314299999999996, 'writing_chunk_lengths': 16381.869535045107, 'downloaded mean chunk size observed': 16376.187304890738, 'start': '2021-04-07 19:17:02.639174', 'finish': '2021-04-07 19:17:37.714514', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/land/Lmon/r1i1p1/v20111018/mrsos/mrsos_Lmon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'error': ''},
{'name': '( Batch 0 - Item 13)', 'file size': 88114316, 'elapsed time': 59.150339, 'waiting_times': 51.380687, 'downloading_chunk_lengths': 16338.645651770814, 'writing_times': 0.63235, 'writing_chunk_lengths': 16341.675816023739, 'downloaded mean chunk size observed': 16338.645651770814, 'start': '2021-04-07 19:16:39.756988', 'finish': '2021-04-07 19:17:38.907327', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'error': ''},
{'name': '( Batch 0 - Item 15)', 'file size': 54977076, 'elapsed time': 40.348709, 'waiting_times': 32.843368999999996, 'downloading_chunk_lengths': 16376.847184986595, 'writing_times': 0.369194, 'writing_chunk_lengths': 16381.72705601907, 'downloaded mean chunk size observed': 16376.847184986595, 'start': '2021-04-07 19:17:01.541996', 'finish': '2021-04-07 19:17:41.890705', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_188001-188912.nc', 'error': ''},
{'name': '( Batch 0 - Item 17)', 'file size': 54977076, 'elapsed time': 43.692049, 'waiting_times': 37.715348999999996, 'downloading_chunk_lengths': 16328.2079002079, 'writing_times': 0.388528, 'writing_chunk_lengths': 16333.058823529413, 'downloaded mean chunk size observed': 16328.2079002079, 'start': '2021-04-07 19:17:03.389185', 'finish': '2021-04-07 19:17:47.081234', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_199001-199912.nc', 'error': ''},
{'name': '( Batch 0 - Item 18)', 'file size': 27452324, 'elapsed time': 25.14729, 'waiting_times': 18.125517, 'downloading_chunk_lengths': 16243.978698224852, 'writing_times': 0.195688, 'writing_chunk_lengths': 16253.596210775608, 'downloaded mean chunk size observed': 16243.978698224852, 'start': '2021-04-07 19:17:34.168212', 'finish': '2021-04-07 19:17:59.315502', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'error': ''},
{'name': '( Batch 0 - Item 11)', 'file size': 138079884, 'elapsed time': 83.338281, 'waiting_times': 75.419112, 'downloading_chunk_lengths': 16381.526159686795, 'writing_times': 0.9921160000000001, 'writing_chunk_lengths': 16383.46986236355, 'downloaded mean chunk size observed': 16381.526159686795, 'start': '2021-04-07 19:16:39.486103', 'finish': '2021-04-07 19:18:02.824384', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'error': ''},
{'name': '( Batch 0 - Item 14)', 'file size': 138080336, 'elapsed time': 88.458065, 'waiting_times': 79.1, 'downloading_chunk_lengths': 16379.63653618031, 'writing_times': 1.001158, 'writing_chunk_lengths': 16381.579784078776, 'downloaded mean chunk size observed': 16379.63653618031, 'start': '2021-04-07 19:16:40.060182', 'finish': '2021-04-07 19:18:08.518247', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/land/Lmon/r1i1p1/v1/mrsos/mrsos_Lmon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'error': ''},
{'name': '( Batch 0 - Item 20)', 'file size': 54977076, 'elapsed time': 35.228511, 'waiting_times': 30.148441, 'downloading_chunk_lengths': 16376.847184986595, 'writing_times': 0.42482400000000003, 'writing_chunk_lengths': 16381.72705601907, 'downloaded mean chunk size observed': 16376.847184986595, 'start': '2021-04-07 19:17:38.907460', 'finish': '2021-04-07 19:18:14.135971', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_194001-194912.nc', 'error': ''},
{'name': '( Batch 0 - Item 21)', 'file size': 47212016, 'elapsed time': 34.262989, 'waiting_times': 29.100497, 'downloading_chunk_lengths': 16091.348329925017, 'writing_times': 0.35795, 'writing_chunk_lengths': 16096.834640300034, 'downloaded mean chunk size observed': 16091.348329925017, 'start': '2021-04-07 19:17:41.890817', 'finish': '2021-04-07 19:18:16.153806', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc', 'error': ''},
{'name': '( Batch 0 - Item 25)', 'file size': 27451904, 'elapsed time': 20.205837, 'waiting_times': 15.911906, 'downloading_chunk_lengths': 16350.151280524122, 'writing_times': 0.202501, 'writing_chunk_lengths': 16359.895113230035, 'downloaded mean chunk size observed': 16350.151280524122, 'start': '2021-04-07 19:18:08.518385', 'finish': '2021-04-07 19:18:28.724222', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/v1/psl/psl_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'error': ''},
{'name': '( Batch 0 - Item 19)', 'file size': 78675024, 'elapsed time': 56.660766, 'waiting_times': 49.173632999999995, 'downloading_chunk_lengths': 16373.574193548387, 'writing_times': 0.5706249999999999, 'writing_chunk_lengths': 16376.982514571191, 'downloaded mean chunk size observed': 16373.574193548387, 'start': '2021-04-07 19:17:37.714627', 'finish': '2021-04-07 19:18:34.375393', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'error': ''},
{'name': '( Batch 0 - Item 23)', 'file size': 54977076, 'elapsed time': 36.254561, 'waiting_times': 30.673888999999996, 'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.401873, 'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267, 'start': '2021-04-07 19:17:59.315612', 'finish': '2021-04-07 19:18:35.570173', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_195001-195912.nc', 'error': ''},
{'name': '( Batch 0 - Item 22)', 'file size': 88114468, 'elapsed time': 59.095251, 'waiting_times': 52.243033, 'downloading_chunk_lengths': 16317.494074074075, 'writing_times': 0.662693, 'writing_chunk_lengths': 16320.51639192443, 'downloaded mean chunk size observed': 16317.494074074075, 'start': '2021-04-07 19:17:47.081348', 'finish': '2021-04-07 19:18:46.176599', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/land/Lmon/r1i1p1/v20110822/mrsos/mrsos_Lmon_CNRM-CM5_historical_r1i1p1_195001-200512.nc', 'error': ''},
{'name': '( Batch 0 - Item 26)', 'file size': 54977076, 'elapsed time': 36.689856, 'waiting_times': 31.296898, 'downloading_chunk_lengths': 16308.83298724414, 'writing_times': 0.399971, 'writing_chunk_lengths': 16313.672403560831, 'downloaded mean chunk size observed': 16308.83298724414, 'start': '2021-04-07 19:18:14.136075', 'finish': '2021-04-07 19:18:50.825931', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_189001-189912.nc', 'error': ''},
{'name': '( Batch 0 - Item 28)', 'file size': 78675404, 'elapsed time': 48.128077, 'waiting_times': 41.385735, 'downloading_chunk_lengths': 16346.43756492832, 'writing_times': 0.61509, 'writing_chunk_lengths': 16349.834580216126, 'downloaded mean chunk size observed': 16346.43756492832, 'start': '2021-04-07 19:18:28.724354', 'finish': '2021-04-07 19:19:16.852431', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc', 'error': ''},
{'name': '( Batch 0 - Item 31)', 'file size': 54977076, 'elapsed time': 36.983367, 'waiting_times': 31.696440000000003, 'downloading_chunk_lengths': 16376.847184986595, 'writing_times': 0.399964, 'writing_chunk_lengths': 16381.72705601907, 'downloaded mean chunk size observed': 16376.847184986595, 'start': '2021-04-07 19:18:46.176754', 'finish': '2021-04-07 19:19:23.160121', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_186001-186912.nc', 'error': ''},
{'name': '( Batch 0 - Item 32)', 'file size': 54977076, 'elapsed time': 32.376716, 'waiting_times': 27.289261999999994, 'downloading_chunk_lengths': 16270.220775377331, 'writing_times': 0.386613, 'writing_chunk_lengths': 16275.03730017762, 'downloaded mean chunk size observed': 16270.220775377331, 'start': '2021-04-07 19:18:50.826033', 'finish': '2021-04-07 19:19:23.202749', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_192001-192912.nc', 'error': ''},
{'name': '( Batch 0 - Item 24)', 'file size': 138079984, 'elapsed time': 80.692164, 'waiting_times': 71.32740899999999, 'downloading_chunk_lengths': 16381.538023490331, 'writing_times': 1.018087, 'writing_chunk_lengths': 16383.48172757475, 'downloaded mean chunk size observed': 16381.538023490331, 'start': '2021-04-07 19:18:02.824492', 'finish': '2021-04-07 19:19:23.516656', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'error': ''},
{'name': '( Batch 0 - Item 35)', 'file size': 27451972, 'elapsed time': 18.777885, 'waiting_times': 14.963367, 'downloading_chunk_lengths': 16350.191780821919, 'writing_times': 0.194159, 'writing_chunk_lengths': 16359.935637663886, 'downloaded mean chunk size observed': 16350.191780821919, 'start': '2021-04-07 19:19:23.202866', 'finish': '2021-04-07 19:19:41.980751', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/seaIce/OImon/r1i1p1/v1/sic/sic_OImon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc', 'error': ''},
{'name': '( Batch 0 - Item 27)', 'file size': 138080132, 'elapsed time': 92.026746, 'waiting_times': 82.762752, 'downloading_chunk_lengths': 16346.647567183616, 'writing_times': 1.010855, 'writing_chunk_lengths': 16348.582997868814, 'downloaded mean chunk size observed': 16346.647567183616, 'start': '2021-04-07 19:18:16.153919', 'finish': '2021-04-07 19:19:48.180665', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/atmos/Amon/r1i1p1/v1/tasmin/tasmin_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc', 'error': ''},
{'name': '( Batch 0 - Item 33)', 'file size': 54977076, 'elapsed time': 33.89334, 'waiting_times': 26.595382999999998, 'downloading_chunk_lengths': 16294.331950207468, 'writing_times': 0.394022, 'writing_chunk_lengths': 16299.162763118886, 'downloaded mean chunk size observed': 16294.331950207468, 'start': '2021-04-07 19:19:16.852554', 'finish': '2021-04-07 19:19:50.745894', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_190001-190912.nc', 'error': ''},
{'name': '( Batch 0 - Item 34)', 'file size': 78675404, 'elapsed time': 39.489458, 'waiting_times': 34.371520000000004, 'downloading_chunk_lengths': 16373.653277835589, 'writing_times': 0.561413, 'writing_chunk_lengths': 16377.061615320566, 'downloaded mean chunk size observed': 16373.653277835589, 'start': '2021-04-07 19:19:23.160334', 'finish': '2021-04-07 19:20:02.649792', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'error': ''},
{'name': '( Batch 0 - Item 36)', 'file size': 78675024, 'elapsed time': 42.93684, 'waiting_times': 36.633677, 'downloading_chunk_lengths': 16326.006225357958, 'writing_times': 0.56215, 'writing_chunk_lengths': 16329.394769613948, 'downloaded mean chunk size observed': 16326.006225357958, 'start': '2021-04-07 19:19:23.516762', 'finish': '2021-04-07 19:20:06.453602', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc', 'error': ''},
{'name': '( Batch 0 - Item 37)', 'file size': 54977076, 'elapsed time': 27.327852, 'waiting_times': 19.582963, 'downloading_chunk_lengths': 16371.970220369267, 'writing_times': 0.39447, 'writing_chunk_lengths': 16376.847184986595, 'downloaded mean chunk size observed': 16371.970220369267, 'start': '2021-04-07 19:19:41.980955', 'finish': '2021-04-07 19:20:09.308807', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/ocnBgchem/Omon/r1i1p1/v20120731/dissic/dissic_Omon_CNRM-CM5_historical_r1i1p1_193001-193912.nc', 'error': ''},
{'name': '( Batch 0 - Item 9)', 'file size': 795795032, 'elapsed time': 288.530289, 'waiting_times': 251.015771, 'downloading_chunk_lengths': 16380.113043657246, 'writing_times': 5.640181, 'writing_chunk_lengths': 16380.450207895929, 'downloaded mean chunk size observed': 16380.113043657246, 'start': '2021-04-07 19:16:28.402676', 'finish': '2021-04-07 19:21:16.932965', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/sic/sic_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'error': ''},
{'name': '( Batch 0 - Item 29)', 'file size': 795795708, 'elapsed time': 180.575284, 'waiting_times': 140.75691499999996, 'downloading_chunk_lengths': 16383.499227966155, 'writing_times': 6.035515, 'writing_chunk_lengths': 16383.836531334926, 'downloaded mean chunk size observed': 16383.499227966155, 'start': '2021-04-07 19:18:34.375501', 'finish': '2021-04-07 19:21:34.950785', 'strategy': 'asyncio aiohttp', 'status_code': 0, 'local_path': 'cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/seaIce/OImon/r1i1p1/v20130101/evap/evap_OImon_CNRM-CM5_historical_r1i1p1_185001-200512.nc', 'error': ''},


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

row = 2
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

# sequential

row = 1
col = 2

sequential_fig = px.timeline(
 sequential,
 title="Downloads",
 x_start="start",
 x_end="finish",
 y=sequential.index,
 color="strategy",
 color_discrete_map=VIEW_COLORS,
 text='elapsed time',
)

for trace in sequential_fig.data:
    figs.add_trace(trace, row=row, col=col)

figs.update_xaxes(type="date", row=row, col=col)

figs.update_yaxes(title_text="File", row=row, col=col)

# asyncio - aiohttp

row = 3
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
 'sequential ({} s)'.format(sequential_duration["duration"]),
 'synda version 3.2 ({} s)'.format(current32_duration["duration"]),
 'asyncio - aiohttp ({} s)'.format(asyncio_aiohttp_duration["duration"]),
)

# rotate all the subtitles of 90 degrees
for i, annotation in enumerate(figs['layout']['annotations']):
    annotation['text'] = titles[i]

figs.show()
