#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module detect frozen wget."""

import os
import psutil # http://code.google.com/p/psutil/wiki/Documentation
import threading
import time
import argparse
import re
import sdapp
import sdlog

class FrozenDownloadCheckerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        watch()

def watch():
    previous_processes={}

    while True:
        new_processes={}

        # 10 mn sleep (exit event aware)
        for i in range(10):
            if quit==1:
                break
            for i in range(6):
                if quit==1:
                    break
                time.sleep(10)

        # exit event
        if quit==1:
            break

        scan_processes(previous_processes,new_processes)

        previous_processes=new_processes

def scan_processes(previous_processes,new_processes,debug=False):
    for pid in psutil.pids(): # retrieve wget pids
        try:
            p=psutil.Process(pid)
            if len(p.cmdline())>0:
                cmd=p.cmdline()[0]

                if cmd=="wget":

                    # second check to be sure not to take other wget process not related to our application
                    parent=psutil.Process(p.ppid())
                    if len(parent.cmdline())>1: # check array size not to raise exception in next line if wget is not related to our application
                        m=re.search("sdget.sh", parent.cmdline()[1])
                        if(m!=None):

                            # retrieve wget args
                            local_path=p.cmdline()[2] # this is a huge hack for the checksum/FIFO case !!!! (this class need to know the local file associated with the process, but because of the FIFO, this dest file do not show in "ps fax" output, so we put the dest file in unused " -D domain-list" option (this option is used only in recursive mode, which we do not use))
                            #local_path=p.cmdline()[4] # to be used without checksum
                            #url=p.cmdline()[-1] # retrieve url (not used for now)

                            if debug:
                                if os.path.isfile(local_path):
                                    print '%i %s'%(os.path.getsize(local_path),local_path)
                                else:
                                    print 'File not found: %s'%(local_path,)
                            else:
                                if os.path.isfile(local_path):
                                    check_if_frozen(p,pid,local_path,previous_processes,new_processes)
                                else:
                                    sdlog.info("SDWATCHD-274","file not found (%s%s)"%(local_path,pid)) # this can occur if wget already started, but didn't create the output file yet

        except Exception, e:
            if debug:
                raise
            else:
                # we silently trap exception during normal operation, because
                # some are raised during normal operation when a process
                # returned by psutil.pids() finished just before execution of
                # psutil.Process()
                pass

def check_if_frozen(p,pid,local_path,previous_processes,new_processes):
    key="%s%s"%(pid,local_path)
    fsize=os.path.getsize(local_path)

    if key in previous_processes:
        previous_size=previous_processes[key]

        # is size the same ? (means wget stalled)
        if fsize==previous_size:
            # not good

            sdlog.error("SDWATCHD-275","wget is stalled (%s,%s)"%(local_path,pid))
            p.terminate()
        else:
            # wget works perfectly, no pb

            #sdlog.debug("SDWATCHD-276","wget is not stalled (%s,%s)"%(local_path,pid))

            pass
    else:
        # new wget in town
        new_processes[key]=fsize

# module init.

quit=0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    scan_processes(None,None,True)
