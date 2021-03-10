#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains database normalization routines."""

import argparse
from synda.sdt import sdapp
from synda.sdt import sdnormalize
from synda.sdt import sdprogress

def normalize_checksum_type(conn):
    conn.create_function("NORMALIZE_CHECKSUM_TYPE", 1, sdnormalize.normalize_checksum_type)
    conn.execute("UPDATE file set checksum_type=NORMALIZE_CHECKSUM_TYPE(checksum_type);")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    from synda.sdt import sddb # do not move at the top (this module is used by sddb module)
    normalize_checksum_type(sddb.conn)
    sddb.conn.commit()
