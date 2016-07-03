#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""This module contains paths and configuration parameters."""

import os
import argparse
import ConfigParser
from spexception import SPException
# this module do not import 'spapp' to prevent circular reference

def get_data_folder():
    if config.has_option('path','data_path'):
        path=config.get('path','data_path')
        if len(path)>0: # would be better to test with None (to do that, try using 'allow_no_value' when configuring ConfigParser)
            return path

    if not system_pkg_install:
        return  "%s/data"%root_folder
    else:
        return  "/srv/synda/sdp/data"

def get_db_folder():
    if config.has_option('path','db_path'):
        path=config.get('path','db_path')
        if len(path)>0: # would be better to test with None (to do that, try using 'allow_no_value' when configuring ConfigParser)
            return path

    if not system_pkg_install:
        return  "%s/db"%root_folder
    else:
        return  "/var/lib/synda/sdp"

def check_path(path):
    if not os.path.exists(path):
        raise SPException("SPCONFIG-101","Path not found (%s)"%path)

# init module.

system_pkg_install=False

if not system_pkg_install:
    if 'SP_HOME' not in os.environ:
        raise SPException('SPCONFIG-010',"'SP_HOME' not set")

    root_folder=os.environ['SP_HOME']
    tmp_folder="%s/tmp"%root_folder
    log_folder="%s/log"%root_folder
    conf_folder="%s/conf"%root_folder
else:
    root_folder='/usr/share/python/synda/sdp'
    tmp_folder='/var/tmp/synda/sdp'
    log_folder='/var/log/synda/sdp'
    conf_folder='/etc/synda/sdp'

bin_folder="%s/bin"%root_folder
pipeline_folder="%s/pipeline"%conf_folder

cleanup_tree_script="%s/spcleanup_tree.sh"%bin_folder
configuration_file="%s/sdp.conf"%conf_folder
stacktrace_log_file="%s/stacktrace.log"%log_folder
daemon_pid_file="%s/daemon.pid"%tmp_folder
ihm_pid_file="%s/ihm.pid"%tmp_folder
certificate_file='%s/server.pem'%tmp_folder

config = ConfigParser.ConfigParser()
config.read(configuration_file)

data_folder=get_data_folder()

db_folder=get_db_folder()
db_file="%s/sdp.db"%db_folder

check_path(root_folder)
check_path(data_folder)

prevent_daemon_and_ihm=False # prevent daemon/IHM concurrent accesses
prevent_ihm_and_ihm=False    # prevent IHM/IHM concurrent accesses
LFAE_mode="abort"            # LFAE means "local file already exists" (possible values are: "keep", "replace", "abort")

#  remove => if checksum doesn't match, set transfer status to error and remove file from local repository
#  keep   => if checksum doesn't match, set transfer status to done, log warning, keep file in local repository
incorrect_checksum_action="remove"

max_metadata_parallel_download_per_index=3

daemon_command_name='sprpcserver'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',default=None)
    args = parser.parse_args()

    if args.name is None:
        li=[]
        for k,v in locals().items():
            if '__' not in k: # prevent display of python system variables
                if k!='li':   # prevent display of this list
                    if isinstance(v, (str,int,basestring,float,bool,list, tuple)):
                        li.append("%s=%s"%(k,v))
        li=sorted(li)

        for v in li:
            print v
    else:
        if args.name in locals():
            print locals()[args.name]
