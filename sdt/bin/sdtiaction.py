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

from sdtools import print_stderr
from sdexception import SDException

def autoremove(args):
    import sddeletedataset
    sddeletedataset.remove_old_versions_datasets(dry_run=args.dry_run)

def cache(args):
    if len(args.parameter)==0:
        pass
    else:
        action=args.parameter[0] # it's a naming mess: rename top level action as subcommand
        if action=="init":
            print_stderr("Retrieving parameters from ESGF...")
            import sdcache
            sdcache.run(reload=True)
            print_stderr("Parameters are up-to-date.")

def certificate(args):
    import sdlogon
    if len(args.action)==0:
        sdlogon.print_certificate()
    else:
        if args.action=="renew":

            if sdlogon.is_openid_set():
                try:
                    sdlogon.renew_certificate(True,quiet=False)
                    print_stderr('Certificate successfully renewed.')   
                except Exception,e:
                    print_stderr('Error occurs while renewing certificate (%s)'%str(e))
            else:
                print_stderr('Error: OpenID not set in configuration file.')   
        elif args.action=="print":
            sdlogon.print_certificate()
        else:
            print_stderr('Not implemented yet.')   

def history(args):
    import sddao
    from tabulate import tabulate
    li=[d.values() for d in sddao.get_history_lines()] # listofdict to listoflist
    print tabulate(li,headers=['action','selection source','date','insertion_group_id'],tablefmt="orgtbl")

def install(args,files=None):
    """
    Returns
        number of newly installed files
    """
    import syndautils

    syndautils.check_daemon()

    if files is None:
        files=syndautils.file_full_search(args)

    if args.dry_run:
        return 0

    # TODO
    interactive=not args.non_interactive

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
                print_stderr('Nothing to install (files already installed).')   
            else:
                print_stderr('Nothing to install (0 file found).')

        return 0

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
            print_stderr('You can now start the daemon to begin the download.') # TODO: ask for confirm and do the start here
    else:
        if interactive:
            print_stderr('Abort.')

    return count_new

def remove(args):
    import sddelete,sddeletefile,syndautils

    syndautils.check_daemon()

    files=syndautils.file_full_search(args)

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
    files=syndautils.file_full_search(args)

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
    # 'upgrade' is a multi-selections 'action' which do the same as the
    # mono-selection 'install' action, but for many selections.  What we do
    # here is replace 'upgrade' action with 'install' action, so that we can,
    # now that we are in 'upgrade' func/context, 
    # come back to the existing mono-selection func (i.e. execute_x_action() func),
    # for each selection, with 'install' action.
    #
    args.action='install'

    project=sdparameter.extract_values_from_parameter(args.parameter,'project') # retrieve project(s) from parameter

    for selection in sdselectionsgroup.get_selection_list(project=project):
        print_stderr("Process %s.."%selection.filename)

        if not args.dry_run:

            # TODO: maybe force type=file here, in case the selection file have 'type=dataset'

            files=sdsearch.run(selection=selection)
            args.non_interactive=True
            install(args,files=files)

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
    if len(args.parameter)<1:
        print_stderr('Incorrect argument')   
    else:
        action=args.parameter[0] # it's a naming mess: rename top level action as subcommand
        if action=="next":
            if len(args.parameter)==1:
                import sdfiledao,sdconst
                files=sdfiledao.get_files(status=sdconst.TRANSFER_STATUS_ERROR)
                for file_ in files:
                    replica_next(file_.file_functional_id,args)
            elif len(args.parameter)==2:
                file_functional_id=args.parameter[1]
                replica_next(file_functional_id,args)

def retry(args):
    import sdmodify
    nbr=sdmodify.retry_all()
    if nbr>0:
        print_stderr("%i file(s) marked for retry."%nbr)
    else:
        print_stderr("No transfer in error")

def daemon(args):
    import sddaemon

    if len(args.parameter)==0:
        sddaemon.print_daemon_status()
    else:
        action=args.parameter[0] # it's a naming mess: rename top level action as subcommand
        if action=="start":
            if sddaemon.is_running():
                print_stderr("Daemon already started")
            else:
                try:
                    sddaemon.start()
                    print_stderr("Daemon successfully started")
                except SDException,e:
                    print_stderr('error occured',e.msg)
        elif action=="stop":
            if sddaemon.is_running():
                try:
                    sddaemon.stop()
                    print_stderr("Daemon successfully stopped")
                except SDException,e:
                    print_stderr('error occured',e.msg)
            else:
                print_stderr("Daemon already stopped")
        elif action=="status":
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
            sdparam.main([args.facet_name]) # tricks to re-use sdparam CLI parser

    else:
        print_stderr('Unknown facet')   

def param(args):
    import sdparam
    sdparam.main(args.parameter) # tricks to re-use sdparam CLI parser

def queue(args):
    import sdstatquery
    from tabulate import tabulate
    from sdprogress import ProgressThread

    project=args.parameter[0] if not (len(args.parameter)==0) else None

    ProgressThread.start(sleep=0.1,running_message='Collecting status information.. ',end_message='') # spinner start
    li=sdstatquery.get_download_status(project)
    ProgressThread.stop() # spinner stop

    print tabulate(li,headers=['status','count','size'],tablefmt="plain")
    #sddaemon.print_daemon_status()

def test(args):
    import os,sdlogon,sdget

    sdlogon.renew_certificate(False)

    if len(args.parameter)==0:
        print_stderr('Incorrect argument')   
    else:
        file_url=args.parameter[0] # it's a naming mess: rename top level action as subcommand

        tmpfile='/tmp/sdt_test_file.nc'

        if os.path.isfile(tmpfile):
            os.remove(tmpfile)

        (sdget_status,local_checksum,killed,script_stdxxx)=sdget.download(file_url,tmpfile)

        print_stderr(script_stdxxx)

        #print_stderr("'Exit code: %i"%sdget_status)

        """
        if sdget_status==0:
            print_stderr('file location: %s'%tmpfile)
        """

def watch(args):
    import sdreport, sddaemon

    if sddaemon.is_running():
        sdreport.print_running_transfers()
    else:
        print_stderr('Daemon not running')

def update(args):
    print_stderr('Not implemented yet.')   

# init.

actions={
    'autoremove':autoremove,
    'cache':cache,
    'certificate':certificate, 
    'daemon':daemon, 
    'facet':facet,
    'history':history, 
    'install':install, 
    'param':param,
    'queue':queue,
    'remove':remove, 
    'replica':replica,
    'reset':reset,
    'retry':retry,
    'selection':selection, 
    'stat':stat, 
    'test':test,
    'update':update,
    'upgrade':upgrade,
    'watch':watch
}
