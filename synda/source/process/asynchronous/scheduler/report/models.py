# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import datetime
import tabulate

tabulate.PRESERVE_WHITESPACE = True


class Report(object):
    def __init__(self, scheduler):
        self.scheduler = None
        self.scheduler = scheduler
        self.add_columns()

    def get_metrics(self):
        report = [datetime.datetime.now().time()]
        columns = ["Time"]
        nb_workers = 0
        for manager in self.scheduler.get_managers():
            current_nb_running, current_nb_cancelled, current_nb_done = \
                manager.get_metrics()
            nb_workers += current_nb_running
            # if first:
            #     headers.extend(["batch", "running", "done"])
            columns.extend(["batch", "running", "done"])
            report.extend(
                [
                    "{:12}".format(int(manager.get_name())),
                    "{:12}".format(current_nb_running),
                    "{:12}".format(current_nb_done),
                ],
            )

        columns.append("nb_workers")
        report.append("{:12}".format(nb_workers))
        return report, columns

    def add_columns(self):
        report, columns = self.get_metrics()
        print("TIME & TASKS STATUS CHANGE".center(160, " "))
        print()
        print(tabulate.tabulate([report], columns, colalign=("right",)))

    def add_metrics(self):
        report, columns = self.get_metrics()
        print(tabulate.tabulate([report], colalign=("right",)))

        # print(tabulate.tabulate([report], headers, colalign=("right",), tablefmt="html"))
