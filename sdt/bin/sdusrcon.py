#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains sdtc user commands.

Note
    'sdusrcon' stands for "SynDa USeR CONsole".
"""

import re
from tabulate import tabulate
import sdapp
from sdtypes import File
from sdbasecon import BaseConsole
from sdexception import SDException
import sdquicksearch
import sddao
import sdfiledao
import sdenqueue
import sdconst
import sdldataset
import sdrdataset
import sdlfile
import sdrfile
import sddeletefile
import sdparam
import sdreport
import sdi18n
import sddeferredafter
import sdsessionparam
import sddaemon
import sdlock
import sdconfig
import sdremoteparam
from sdconsoleutils import ConsoleUtils
from sdshortcut import Shortcut

class UserConsole(BaseConsole,ConsoleUtils,Shortcut):
    intro='Synda User console\nType help for a list of supported commands.\n\n%s\n'%sddaemon.get_daemon_status()
    prompt='sd> '

    def default(self,arg):
        """
        This func add support to automatically list available parameters, depending on
        which facets are currently selected.
        """
        if sdparam.exists_parameter_name(arg):

            selected_facets=sdsessionparam.get_session_facets_as_facetsgroup()
            if len(selected_facets)>0:
                # facet selected: retrieve parameters from ESGF

                params=sdremoteparam.run(pname=arg,facets_group=selected_facets,dry_run=True)
                # TODO: func for code below
                items=params.get(arg,[])
                for item in items:
                    print item.name

            else:
                # no facet selected: retrieve parameters from cache

                sdparam.main(arg.split()) # tricks to re-use sdparam CLI parser

        else:
            print '*** Unknown command: %s'%arg

    # below this line is functional code

    parameter=None

    def do_lock(self,arg):
        if arg=='':
            return

        model=arg

        try:
            sdlock.lock(model)
        except SDException,e:
            sdtools.print_stderr("Lock error: '%s' model not found on %s"%(model,sdindex.get_default_index()))

    def do_unlock(self,arg):
        model=arg
        sdlock.unlock(model)

    def do_admin(self,arg):
        from sdadmcon import AdminConsole
        AdminConsole().cmdloop()

    def do_param(self,arg):
        sdparam.main(arg.split()) # tricks to re-use sdparam CLI parser

    def do_config(self,arg):
        arg=None if arg=='' else arg # set None if empty
        sdconfig.print_(arg)

    def do_add(self,file):
        self.parameter=["limit=1","instance_id=%s"%file]
        self.complete_parameter()
        result=sdquicksearch.run(parameter=self.parameter)
        if len(result.files)==1:
            f=result.files[0]
            if f['status']==sdconst.TRANSFER_STATUS_NEW:
                sdenqueue.run(result.files)
                print "File successfully enqueued"
            else:
                print "File already enqueued"
        elif len(result.files)==0:
            print "File not found"

    def do_delete(self,file):
        files=sdfiledao.get_files(file_functional_id=file,limit=1)
        if len(files)==1:
            f=files[0]
            sddeletefile.immediate_delete(f)
            print "File successfully deleted"
        elif len(files)==0:
            print "File not found"

    def do_search(self,arg):
        self.parameter=arg.split()
        self.complete_parameter()

        localsearch=sdsessionparam.get_value('localsearch')
        dry_run=sdsessionparam.get_value('dry_run')
        
        type_=sdsessionparam.get_value('type')

        kw={'parameter':self.parameter,'dry_run':dry_run}

        if localsearch:
            if type_=='Dataset':
                datasets=sdldataset.get_datasets(**kw)
                if not dry_run:
                    if len(datasets)==0:
                        print "Dataset not found"
                    else:
                        sdldataset.print_list(datasets)
            elif type_=='File':
                files=sdlfile.get_files(**kw)
                if not dry_run:
                    sdlfile.print_(files)
        else:
            if type_=='Dataset':
                datasets=sdrdataset.get_datasets(**kw)
                if not dry_run:
                    if len(datasets)==0:
                        print "Dataset not found"
                    else:
                        sdrdataset.print_list(datasets)
            elif type_=='File':
                files=sdrfile.get_files(**kw)
                if not dry_run:
                    sdrfile.print_list(files)

    def do_unset(self,arg):
        sdsessionparam.remove_session_param(arg)

    def do_set(self,arg):
        if arg=='all':
            sdsessionparam.print_session_params()
        elif arg=='option':
            sdsessionparam.print_options()
        elif arg=='facet':
            sdsessionparam.print_search_api_facets()
        elif arg=='':
            sdsessionparam.print_modified_session_params()
        elif arg.endswith('?'):
            name=re.sub('\?$','',arg)
            sdsessionparam.print_session_param(name)
        elif arg=='default':
            sdsessionparam.set_default()
        else:
            if '=' in arg:
                pname,pvalue=arg.split('=')
                sdsessionparam.set(pname,pvalue)

    def help_lock(self):
        print sdi18n.m0006('','')
    def help_unlock(self):
        print sdi18n.m0006('','')
    def help_daemon(self):
        print sdi18n.m0006('daemon <action>','Start/stop daemon',example=sdi18n.m0012)
    def help_version(self):
        print sdi18n.m0006('version','Print Synda version')
    def help_run(self):
        print sdi18n.m0006('run','Print running transfers.')
    def help_config(self):
        print sdi18n.m0006('config [ name ]','Print configuration parameter.')
    def help_status(self):
        print sdi18n.m0006('status [ project ]','Print download status.')
    def help_add(self):
        print sdi18n.m0006('add <file>','Add files in download queue.',example=sdi18n.m0008,note=sdi18n.m0009)
    def help_delete(self):
        print sdi18n.m0006('delete <file>','Delete file from local repository',example=sdi18n.m0007)
    def help_quit(self):
        print sdi18n.m0006('quit','Leave Synda console.')
    def help_unset(self):
        print sdi18n.m0006('unset name','Unset session parameter.')
    def help_set(self):
        print sdi18n.m0006('set [ name? | name=value | all | option | facet | default ]','Set session parameter.',example=sdi18n.m0011)
    def help_param(self):
        print sdi18n.m0006('param [ facet_name | pattern ] [ pattern ]','List ESGF facets',example=sdi18n.m0004('param'))
    def help_search(self):
        print sdi18n.m0006('search [FILTER]... [ limit ]','Search file(s)',example=sdi18n.m0002('search'),note=sdi18n.m0005)
    def help_admin(self):
        print sdi18n.m0006('admin',"Switch to 'admin' mode")

# init.
