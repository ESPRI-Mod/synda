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
import csv
from pandas import read_csv


def read_data(file_name, sep, header=None, names=None, index_col=None):
    data = \
        read_csv(
            file_name,
            encoding='utf8',
            engine='python',
            sep=sep,
            header=header,
            names=names,
            index_col=index_col,
        )
    return data


def read_header(full_filename, delimiter=';'):
    with open(full_filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        header = next(reader)
        f.close()
    return header


if __name__ == '__main__':
    pass
