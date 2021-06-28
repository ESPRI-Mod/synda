# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import datetime
import threading
import time
import pandas as pd

from synda.source.constants import get_env_folder
from synda.source.db.task.file.read.utils import get_local_paths_and_sizes


def get_local_full_finame(local_path):
    root = get_env_folder()
    return os.path.join(
        os.path.join(
            root,
            "data",
        ),
        local_path,
    )


def is_downloading_completed(df):
    completed = False
    downloaded_size = 0
    for i in df.index:
        if df["completed"][i]:
            downloaded_sizei = df["size"][i]
        else:
            local_full_filename = df["local_full_filename"][i]
            if os.path.isfile(local_full_filename):
                downloaded_sizei = os.path.getsize(local_full_filename)
                if downloaded_sizei == df["size"][i]:
                    df.loc[i, "completed"] = True
            else:
                downloaded_sizei = 0
        downloaded_size += downloaded_sizei

    if df["size"].sum() == downloaded_size:
        completed = True

    return completed, downloaded_size


def get_downloading_duration(local_paths_and_sizes):

    data = []
    for item in local_paths_and_sizes:
        new_item = dict()
        new_item['size'] = item['size']
        new_item['local_full_filename'] = get_local_full_finame(item['local_path'])
        new_item["completed"] = False
        data.append(new_item)

    df = pd.DataFrame(data)

    begin = None
    end = None
    started = False
    finished = False

    completed, downloaded_size = is_downloading_completed(df)

    if downloaded_size:
        print()
        print(">>>>> SOME FILES already EXIST <<<<<")
        print()
        begin = end = datetime.datetime.now()

    else:

        while not finished:

            completed, downloaded_size = is_downloading_completed(df)

            if not started:
                if downloaded_size:
                    started = True
                    begin = datetime.datetime.now()
                    display_downloading_date(begin)
                else:
                    time.sleep(1.0)
            else:
                if completed:
                    finished = True
                    end = datetime.datetime.now()
                    display_downloading_date(end)
                else:
                    time.sleep(1.0)

    return (end - begin).total_seconds(), df


def display_downloading_date(date):
    print(date)


def display_report(duration, df):

    print("              REPORT")
    print("")
    print(
        "   {} Files, {} Bytes".format(
            len(df.index),
            df["size"].sum(),
        ),
    )
    print("")
    print(
        {'calculated from os': duration}
    )


def downloading_control(local_paths_and_sizes):
    print("========================================")
    print("Downloading control in progress...")
    duration, df = get_downloading_duration(local_paths_and_sizes)
    display_report(duration, df)
    print("========================================")


def launch_downloading_control(local_paths_and_sizes):
    thread = threading.Thread(
        target=downloading_control,
        args=(local_paths_and_sizes,),
    )

    thread.start()
    thread.join()


if __name__ == '__main__':
    _data = get_local_paths_and_sizes()
    launch_downloading_control(_data)
