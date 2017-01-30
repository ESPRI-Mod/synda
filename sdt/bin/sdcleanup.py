#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains cleanup routines."""

import os
import argparse
import sdapp
import sdconfig
import sdlog
import sdtools
import sdutils
from sdexception import SDException

def remove_empty_files(path):
    for p in sdtools.walk_backward_without_sibling(path):
        for x in os.listdir(p):
            if os.isfile(x):
                if not os.islink(x):
                    f = '%s/%s' % (p,x)
                    if os.path.getsize(f)==0:
                        try:
                            sdlog.debug("SYNCLEAN-090","os.remove(%s)"%(f,))
                            os.remove(f)
                        except Exception as e:
                            sdlog.warning("SYNCLEAN-040","Error occurs during file deletion (%s,%s)"%(f,str(e)))

def full_cleanup():
    """Remove empty files and folders."""

    sdlog.info("SYNCLEAN-008","Starting cleanup in %s."%sdconfig.data_folder)

    argv=[sdconfig.cleanup_tree_script,sdconfig.data_folder]

    (status,stdout,stderr)=sdutils.get_status_output(argv)
    if status!=0:
        sdtools.trace(sdconfig.stacktrace_log_file,os.path.basename(sdconfig.cleanup_tree_script),status,stdout,stderr)
        raise SDException("SYNCLEAN-001","Error occurs during tree cleanup")

    sdlog.info("SYNCLEAN-010","Cleanup done.")

def part_cleanup(paths):
    """Remove empty files and folders."""

    sdlog.info("SYNCLEAN-018","Starting cleanup")

    paths=sorted(paths, reverse=True) # maybe overkill

    for p in paths:

        # remove empty files
        remove_empty_files(p)

        # remove empty directories starting from leaves
        sdlog.debug("SYNCLEAN-100","os.removedirs(%s)"%(p,))
        os.removedirs(p)

    sdlog.info("SYNCLEAN-020","Cleanup done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    full_cleanup()
