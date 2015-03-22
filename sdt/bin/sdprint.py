#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdprint.py 3053 2014-03-10 14:07:17Z jripsl $
#  @version        $Rev: 3053 $
#  @lastrevision   $Date: 2014-03-10 15:07:17 +0100 (Mon, 10 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains print routines."""

import json
import sys

def print_format(files,format,print_only_one_item=False,fh=sys.stdout):
    """Print files list with given format."""

    if print_only_one_item:
        files=[files[0]]
        format='indent' # force format to indent when displaying only one item

    if format == 'raw':
        fh.write("%s\n"%json.dumps(files))
    elif format == 'line':
        for f in files:
            fh.write("%s\n"%json.dumps(f))
    elif format == 'indent':
        fh.write("%s\n"%json.dumps(files,indent=4, separators=(',', ': ')))
