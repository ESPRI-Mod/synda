#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains type insensitive action used by 'synda' script.

Note
    In this file, module import directives are moved near the calls,
    so to improve startup time.
"""

import sys
from sdtools import print_stderr
from sdexception import SDException,EmptySelectionException

def autoremove(args):
    import sddeletedataset
    sddeletedataset.remove_old_versions_datasets(dry_run=args.dry_run)

def certificate(args):
    import sdlogon
    if args.action is None:
        sdlogon.print_certificate()
    else:
        if args.action=="renew":
            if sdlogon.is_openid_set():
                try:
                    sdlogon.renew_certificate(True,quiet=False,debug=False,force_renew_ca_certificates=args.force_renew_ca_certificates)
                    print_stderr('Certificate successfully renewed.')   
                except Exception,e:
                    print_stderr('Error occurs while renewing certificate (%s)'%str(e))
            else:
                print_stderr('Error: OpenID not set in configuration file.')   
        elif args.action=="print":
            sdlogon.print_certificate()
        else:
            print_stderr('Not implemented yet.')   

def contact(args):
    import sdi18n
    print sdi18n.m0018

def daemon(args):
    import sddaemon,sdconfig

    if args.action is None:
        sddaemon.print_daemon_status()
    else:
        if args.action=="start":

            if sdconfig.multiuser:
                print_stderr("Daemon must be started using 'systemctl' command")
                return 1

            if sddaemon.is_running():
                print_stderr("Daemon already started")
            else:
                try:
                    sddaemon.start()
                    print_stderr("Daemon successfully started")
                except SDException,e:
                    print_stderr('error occured',e.msg)
        elif args.action=="stop":

            if sdconfig.multiuser:
                print_stderr("Daemon must be stopped using 'systemctl' command")
                return 1

            if sddaemon.is_running():
                try:
                    sddaemon.stop()
                    print_stderr("Daemon successfully stopped")
                except SDException,e:
                    print_stderr('error occured',e.msg)
            else:
                print_stderr("Daemon already stopped")
        elif args.action=="status":
            sddaemon.print_daemon_status()

def facet(args):
    import sdparam,sdremoteparam,syndautils,sdinference

    facets_groups=syndautils.get_stream(args)
    facets_groups=sdinference.run(facets_groups)


    if sdparam.exists_parameter_name(args.facet_name): # first, we check in cache so to quickly return if facet is unknown

        if len(facets_groups)==1:
            # facet selected: retrieve parameters from ESGF

            facets_group=facets_groups[0]

            params=sdremoteparam.run(pname=args.facet_name,facets_group=facets_group,dry_run=args.dry_run)

            # TODO: func for code below
            items=params.get(args.facet_name,[])
            for item in items:
                print item.name
        elif len(facets_groups)>1:
            print_stderr('Multi-queries not supported')

        else:
            # Parameter not set. In this case, we retrieve facet value list from cache.

            sdparam.main([args.facet_name]) # tricks to re-use sdparam CLI parser

    else:
        print_stderr('Unknown facet')   

def get(args):
    import sdlogon, sdrfile, sddeferredafter, sddirectdownload, syndautils, humanize, sdconfig, os, sdconst

    if args.verify_checksum and args.network_bandwidth_test:
        print_stderr("'verify_checksum' option cannot be set when 'network_bandwidth_test' option is set.")
        return 1

    stream=syndautils.get_stream(args)

    sdlogon.renew_certificate(False)

    http_client=sdconst.HTTP_CLIENT_URLLIB if args.urllib2 else sdconst.HTTP_CLIENT_WGET

    # local_path
    #
    # 'synda get' subcommand currently force local_path to the following construct:
    # '<dest_folder>/<filename>' (i.e. you can't use DRS tree in-between). This may
    # change in the future.
    #
    local_path_prefix=args.dest_folder

    # BEWARE
    #
    # when set in CLI parameter, url is usually an ESGF facet, and as so should
    # be sent to the search-api as other facets
    # BUT
    # we want a special behaviour here (i.e. with 'synda get' command) with url:
    # if url is set by user, we DON'T call search-api operator. Instead, we
    # download the url directly.

    urls=syndautils.get_facet_values_early(stream,'url')
    if len(urls)==0:
        # no url in stream: switch to search-api operator mode

        sddeferredafter.add_default_parameter(stream,'limit',5)
        sddeferredafter.add_forced_parameter(stream,'local_path_format','notree')

        files=sdrfile.get_files(stream=stream,post_pipeline_mode='file',dry_run=args.dry_run) # yes: this is the second time we run sdinference filter, but it doesn't hurt as sdinference is idempotent

        if not args.dry_run:
            if len(files)>0:

                # compute metric
                total_size=sum(int(f['size']) for f in files)
                total_size=humanize.naturalsize(total_size,gnu=False)

                print_stderr('%i file(s) will be downloaded for a total size of %s.'%(len(files),total_size))

                status=sddirectdownload.run(files,
                                            args.timeout,
                                            args.force,
                                            http_client,
                                            local_path_prefix,
                                            verify_checksum=args.verify_checksum,
                                            network_bandwidth_test=args.network_bandwidth_test,
                                            debug=True,
                                            verbosity=args.verbosity,
                                            show_progress=True,
                                            hpss=args.hpss)

                if status!=0:
                    return 1

            else:
                print_stderr("File not found")
                return 1
        else:
            for f in files:
                size=humanize.naturalsize(f['size'],gnu=False)
                print '%-12s %s'%(size,f['filename'])

    elif len(urls)>0:
        # url(s) found in stream: search-api operator not needed (download url directly)

        if args.verify_checksum:
            print_stderr("To perform checksum verification, ESGF file identifier (e.g. title, id, tracking id..)  must be used instead of file url.")
            return 1

        # TODO: to improve genericity, maybe merge this block into the previous one (i.e. url CAN be used as a search key in the search-api (but not irods url))

        files=[]
        for url in urls:

            filename=os.path.basename(url)
            local_path=filename

            f=dict(local_path=local_path,url=url)

            files.append(f)
            
        status=sddirectdownload.run(files,
                                    args.timeout,
                                    args.force,
                                    http_client,
                                    local_path_prefix,
                                    verify_checksum=args.verify_checksum,
                                    network_bandwidth_test=args.network_bandwidth_test,
                                    debug=True,
                                    verbosity=args.verbosity,
                                    show_progress=True,
                                    hpss=args.hpss)

        if status!=0:
            return 1

    else:
        assert False

    return 0

def history(args):
    import sddao
    from tabulate import tabulate
    li=[d.values() for d in sddao.get_history_lines()] # listofdict to listoflist
    print tabulate(li,headers=['action','selection source','date','insertion_group_id'],tablefmt="orgtbl")

def install(args):
    (status,newly_installed_files_count)=install_helper(args)

    return status

def install_helper(args,files=None):
    """
    Returns
        number of newly installed files
    """
    import syndautils, sddaemon

    syndautils.check_daemon()

    if files is None:

        try:
            files=syndautils.file_full_search(args)
        except EmptySelectionException, e:
            print 'No packages will be installed, upgraded, or removed.'
            sys.exit(0)

    # in dry-run mode, we stop here
    if args.dry_run:
        return (0,0)

    interactive=not args.yes

    # Compute total files stat
    count_total=len(files)
    size_total=sum(int(f['size']) for f in files)


    # Compute new files stat
    #
    # (yes, block below is a duplicate of what is done inside sdenqueue.run()
    # method, but safer to keep it there too, and should be no harm in term of
    # perfomance)
    #
    import sdsimplefilter, sdconst
    files=sdsimplefilter.run(files,'status',sdconst.TRANSFER_STATUS_NEW,'keep')
    count_new=len(files)
    size_new=sum(int(f['size']) for f in files)


    # what to do if no match
    if count_new<1:

        if interactive:
            if count_total>0:
                print_stderr("Nothing to install (matching files are already installed or waiting in the download queue). To monitor transfers status and progress, use 'synda queue' command.")
            else:
                print_stderr('Nothing to install (0 file found).')

        return (0,0)

    # ask user for confirmation
    if interactive:
        import humanize
        print_stderr('%i file(s) will be added to the download queue.'%count_new)
        print_stderr('Once downloaded, %s of additional disk space will be used.'%humanize.naturalsize(size_new,gnu=False))

        import sdutils
        if sdutils.query_yes_no('Do you want to continue?', default="yes"):
            installation_confirmed=True
        else:
            installation_confirmed=False
    else:
        installation_confirmed=True


    # install
    if installation_confirmed:
        import sdenqueue
        sdenqueue.run(files)

        if interactive:
            print_stderr("%i file(s) enqueued"%count_new)
            print_stderr("You can follow the download using 'synda watch' and 'synda queue' commands")

            if not sddaemon.is_running():
                print_stderr("The daemon is not running. To start it, use 'sudo service synda start'.")
    else:
        if interactive:
            print_stderr('Abort.')

    return (0,count_new)

def intro(args):
    import sdi18n
    print sdi18n.m0019

def metric(args):
    import sdmetric,sdparam

    # check
    if args.groupby=='model':
        if args.project not in sdparam.params['project']:
            print_stderr("Unknown project (%s)"%args.project)
            return 1

    if args.metric=='size':
        sdmetric.print_size(args.groupby,args.project)
    elif args.metric=='rate':
        sdmetric.print_rate(args.groupby,args.project)

def remove(args):
    import sddelete,sddeletefile,syndautils

    syndautils.check_daemon()

    try:
        files=syndautils.file_full_search(args)
    except EmptySelectionException, e:
        print 'No packages will be installed, upgraded, or removed.'
        sys.exit(0)

    if not args.dry_run:
        import humanize, sdsimplefilter, sdconst, sdutils, sdoperation, sddeletedataset

        # Compute deleted stat for files
        files=sdsimplefilter.run(files,'status',sdconst.TRANSFER_STATUS_NEW,'remove')
        files=sdsimplefilter.run(files,'status',sdconst.TRANSFER_STATUS_DELETE,'remove') # maybe not needed as we do immediate delete from now...
        count_delete=len(files)
        size_delete=sum(int(f['size']) for f in files if f['status']==sdconst.TRANSFER_STATUS_DONE)

        if count_delete>0:

            print_stderr('%i file(s) will be removed.'%count_delete)
            print_stderr('After this operation, %s of disk space will be freed.'%humanize.naturalsize(size_delete,gnu=False))

            if sdutils.query_yes_no('Do you want to continue?', default="no"):

                # first step, change the files status from 'done' to 'delete' (update metadata)
                nbr=sddelete.run(files)
                print_stderr("%i file(s) removed"%nbr)

                # second step, do the deletion (remove files on filesystem and remove files metadata)
                # (to do a deferred deletion (i.e. by the daemon), comment line below)
                sddeletefile.delete_transfers()

                # third step is to remove orphan dataset
                sddeletedataset.purge_orphan_datasets()

                # fourth step is to remove orphan folder.
                sdoperation.cleanup_tree()

            else:
                print_stderr('Abort.')
        else:
            print_stderr('Nothing to delete.')

def reset(args):
    import sddeletefile
    sddeletefile.reset()

def stat(args):
    import syndautils

    try:
        files=syndautils.file_full_search(args)
    except EmptySelectionException, e:
        print "You must specify at least one facet to perform this action."
        sys.exit(0)

    if not args.dry_run:
        import sdstat
        sdstat.run(files)

def selection(args): # don't remove 'args' argument event if not used
    """
    Note
        inter-selection func
    """
    import sdselectionsgroup
    sdselectionsgroup.print_selection_list()

def upgrade(args):
    """
    Note
        inter-selection func
    """
    import sdselectionsgroup, sdparameter, sdsearch


    # BEWARE: tricky statement
    #
    # 'upgrade' is a multi-selections 'subcommand' which do the same as the
    # mono-selection 'install' subcommand, but for many selections.  What we do
    # here is replace 'upgrade' subcommand with 'install' subcommand, so that we can,
    # now that we are in 'upgrade' func/context, 
    # come back to the existing mono-selection func,
    # for each selection, with 'install' subcommand.
    #
    args.subcommand='install'

    project=sdparameter.extract_values_from_parameter(args.parameter,'project') # retrieve project(s) from parameter

    for selection in sdselectionsgroup.get_selection_list(project=project):
        print_stderr("Process %s.."%selection.filename)

        if not args.dry_run:

            # TODO: maybe force type=file here, in case the selection file have 'type=dataset'

            files=sdsearch.run(selection=selection)
            args.yes=True
            (status,newly_installed_files_count)=install_helper(args,files=files)

def replica_next(file_functional_id,args):
    import sdrfile, sdmodify, sdfiledao, sdutils, sdconst

    parameter=['keep_replica=true','nearest=false','file_functional_id=%s'%file_functional_id]
    files=sdrfile.get_files(parameter=parameter,dry_run=args.dry_run)
    if not args.dry_run:
        if len(files)==0:
            print_stderr("File not found in ESGF (file_functional_id=%s)"%file_functional_id)
        else:
            replicas=[(f['url'],f['data_node']) for f in files]

            file_=sdfiledao.get_file(file_functional_id)
            if file_ is not None:

                if sdutils.get_transfer_protocol(file_.url)==sdconst.TRANSFER_PROTOCOL_HTTP:
                    sdmodify.replica_next(file_,replicas)
                else:
                    print_stderr("Incorrect protocol") # only http protocol is supported in 'synda replica' for now

            else:
                print_stderr("Local file not found")

def replica(args):
    if args.action=="next":
        if args.file_id is None:
            import sdfiledao,sdconst
            files=sdfiledao.get_files(status=sdconst.TRANSFER_STATUS_ERROR)
            for file_ in files:
                replica_next(file_.file_functional_id,args)
        else:
            replica_next(args.file_id,args)
    else:
        print_stderr('Incorrect argument')   

def retry(args):
    import sdmodify
    nbr=sdmodify.retry_all()
    if nbr>0:
        print_stderr("%i file(s) marked for retry."%nbr)
    else:
        print_stderr("No transfer in error")

def param(args):
    import sdparam
    sdparam.print_(args)

def queue(args):
    import sdfilequery
    from tabulate import tabulate
    from sdprogress import ProgressThread

    ProgressThread.start(sleep=0.1,running_message='Collecting status information.. ',end_message='') # spinner start
    li=sdfilequery.get_download_status(args.project)
    ProgressThread.stop() # spinner stop

    print tabulate(li,headers=['status','count','size'],tablefmt="plain")
    #sddaemon.print_daemon_status()

def update(args):
    print_stderr("Retrieving parameters from ESGF...")
    import sdcache
    sdcache.run(reload=True,host=args.index_host,project=args.project)
    print_stderr("Parameters are up-to-date.")

def variable(args):
    import sdremoteparam,sdutils,sdproxy_light

    # currently, mode (list or show) is determined by
    # parameter existency. This may change in the future
    # as it may be useful to list variable based on filter
    # (e.g. list variable long name only for obs4MIPs
    # project, etc..). To do that, we will need to 
    # add an 'action' argument (i.e. list and show).
    #
    action='show' if len(args.parameter)>0 else 'list'

    if action=='list':

        if args.long_name:
            facet='variable_long_name'
        elif args.short_name:
            facet='variable'
        elif args.standard_name:
            facet='cf_standard_name'
        else:
            # no options set by user

            facet='variable_long_name' # default
            

        params=sdremoteparam.run(pname=facet,dry_run=args.dry_run)

        if not args.dry_run:

            # This try/except block is to prevent
            # IOError: [Errno 32] Broken pipe
            # Other way to prevent it is to ignore SIGPIPE
            # More info at
            # http://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
            try:

                # TODO: func for code below
                items=params.get(facet)
                for item in items:
                    print item.name

            except:
                pass

    elif action=='show':

        # We do not use inference here, instead we use
        # search-api 'query' feature to do the job.
        #
        query=sdutils.parameter_to_query(args.parameter)
        file_=sdproxy_light.get_one_file(query=query,dry_run=args.dry_run)

        if not args.dry_run:

            if file_ is None:

                print 'Variable not found.'

            else:

                print 'short name:       ',file_['variable'][0]
                print 'standard name:    ',file_['cf_standard_name'][0]
                print 'long name:        ',file_['variable_long_name'][0]
                print 'unit:             ',file_['variable_units'][0]

def watch(args):
    import sdreport, sddaemon

    if sddaemon.is_running():
        sdreport.print_running_transfers()
    else:
        print_stderr('Daemon not running')

# init.

# TODO: rename as subcommands
actions={
    'autoremove':autoremove,
    'certificate':certificate, 
    'contact':contact,
    'daemon':daemon, 
    'facet':facet,
    'get':get,
    'history':history, 
    'install':install, 
    'intro':intro, 
    'metric':metric, 
    'param':param,
    'queue':queue,
    'remove':remove, 
    'replica':replica,
    'reset':reset,
    'retry':retry,
    'selection':selection, 
    'stat':stat, 
    'update':update,
    'upgrade':upgrade,
    'variable':variable,
    'watch':watch
}
