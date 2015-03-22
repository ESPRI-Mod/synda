#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdrtt.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module compute the round trip time between two host.

Note
    sdrtt means 'Synchro-Data Round Trip Time'.
"""

import re
import argparse
import sdutils
from sdexception import SDException

def compute_RTT(remote_host,count=1):
    """
    Args
        count: how many ping used to compute the average RTT
    """
    rtt=0.0

    (status,stdout,stderr)=sdutils.get_status_output('ping -q -c %i %s'%(count,remote_host),shell=True)
    if status==0:
        m = re.search('.*min/avg/max/mdev = ([0-9.]+)/([0-9.]+)/([0-9.]+)/([0-9.]+) ms.*', stdout,re.MULTILINE|re.DOTALL)
        if m: 
            rtt=float(m.group(2))
        else: 
            raise SDException("SYNDARTT-001","'ping' output parsing error (%s)"%(stdout,))
    else: 
        raise SDException("SYNDARTT-002","'ping' command failed (remote_host=%s,status=%i)"%(remote_host,status,))

    return rtt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    rtt=compute_RTT('google.fr')
    print rtt
