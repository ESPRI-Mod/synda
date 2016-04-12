#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains paths and configuration parameters."""

import os
import argparse
import ConfigParser
import sdtools
from sdexception import SDException
# this module do not import 'sdapp' to prevent circular reference
# this module do not import 'sdlog' as used by sddaemon module (i.e. double fork pb)

def get_data_folder():
        path=config.get('core','data_path')
        if len(path)>0: # would be better to test with None (to do that, try using 'allow_no_value' when configuring ConfigParser)
            return path

    return "%s/data"%root_folder

def get_db_folder():
        path=config.get('core','db_path')
        if len(path)>0: # would be better to test with None (to do that, try using 'allow_no_value' when configuring ConfigParser)
            return path

    return "%s/db"%root_folder

def get_project_default_selection_file(project):
    path="%s/default_%s.txt"%(selection_default_folder,project)
    return path

def find_selection_file(file):
    if os.path.isfile(file):
        # file found

        return file
    else:
        if '/' in file:
            # path

            # if we are here, path is incorrect.
            # we return the path 'as is'
            # (it will trigger an error message in the calling func)

            return file
        else:
            # filename

            # if we are here, we expect the file to be in the 'selection' folder

            return "%s/%s"%(selections_folder,file)

def check_path(path):
    if not os.path.exists(path):
        raise SDException("SDATYPES-101","Path not found (%s)"%path)

def print_(name):
    if name is None:
        # print all configuration parameters

        sdtools.print_module_variables(globals())
    else:
        # print given configuration parameter

        if name in globals():
            print globals()[name]

# Init module.

if 'ST_HOME' not in os.environ:
    raise SDException('SDCONFIG-010',"'ST_HOME' is not set")

root_folder=os.environ['ST_HOME']
tmp_folder="%s/tmp"%root_folder
selections_folder="%s/selection"%root_folder
log_folder="%s/log"%root_folder
conf_folder="%s/conf"%root_folder
bin_folder="%s/bin"%root_folder

selection_default_folder="%s/default"%conf_folder

data_download_script_http="%s/sdget.sh"%bin_folder
data_download_script_gridftp="%s/sdgetg.sh"%bin_folder

logon_script="%s/sdlogon.sh"%bin_folder
cleanup_tree_script="%s/sdcleanup_tree.sh"%bin_folder
default_selection_file="%s/default.txt"%selection_default_folder
configuration_file="%s/sdt.conf"%conf_folder
credential_file="%s/credentials.conf"%conf_folder
user_configuration_file=os.path.expanduser("~/.syndarc")

stacktrace_log_file="%s/stacktrace.log"%log_folder

daemon_pid_file="%s/daemon.pid"%tmp_folder
ihm_pid_file="%s/ihm.pid"%tmp_folder

multiuser=False

# TODO: replace default options DICTIONNARY below with a default options FILE
# (pb with options below is that they are available in all sections)
default_options={'max_parallel_download':'8',
                 'user':'',
                 'group':'',
                 'hpss':'0',
                 'post_processing':'0',
                 'globustransfer':'0',
                 'data_path':'',
                 'db_path':'',
                 'unicode_term':'0',
                 'progress':'1',
                 'onemgf':'false',
                 'ignorecase':'true',
                 'check_parameter':'1',
                 'verbosity_level':'info',
                 'scheduler_profiling':'0',
                 'lfae_mode':'abort',
                 'indexes':'esgf-node.ipsl.fr,esgf-data.dkrz.de,esgf-index1.ceda.ac.uk',
                 'default_index':'esgf-node.ipsl.fr',
                 'nearest':'false',
                 'nearest_mode':'geolocation',
                 'incorrect_checksum_action':'remove'}

# global options
config = ConfigParser.ConfigParser(default_options)
config.read(configuration_file)

# user options override global options (if any user options)
if not sdtools.is_daemon():
    if os.path.exists(user_configuration_file):
        config.read(user_configuration_file)

# set security_dir
#
# TODO
#     may use tmp_folder for both to improve consistency (if HOME is used in multi-user mode, it can be root or daemon unprivileged user which increase complexity)
#
if multiuser:
    security_dir="%s/.esg"%tmp_folder
else:
    security_dir="%s/.esg"%os.environ['HOME']

# set x509 paths
esgf_x509_proxy=os.path.join(security_dir,'credentials.pem')
esgf_x509_cert_dir=os.path.join(security_dir,'certificates')

# credential file
if multiuser:
    if sdtools.is_root():
        config.read(credential_file)
else:
    config.read(credential_file)

data_folder=get_data_folder()
db_folder=get_db_folder()
db_file="%s/sdt.db"%db_folder

check_path(root_folder)
check_path(selections_folder)
check_path(data_folder)

prevent_daemon_and_modification=False # prevent modification while daemon is running
prevent_daemon_and_ihm=False # prevent daemon/IHM concurrent accesses
prevent_ihm_and_ihm=False    # prevent IHM/IHM concurrent accesses

files_download=True # if set to False, daemon do not renew certificate nor download files (useful to use synda in post-processing mode only)

dataset_filter_mecanism_in_file_context='dataset_id' # dataset_id | query

max_metadata_parallel_download_per_index=3
sdtc_history_file=os.path.expanduser("~/.sdtc_history")

http_client='wget' # wget | urllib

daemon_command_name='sdtaskscheduler'

# note that variable below only set which low_level mecanism to use to find the nearest (i.e. it's not an on/off flag (the on/off flag is the 'nearest' selection file parameter))
nearest_schedule='post' # pre | post

unknown_value_behaviour='error' # error | warning

mono_host_retry=False
proxymt_progress_stat=False
poddlefix=True
fix_encoding=False

twophasesearch=False # Beware before enabling this: must be well tested/reviewed as it seems to currently introduce regression.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',default=None,help='Name of the parameter to be displayed (if not set, all parameters are displayed)')
    parser.add_argument('--testconfigparser',action='store_true',help='Test ConfigParser')
    args = parser.parse_args()

    if args.testconfigparser:
        openid=config.get('esgf_credential','openid')
        print openid
    else:
        print_(args.name)
