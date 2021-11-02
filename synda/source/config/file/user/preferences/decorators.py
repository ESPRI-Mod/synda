# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
from synda.sdt.sdtime import SDTimer
from synda.sdt import sdlog


def print_elapsed_time():
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = SDTimer.get_time()
            result = func(*args, **kwargs)
            elapsed_time = SDTimer.get_elapsed_time(start_time)
            # print('SDPROFIL-001', '%s ran in %2.9f sec' % (func.__name__, elapsed_time))
            # data = dict(
            #     time=elapsed_time,
            #     validated=result,
            # )
            # print(f"{data},")

            return result
        return wrapper
    return decorator


def report_elapsed_time_into_log_file(scheduler_profiling):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if scheduler_profiling:
                start_time = SDTimer.get_time()
                result = func(*args, **kwargs)
                elapsed_time = SDTimer.get_elapsed_time(start_time)

                sdlog.info('SDPROFIL-001', '%s ran in %2.9f sec' % (func.__name__, elapsed_time))

                return result

            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":

    import time

    @report_elapsed_time_into_log_file(0)
    def test0():
        time.sleep(2)

    @report_elapsed_time_into_log_file(1)
    def test1():
        time.sleep(3)

    test0()
    test1()
