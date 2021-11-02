#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from synda.sdt.sdtools import print_stderr
from synda.sdt import sdexception

from synda.source.config.file.certificate.x509.models import Config as SecurityFile
from synda.source.config.path.tree.certificate.x509.models import Config as SecurityPath
from synda.source.config.file.user.credentials.models import Config as Credentials

from synda.source.config.process.download.constants import get_http_clients
from synda.source.config.process.download.constants import TRANSFER
from synda.source.config.process.download.constants import get_transfer_protocol
from synda.source.process.env.manager import Manager


def autoremove(args):
    from synda.sdt import sddeletedataset,sddeletefile
    sddeletedataset.remove_old_versions_datasets(dry_run=args.dry_run)
    sddeletefile.delete_transfers_lowmem()

def certificate(args):
    from synda.sdt import sdlogon
    if args.action is None:
        sdlogon.print_certificate()
        return 0
    else:
        if args.action=="renew":

            # retrieve openid and passwd
            if args.openid and args.password:
                # use credential from CLI

                oid=args.openid
                pwd=args.password
            else:
                # use credential from file
                credentials = args.authority.get_user_credentials()
                if credentials.is_openid_set():
                    oid = credentials.openid
                    pwd = credentials.password
                else:
                    credential_file = Credentials().get()
                    print_stderr('Error: OpenID not set in configuration file (%s).' % credential_file)
                    return 1

            # retrieve certificate
            try:
                sdlogon.renew_certificate(oid,pwd,force_renew_certificate=True,force_renew_ca_certificates=args.force_renew_ca_certificates)
                print_stderr('Certificate successfully renewed.')
                return 0
            except Exception as e:
                print_stderr('Error occurs while renewing certificate (%s)'%str(e))
                return 1
        elif args.action=="info":
            esgf_x509_cert_dir = SecurityPath().get_certificates()
            print('ESGF CA certificates location: {}'.format(esgf_x509_cert_dir))

            esgf_x509_proxy = SecurityFile().get_credentials()
            print('ESGF user certificate location: {}'.format(esgf_x509_proxy))
            return 0
        elif args.action=="print":
            sdlogon.print_certificate()
            return 0
        else:
            print_stderr('Not implemented yet.')   
            return 1

def check(args):
    from synda.sdt import sddump,sdcheckdatasetversion,sdfields

    status=0

    if args.action is None:
        print_stderr('Please specify a check to perform.')
        status=1

    elif args.action=="selection":
        from synda.sdt import sdselectionsgroup,sdpipeline

        for selection in sdselectionsgroup.get_selection_list():
            try:
                print_stderr("Checking %s.."%selection.filename)
                sdpipeline.prepare_param(selection=selection)
            except sdexception.IncorrectParameterException as e:
                print_stderr("Error occurs while processing %s (%s)"%(selection.filename,str(e)))

    elif args.action=="file_variable":

        #subset_filter=['model=HadCM3','project=CMIP5','experiment=historical','realm=atmos']
        #subset_filter=['model=HadCM3','project=CMIP5']
        #subset_filter=['project=CMIP5']

        #subset_filter=['time_frequency=day','model=EC-EARTH','project=CMIP5','experiment=rcp85','realm=atmos']

        subset_filter=['model=CNRM-CM5','project=specs','realm=atmos','variable=tas']
        #subset_filter=['project=specs']

        files=sddump.dump_ESGF(parameter=subset_filter,fields=sdfields.get_file_variable_fields(),dry_run=args.dry_run,type_='File')

        if not args.dry_run:
            print('%i file(s) retrieved'%len(files))

            errors=0
            for file_ in files:

                # debug
                #print(file_['variable'])

                if len(file_['variable'])>1:
                    print('File contains many variables (%s,%s)'%(file_['title'],str(file_['variable'])))
                    errors+=1

            if errors==0:
                print('No inconsistency detected')
            else:
                print('%d inconsistencies detected'%errors)

    elif args.action=="dataset_version":
        status=sdcheckdatasetversion.run(args)

    else:
        print_stderr('Invalid check "%s"'%args.action)
        status=1

    return status

def config(args):
    from synda.sdt import sdconfig
    if args.action is None:
        sdconfig.print_()
    else:
        if args.action=='get':
            sdconfig.print_(args.name)
        elif args.action=='set':
            # TODO see if section can be added to the argparser arguments.
            print('Feature not implemented yet.')


def contact(args):
    from synda.sdt import sdi18n
    print(sdi18n.m0018)


def download(args):
    from synda.source.process.subcommand.download.models import Process as DownloadProcess

    status = DownloadProcess().run(args)

    return status


def facet(args):
    from synda.sdt import sdparam,sdremoteparam,syndautils,sdinference,sdignorecase

    facets_groups=syndautils.get_stream(subcommand=args.subcommand,parameter=args.parameter,selection_file=args.selection_file,no_default=True)
    facets_groups=sdignorecase.run(facets_groups)
    facets_groups=sdinference.run(facets_groups, show_infere_parameter_name_info_message=False)


    if sdparam.exists_parameter_name(args.facet_name): # first, we check in cache so to quickly return if facet is unknown

        if len(facets_groups)==1:
            # facet selected: retrieve parameters from ESGF

            facets_group=facets_groups[0]

            params=sdremoteparam.run(pname=args.facet_name,facets_group=facets_group,dry_run=args.dry_run)

            # TODO: func for code below
            items=params.get(args.facet_name,[])
            for item in items:
                print(item.name)
        elif len(facets_groups)>1:
            print_stderr('Multi-queries not supported')

        else:
            # Parameter not set. In this case, we retrieve facet values list from cache.

            sdparam.main([args.facet_name]) # tricks to re-use sdparam CLI parser

    else:
        print_stderr('Unknown facet')   


def get(args):

    from synda.sdt import sdlogon
    from synda.sdt import sdrfile
    from synda.sdt import sddeferredafter
    from synda.sdt import sddirectdownload
    from synda.sdt import syndautils
    import humanize
    import os
    from synda.sdt import sdearlystreamutils

    # hack
    # see TAG43534FSFS
    if args.quiet:
        args.verbosity = 0

    if args.verify_checksum and args.network_bandwidth_test:
        print_stderr("'verify_checksum' option cannot be set when 'network_bandwidth_test' option is set.")
        return 1

    stream = syndautils.get_stream(
        subcommand=args.subcommand,
        parameter=args.parameter,
        selection_file=args.selection_file,
    )

    if args.openid and args.password:
        # use credential from CLI

        oid = args.openid
        pwd = args.password
    else:
        # use credential from file
        credentials = args.authority.get_user_credentials()
        if credentials.is_openid_set():
            oid = credentials.openid
            pwd = credentials.password
        else:
            credential_file = Credentials().get()
            print_stderr(
                'Error: OpenID not set in configuration file (%s).'.format(
                    credential_file,
                ),
            )

            return 1

    # retrieve certificate
    sdlogon.renew_certificate(
        oid,
        pwd,
        force_renew_certificate=False,
    )

    http_client = get_http_clients()["urllib"] if args.urllib else get_http_clients()["wget"]

    # local_path
    #
    # 'synda get' subcommand currently force local_path to the following construct:
    # '<dest_folder>/<filename>' (i.e. you can't use DRS tree in-between). This may
    # change in the future.
    #
    if args.dest_folder is None:
        # current working directory
        local_path_prefix = os.getcwd()
    else:
        local_path_prefix = args.dest_folder

    # BEWARE
    #
    # when set in CLI parameter, url is usually an ESGF facet, and as so should
    # be sent to the search-api as other facets
    # BUT
    # we want a special behaviour here (i.e. with 'synda get' command) with url:
    # if url is set by user, we DON'T call search-api operator. Instead, we
    # download the url directly.

    urls = sdearlystreamutils.get_facet_values_early(stream, 'url')

    if len(urls) == 0:
        # no url in stream: switch to search-api operator mode

        sddeferredafter.add_default_parameter(stream, 'limit', 5)
        sddeferredafter.add_forced_parameter(stream, 'local_path_format', 'notree')

        # yes: this is the second time we run sdinference filter, but it doesn't hurt as sdinference is idempotent
        files = sdrfile.get_files(
            stream=stream,
            post_pipeline_mode='file',
            dry_run=args.dry_run,
        )

        if not args.dry_run:
            if len(files) > 0:

                # compute metric
                total_size = sum(int(f['size']) for f in files)
                total_size = humanize.naturalsize(total_size, gnu=False)

                print_stderr(
                    '{} file(s) will be downloaded for a total size of {}.'.format(
                        len(files),
                        total_size,
                    ),
                )

                status = \
                    sddirectdownload.run(
                        files,
                        args.config_manager,
                        timeout=args.timeout,
                        force=args.force,
                        http_client=http_client,
                        local_path_prefix=local_path_prefix,
                        verify_checksum=args.verify_checksum,
                        network_bandwidth_test=args.network_bandwidth_test,
                        debug=True,
                        verbosity=args.verbosity,
                        buffered=False,
                        hpss=args.hpss,
                    )

                if status != 0:
                    return 1

            else:
                print_stderr("File not found")
                return 1
        else:
            for f in files:
                size = humanize.naturalsize(f['size'], gnu=False)
                print(
                    '%-12s %s'.format(
                        size,
                        f['filename'],
                    ),
                )

    elif len(urls) > 0:

        # url(s) found in stream: search-api operator not needed (download url directly)

        # TAGDSFDF432F
        if args.verify_checksum:
            print_stderr(
                "To perform checksum verification, "
                "ESGF file identifier (e.g. title, id, tracking id..)  must be used instead of file url.",
            )
            return 1

        # TODO: to improve genericity, maybe merge this block into the previous one (i.e.
        # TODO: url CAN be used as a search key in the search-api (but not irods url))

        files = []
        for url in urls:

            filename = os.path.basename(url)
            local_path = filename

            f = dict(local_path=local_path, url=url)

            files.append(f)
            
        status = \
            sddirectdownload.run(
                files,
                args.config_manager,
                timeout=args.timeout,
                force=args.force,
                http_client=http_client,
                local_path_prefix=local_path_prefix,
                # see above at TAGDSFDF432F
                verify_checksum=args.verify_checksum,
                network_bandwidth_test=args.network_bandwidth_test,
                debug=True,
                verbosity=args.verbosity,
                buffered=False,
                hpss=args.hpss,
            )

        if status != 0:
            return 1

    else:
        assert False

    return 0


def getinfo(args):
    from synda.source.process.subcommand.getinfo.models import Process as GetInfoProcess

    status = GetInfoProcess().run(args)

    return status


def history(args):
    from synda.sdt import sdhistorydao
    from tabulate import tabulate
    li = [list(d.values()) for d in sdhistorydao.get_all_history_lines()]  # listofdict to listoflist
    print(tabulate(li,headers=['action','selection source','date','insertion_group_id'],tablefmt="orgtbl"))


def install(args):
    from synda.source.process.subcommand.install.models import Process as InstallProcess

    status = InstallProcess().run(args)

    return status


def intro(args):
    from synda.sdt import sdi18n
    print(sdi18n.m0019)


def metric(args):
    from synda.sdt import sdmetric,sdparam

    # check
    if args.groupby=='model':
        if args.project not in sdparam.params['project']:
            print_stderr("Unknown project (%s)"%args.project)
            return 1

    if args.metric=='size':
        sdmetric.print_size(args.groupby,args.project,dry_run=args.dry_run)
    elif args.metric=='rate':
        sdmetric.print_rate(args.groupby,args.project,dry_run=args.dry_run)


def remove(args):
    from synda.sdt import sdremove, syndautils

    stream = syndautils.get_stream(
        subcommand=args.subcommand,
        parameter=args.parameter,
        selection_file=args.selection_file,
        no_default=args.no_default,
        raise_exception_if_empty=True,
    )

    return sdremove.run(args, stream)


def reset(args):
    from synda.sdt import sddeletefile
    sddeletefile.reset()

def stat(args):
    from synda.sdt import sdstat
    return sdstat.run(args)


# don't remove 'args' argument event if not used
def selection(args):
    """
    Note
        inter-selection func
    """
    from synda.sdt import sdselectionsgroup
    sdselectionsgroup.print_selection_list()


def upgrade(args):
    """
    Note
        inter-selection func
    """
    from synda.sdt import sdselectionsgroup, sdparameter, sdupgrade

    project=sdparameter.extract_values_from_parameter(args.parameter,'project') # retrieve project(s) from parameter
    selections=sdselectionsgroup.get_selection_list(project=project)
    sdupgrade.run(selections,args)

def replica_next(file_functional_id,args):
    from synda.sdt import sdrfile, sdmodify, sdfiledao, sdutils

    parameter=['keep_replica=true','nearest=false','file_functional_id=%s'%file_functional_id]
    files=sdrfile.get_files(parameter=parameter,dry_run=args.dry_run)
    if not args.dry_run:
        if len(files)==0:
            print_stderr("File not found in ESGF (file_functional_id=%s)"%file_functional_id)
        else:
            replicas=[(f['url'],f['data_node']) for f in files]

            file_=sdfiledao.get_file(file_functional_id)
            if file_ is not None:

                if sdutils.get_transfer_protocol(file_.url)==get_transfer_protocol():
                    sdmodify.replica_next(file_,replicas)
                else:
                    print_stderr("Incorrect protocol") # only http protocol is supported in 'synda replica' for now

            else:
                print_stderr("Local file not found")

def replica(args):
    if args.action=="next":
        if args.file_id is None:
            from synda.sdt import sdfiledao,sdconst
            files=sdfiledao.get_files(status=TRANSFER["status"]['error'])
            for file_ in files:
                replica_next(file_.file_functional_id,args)
        else:
            replica_next(args.file_id,args)
    else:
        print_stderr('Incorrect argument')   


def retry(args):
    from synda.sdt import sdmodify
    nbr = sdmodify.retry_all(query_filter=args.where)
    if nbr > 0:
        print_stderr("%i file(s) marked for retry." % nbr)
    else:
        print_stderr("No transfer in error")


def param(args):
    from synda.sdt import sdparam
    sdparam.print_(args)


def update(args):
    print_stderr("Retrieving parameters from ESGF...")
    from synda.sdt import sdcache
    sdcache.run(reload=True,host=args.index_host,project=args.project)
    print_stderr("Parameters are up-to-date.")

def variable(args):
    from synda.sdt import sdremoteparam,sdutils,sdproxy_ra

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
                    print(item.name)

            except:
                pass

    elif action=='show':

        # We do not use inference here, instead we use
        # search-api 'query' feature to do the job.
        #
        query=sdutils.parameter_to_query(args.parameter)
        file_=sdproxy_ra.get_one_file(query=query,dry_run=args.dry_run)

        if not args.dry_run:

            if file_ is None:

                print('Variable not found.')

            else:

                print('short name:       ',file_['variable'][0])
                print('standard name:    ',file_['cf_standard_name'][0])
                print('long name:        ',file_['variable_long_name'][0])
                print('unit:             ',file_['variable_units'][0])


def checkenv(args):
    env_manager = Manager()
    env_manager.check(interactive_mode=True)


# init.
def initenv(args):
    """
    should find the tar data.tar.bz and untar it
    should find the tar data.tar.bz and untar it
    :param args:
    :return:
    """
    env_manager = Manager()
    env_manager.init(interactive_mode=True)


# TODO: rename as subcommands
actions = {
    'autoremove': autoremove,
    'certificate': certificate,
    'check': check,
    'config': config,
    'contact': contact,
    'download': download,
    'facet': facet,
    'get': get,
    'getinfo': getinfo,
    'history': history,
    'install': install,
    'intro': intro,
    'metric': metric,
    'param': param,
    'remove': remove,
    'replica': replica,
    'reset': reset,
    'retry': retry,
    'selection': selection,
    'stat': stat,
    'update': update,
    'upgrade': upgrade,
    'variable': variable,
    'check-env': checkenv,
    'init-env': initenv,
}
