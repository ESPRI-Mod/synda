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
import sys
import uuid
import argparse
import sdconst
import sdtools
import sdcfloader
import sdconfigutils
import sdi18n
import sdcfbuilder
from sdexception import SDException
# this module do not import 'sdapp' to prevent circular reference
# this module do not import 'sdlog' as used by sddaemon module (i.e. double fork pb)

def get_security_dir():
    if security_dir_mode==sdconst.SECURITY_DIR_TMP:
        security_dir="%s/.esg"%tmp_folder
    elif security_dir_mode==sdconst.SECURITY_DIR_TMPUID:
        security_dir="%s/%s/.esg"%(tmp_folder,str(os.getuid()))
    elif security_dir_mode==sdconst.SECURITY_DIR_HOME:
        if 'HOME' not in os.environ:
            raise SDException('SDCONFIG-120',"HOME env. var. must be set when 'security_dir_mode' is set to %s"%sdconst.SECURITY_DIR_HOME)
        security_dir="%s/.esg"%os.environ['HOME']
    elif security_dir_mode==sdconst.SECURITY_DIR_MIXED:
        wia=sdtools.who_am_i()
        if wia=='ihm':
            if 'HOME' not in os.environ:
                raise SDException('SDCONFIG-121',"HOME env. var. must be set when 'security_dir_mode' is set to %s in a IHM context"%sdconst.SECURITY_DIR_MIXED)
            security_dir="%s/.esg"%os.environ['HOME']
        elif wia=='daemon':
            security_dir="%s/.esg"%tmp_folder
        else:
            assert False
    else:
        raise SDException('SDCONFIG-020',"Incorrect value for security_dir_mode (%s)"%security_dir_mode)

    return security_dir

def get_default_limit(command):
    return sdconst.DEFAULT_LIMITS[default_limits_mode][command]

def get_path(name,default_value):
    path=config.get('core',name)
    if len(path)>0:
        return path
    else:
        return default_value

def get_project_default_selection_file(project):
    path="%s/default_%s.txt"%(default_folder,project)
    return path

def check_path(path):
    if not os.path.exists(path):
        raise SDException("SDCONFIG-014","Path not found (%s)"%path)

def print_(name):
    if name is None:
        # print all configuration parameters

        sdtools.print_module_variables(globals())
    else:
        # print given configuration parameter

        if name in globals():
            print globals()[name]

def is_openid_set():
    if openid=='https://esgf-node.ipsl.fr/esgf-idp/openid/foo':
        return False
    else:
        return True

def is_event_enabled(event,project):
    if event==sdconst.EVENT_FILE_COMPLETE:
        return False
    elif event==sdconst.EVENT_VARIABLE_COMPLETE:
        if project=='CMIP5':
            return False # CMIP5 use special output12 event
        else:
            return True

# Init module.

os.umask(0002)

system_pkg_install=False

# set synda folders paths (aka install-folders)
if not system_pkg_install:
    if 'ST_HOME' not in os.environ:
        raise SDException('SDCONFIG-010',"'ST_HOME' is not set")

    install_paths=sdconfigutils.SourceInstallPaths(os.environ['ST_HOME'])
else:
    install_paths=sdconfigutils.PackageSystemPaths()

# set user folders
user_paths=sdconfigutils.UserPaths(os.path.expanduser("~/.sdt"))


if sdtools.is_file_read_access_OK(install_paths.credential_file):
    paths=install_paths
else:
    # if we are here, it means we have NO access to the machine-wide credential file.

    if os.environ.get('SDT_USER_ENV','0')=='1':
        # Being here means we use machine-wide synda environment as non-admin synda user,
        # and so can only perform RO task (eg synda search, synda get, etc..)
        # Also it means we are not in daemon mode (daemon mode is currently only
        # available for admin-user. see TAG43J2K253J43 for more infos.)

        # Non fully working as multi-daemon support not implemented yet. But works for
        # basic command (eg 'synda get')

        user_paths.create_tree()
        paths=user_paths
    else:
        # being here means synda application can only be used by root or admin (admin means being in the synda group)

        sdtools.print_stderr(sdi18n.m0027)
        sys.exit(1)

# aliases
bin_folder=paths.bin_folder
tmp_folder=paths.tmp_folder
log_folder=paths.log_folder
conf_folder=paths.conf_folder
#
default_selection_folder=paths.default_selection_folder
default_db_folder=paths.default_db_folder
default_data_folder=paths.default_data_folder
default_sandbox_folder=paths.default_sandbox_folder
#
default_folder_default_path=paths.default_folder_default_path
configuration_file=paths.configuration_file
credential_file=paths.credential_file


stacktrace_log_file="/tmp/sdt_stacktrace_%s.log"%str(uuid.uuid4())

daemon_pid_file="%s/daemon.pid"%tmp_folder
ihm_pid_file="%s/ihm.pid"%tmp_folder

check_path(bin_folder)

prevent_daemon_and_modification=False # prevent modification while daemon is running
prevent_daemon_and_ihm=False # prevent daemon/IHM concurrent accesses
prevent_ihm_and_ihm=False    # prevent IHM/IHM concurrent accesses

log_domain_inconsistency=True # this is to prevent flooding log file with domain message during debugging session (i.e. set it to false when debugging).
print_domain_inconsistency=True # If true, domain inconsistencies are printed on stderr

dataset_filter_mecanism_in_file_context='dataset_id' # dataset_id | query

max_metadata_parallel_download_per_index=3
sdtc_history_file=os.path.expanduser("~/.sdtc_history")

metadata_parallel_download=False
http_client='wget' # wget | urllib

# note that variable below only set which low_level mecanism to use to find the nearest (i.e. it's not an on/off flag (the on/off flag is the 'nearest' selection file parameter))
nearest_schedule='post' # pre | post

unknown_value_behaviour='error' # error | warning

mono_host_retry=False
proxymt_progress_stat=False
poddlefix=True
lowmem=True
fix_encoding=False
twophasesearch=False # Beware before enabling this: must be well tested/reviewed as it seems to currently introduce regression.
stop_download_if_error_occurs=False # If true, stop download if error occurs during download, if false, the download continue. Note that in the case of a certificate renewal error, the daemon always stops not matter if this false is true or false.

config=sdcfloader.load(configuration_file,credential_file)


# alias
#
# Do not move me upward nor downward
# ('security_dir_mode' must be defined before any call to the get_security_dir() func, and config must be defined)
#
security_dir_mode=config.get('core','security_dir_mode')


# Set location of ESGF X.509 credential
esgf_x509_proxy=os.path.join(get_security_dir(),'credentials.pem')
esgf_x509_cert_dir=os.path.join(get_security_dir(),'certificates')


# aliases (indirection to ease configuration parameter access)
openid=config.get('esgf_credential','openid')
password=config.get('esgf_credential','password')
progress=config.getboolean('interface','progress')
download=config.getboolean('module','download')
metadata_server_type=config.get('core','metadata_server_type')

default_folder=get_path('default_path',default_folder_default_path)
selection_folder=get_path('selection_path',default_selection_folder)
db_folder=get_path('db_path',default_db_folder)
data_folder=get_path('data_path',default_data_folder)
sandbox_folder=get_path('sandbox_path',default_sandbox_folder)

data_download_script_http="%s/sdget.sh"%bin_folder
data_download_script_gridftp="%s/sdgetg.sh"%bin_folder

cleanup_tree_script="%s/sdcleanup_tree.sh"%bin_folder

default_selection_file="%s/default.txt"%default_folder
db_file="%s/sdt.db"%db_folder

check_path(selection_folder)
check_path(data_folder)

# destination folder for 'synda get'
#
# Allowed value
#     None
#     sandbox_folder
#
# Note
#     when set to None, destination folder is the current working directory (as wget)
#
files_dest_folder_for_get_subcommand=None

default_limits_mode=config.get('interface','default_listing_size')

# Set default type (File | Dataset | Variable)
sdtsaction_type_default=sdconst.SA_TYPE_FILE if metadata_server_type=='apache_default_listing' else sdconst.SA_TYPE_DATASET

# Note
#     When set to xml, 'lxml' package is required (must be added both in install.sh and in requirements.txt)
searchapi_output_format=sdconst.SEARCH_API_OUTPUT_FORMAT_JSON

# if set to True, automatically switch to the next url if error occurs (e.g. move from gridftp url to http url)
next_url_on_error=config.getboolean('download','http_fallback')

show_advanced_options=False

# when true, allow fast cycle for test (used for UAT)
fake_download=False

copy_ds_attrs=False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',default=None,help='Name of the parameter to be displayed (if not set, all parameters are displayed)')
    args = parser.parse_args()

    print_(args.name)
