#!/usr/bin/env python3.6
import sys
import time
import asyncio
from contextlib import closing

import aiohttp
from tqdm.asyncio import tqdm


async def download(session, url, progress_queue):
    downloaded_so_far = 0
    progressbar_size = 50
    start_of_download = time.time()

    async with session.get(url) as response:
        target = url.rpartition('/')[-1]
        size = int(response.headers.get('content-length', 0)) or None
        position = await progress_queue.get()

        # progressbar = tqdm(
        #     desc=target, total=size, position=position, leave=False,
        # )

        with open(target, mode='wb') as f:
            async for chunk in response.content.iter_chunked(512):
                downloaded_so_far += len(chunk)
                progressbar_done = int(progressbar_size * downloaded_so_far / size)
                rate = (downloaded_so_far // (time.time() - start_of_download)) // 1024
                f.write(chunk)
                sys.stdout.write(
                    "\r[{}{}] {} KiB/s".format(
                        '=' * progressbar_done,
                        ' ' * (progressbar_size - progressbar_done),
                        rate,
                    ),
                )
                # sys.stdout.flush()

        await progress_queue.put(position)

        return target


async def main(loop):

    urls = [

        'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/psl/psl_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
        # 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc',
        # 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc',
        # 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_190001-194912.nc',
        # 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/psl/psl_Amon_CNRM-CM5_historical_r1i1p1_195001-200512.nc',
        # 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/historical/mon/atmos/Amon/r1i1p1/v20110901/tasmin/tasmin_Amon_CNRM-CM5_historical_r1i1p1_185001-189912.nc',

    ]

    progress_queue = asyncio.Queue(loop=loop)
    for pos in range(5):
        progress_queue.put_nowait(pos)

    async with aiohttp.ClientSession(loop=loop) as session:

        tasks = [download(session, url, progress_queue) for url in urls]
        return await asyncio.gather(*tasks)


if __name__ == '__main__':

    with closing(asyncio.get_event_loop()) as loop:
        for tgt in loop.run_until_complete(main(loop)):
            print(tgt)
