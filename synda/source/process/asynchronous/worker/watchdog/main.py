# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sys
import shutil
import os
import asyncio
# wiper.py


# class Wipe(object):
#     def __repr__(self):
#         return '\n'* 4
#
# wipe = Wipe()

cls = lambda: print("\033c\033[3J", end='')

if __name__ == '__main__':

    import time
    import os

    # print("toto", end="\r")
    # # sys.stdout.flush()
    # time.sleep(1)
    # print("\ntata", end="\r")
    # time.sleep(1)
    # print("toto", end="\r")
    # time.sleep(1)
    # print("titi", end="\r")
    # # sys.stdout.flush()
    # time.sleep(1)
    # print("tutu", end="\r")
    # time.sleep(1)

    for i in range(10):
        print(i)
        print("toto")
        print("tata")
        time.sleep(1)
        if i < 9:
            cls()
