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
import sdconst
import sdtools
import sdcfloader
import sdcfbuilder
from sdexception import SDException
# this module do not import 'sdapp' to prevent circular reference
# this module do not import 'sdlog' as used by sddaemon module (i.e. double fork pb)

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
        raise SDException("SDATYPES-101","Path not found (%s)"%path)

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

def is_special_user():
    """
    Notes
        - special-user can be
            - root (when using system package installation)
            - <user> who performed synda installation from source (can be root or a normal user)
    """

    if system_pkg_install:
        # in system package based installation, root is always the special-user

        if sdtools.is_root():
            return True
        else:
            return False

    else:
        # in source based installation, the special-user can be any user

        if sdtools.is_file_read_access_OK(credential_file):

            # note that root is always considered 'special-user'
            # because of the side-effect that he have access to all files.
            # maybe use 'file owner' here instead to fix this.

            return True
        else:
            return False

# Init module.

system_pkg_install=False

if not system_pkg_install:
    if 'ST_HOME' not in os.environ:
        raise SDException('SDCONFIG-010',"'ST_HOME' is not set")

    root_folder=os.environ['ST_HOME']
    tmp_folder="%s/tmp"%root_folder
    log_folder="%s/log"%root_folder
    conf_folder="%s/conf"%root_folder

    default_selection_folder="%s/selection"%root_folder
    default_db_folder="%s/db"%root_folder
    default_data_folder="%s/data"%root_folder
    default_sandbox_folder="%s/sandbox"%root_folder
else:
    root_folder='/usr/share/python/synda/sdt'
    tmp_folder='/var/tmp/synda/sdt'
    log_folder='/var/log/synda/sdt'
    conf_folder='/etc/synda/sdt'

    default_selection_folder='/etc/synda/sdt/selection'
    default_db_folder='/var/lib/synda/sdt'
    default_data_folder='/srv/synda/sdt/data'
    default_sandbox_folder='/srv/synda/sdt/sandbox'

default_folder_default_path="%s/default"%conf_folder


configuration_file="%s/sdt.conf"%conf_folder
credential_file="%s/credentials.conf"%conf_folder

user_root_dir=os.path.expanduser("~/.sdt")
user_conf_dir=os.path.join(user_root_dir,'conf')

user_configuration_file=os.path.join(user_conf_dir,"sdt.conf")
user_credential_file=os.path.join(user_conf_dir,"credentials.conf")

stacktrace_log_file="%s/stacktrace.log"%log_folder

daemon_pid_file="%s/daemon.pid"%tmp_folder
ihm_pid_file="%s/ihm.pid"%tmp_folder

# set security_dir
if sdtools.is_daemon():

    # better keep tmp_folder for this case
    # (if HOME is used here, it can be root or daemon
    # unprivileged user which increase complexity)

    security_dir="%s/.esg"%tmp_folder
else:

    #if system_pkg_install:
    if is_special_user():

        # we may use HOME in this case too,
        # but when doing that, this error occurs (on sl67 with rpm pkg):
        #
        # Starting synda daemon (sdt): Traceback (most recent call last):
        #   File "/usr/share/python/synda/sdt/bin/sddaemon.py", line 39, in <module>
        #     import sdconfig
        #   File "/usr/share/python/synda/sdt/bin/sdconfig.py", line 170, in <module>
        #     security_dir="%s/.esg"%os.environ['HOME']
        #   File "/usr/share/python/synda/sdt/lib64/python2.6/UserDict.py", line 22, in __getitem__
        #     raise KeyError(key)
        # KeyError: 'HOME'


        security_dir="%s/.esg"%tmp_folder
    else:

        # OLD
        #security_dir="%s/.esg"%os.environ['HOME']

        # TAGJ4K53J45
        #
        # 'OLD' has been disabled, because error below occurs when running 'service' command as a non-special user (vagrant user on sl67 with rpm pkg)
        #
        # [vagrant@localhost ~]$ service synda status
        # Traceback (most recent call last):
        #   File "/usr/share/python/synda/sdt/bin/sddaemon.py", line 36, in <module>
        #     import sdconfig
        #   File "/usr/share/python/synda/sdt/bin/sdconfig.py", line 162, in <module>
        #     security_dir="%s/.esg"%os.environ['HOME']
        #   File "/usr/share/python/synda/sdt/lib64/python2.6/UserDict.py", line 22, in __getitem__
        #     raise KeyError(key)
        # KeyError: 'HOME'

        # NEW
        if 'HOME' in os.environ:
            security_dir="%s/.esg"%os.environ['HOME']
        else:
            # we shouldn't be here
            # (the only reason is TAGJ4K53J45)

            # this is just to prevent TAGJ4K53J45 ugly error
            # (i.e. the folder will not be used to store certificate as we are here only via 'service synda' command)
            security_dir="%s/.esg"%tmp_folder

# set x509 paths
esgf_x509_proxy=os.path.join(security_dir,'credentials.pem')
esgf_x509_cert_dir=os.path.join(security_dir,'certificates')

check_path(root_folder)

prevent_daemon_and_modification=False # prevent modification while daemon is running
prevent_daemon_and_ihm=False # prevent daemon/IHM concurrent accesses
prevent_ihm_and_ihm=False    # prevent IHM/IHM concurrent accesses

log_domain_inconsistency=True # this is to prevent flooding log file with domain message during debugging session (i.e. set it to false when debugging).

dataset_filter_mecanism_in_file_context='dataset_id' # dataset_id | query

max_metadata_parallel_download_per_index=3
sdtc_history_file=os.path.expanduser("~/.sdtc_history")

metadata_parallel_download=False
http_client='wget' # wget | urllib

# note that variable below only set which low_level mecanism to use to find the nearest (i.e. it's not an on/off flag (the on/off flag is the 'nearest' selection file parameter))
nearest_schedule='post' # pre | post

unknown_value_behaviour='error' # error | warning

# this is to switch between 'sdmyproxy.py' and 'sdlogon.sh'
use_myproxy_module=True

# Type of metadata server. Default is 'esgf_search_api'.
metadata_server_type='esgf_search_api' # 'esgf_search_api' | 'thredds_catalog' | 'apache_default_listing'

# Set default type (File | Dataset | Variable)
sdtsaction_type_default=sdconst.SA_TYPE_FILE if metadata_server_type=='apache_default_listing' else sdconst.SA_TYPE_DATASET

mono_host_retry=False
proxymt_progress_stat=False
poddlefix=True
lowmem=True
fix_encoding=False
twophasesearch=False # Beware before enabling this: must be well tested/reviewed as it seems to currently introduce regression.
stop_download_if_error_occurs=False # If true, stop download if error occurs during download, if false, the download continue. Note that in the case of a certificate renewal error, the daemon always stops not matter if this false is true or false.

if not is_special_user():
    # if we are here, it means we have no access to the machine-wide credential file.

    # also if we are here, we are not in daemon mode (daemon mode is
    # currently only available for special-user. see TAG43J2K253J43 for more
    # infos.)

    # create user credential file sample
    if not os.path.exists(user_credential_file):
        if not os.path.exists(user_conf_dir):
            os.makedirs(user_conf_dir)
        sdcfbuilder.create_credential_file_sample(user_credential_file)
        os.chmod(user_credential_file,0600)

config=sdcfloader.load(configuration_file,credential_file,user_configuration_file,user_credential_file,special_user=is_special_user())

# aliases (indirection to ease configuration parameter access)
openid=config.get('esgf_credential','openid')
password=config.get('esgf_credential','password')
progress=config.getboolean('interface','progress')
download=config.getboolean('module','download')

default_folder=get_path('default_path',default_folder_default_path)
selection_folder=get_path('selection_path',default_selection_folder)
db_folder=get_path('db_path',default_db_folder)
data_folder=get_path('data_path',default_data_folder)
sandbox_folder=get_path('sandbox_path',default_sandbox_folder)
bin_folder="%s/bin"%root_folder

data_download_script_http="%s/sdget.sh"%bin_folder
data_download_script_gridftp="%s/sdgetg.sh"%bin_folder

logon_script="%s/sdlogon.sh"%bin_folder
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

# Note
#     When set to xml, 'lxml' package is required (must be added both in install.sh and in requirements.txt)
searchapi_output_format=sdconst.SEARCH_API_OUTPUT_FORMAT_JSON

# if set to True, automatically switch to the next url if error occurs (e.g. move from gridftp url to http url)
next_url_on_error=config.getboolean('download','http_fallback')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',default=None,help='Name of the parameter to be displayed (if not set, all parameters are displayed)')
    args = parser.parse_args()

    print_(args.name)
