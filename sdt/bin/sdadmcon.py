#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdadmcon.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""syndac command (REPL front-end).

Note
    'sdadmcon' stands for "Synchro-Data ADMin CONsole".
"""

import argparse
from sdbasecon import BaseConsole
import sdtools
import sdselection
import sdselectionsgroup
import sdquicksearch
import sddao
import sdfiledao
import sdconst
import sdextractremoteinfos
import sdoperation
import sddeletedataset
import sdi18n
import sdsessionparam
import sdmodify
import sdtest
import sdremoteparam
import sddeletefile
import sdconfig
from tabulate import tabulate

class AdminConsole(BaseConsole):
    intro='Synchro-data Admin console\nType help for a list of supported commands.\n'
    prompt='sda> '

    def do_retry(self,arg):
        if arg=='all':
            nbr=sdmodify.retry_all()
            if nbr>0:
                print "%i file(s) marked for retry."%nbr
        else:
            file=sdfiledao.get_file(arg)
            if file is not None:
                if file.status == sdconst.TRANSFER_STATUS_ERROR:
                    file.status=sdconst.TRANSFER_STATUS_WAITING
                    sdfiledao.update_file(file)
                    print "File marked for retry"
                else:
                    print "Retry failed (only file with error status can be retried)."
            else:
                print "File not found"

    def do_benchmark(self,arg):
        sdtest.test_index_hosts()

    def do_sample(self,arg):
        parser = argparse.ArgumentParser(add_help=False) 
        parser.add_argument('project', type = str) 
        parser.add_argument('sample_type', type = str) 
        try:
            args = parser.parse_args(arg.split()) 
            sdextractremoteinfos.print_small_dataset(args.project)
        except SystemExit:
            pass

    def do_priority(self,arg):
        pass

    def do_history(self,arg):
        li=[d.values() for d in sddao.get_history_lines()] # listofdict to listoflist
        print tabulate(li,headers=['action','selection source','date','insertion_group_id'],tablefmt="orgtbl")

    #def do_si(self,line):
    #    """si SELECTION
    #    Print selection infos.
    #    """
    #    print_selections_infos()
    def do_selection(self,arg):
        if arg=='':
            arg='list'

        li=arg.split()
        action=li[0]

        if action=='list':
            pattern=li[1] if len(li)==2 else None
            sdselectionsgroup.print_selection_list_with_index(pattern)
        else:
            if len(li)==1:
                print "Incorrect argument"
                return
            elif len(li)==2:
                idx=int(li[1])
                s=sdselectionsgroup.selections[idx]

                if action=='cat':
                    sdselection.cat_selection(s.filename)
                elif action=='print':
                    sdselection.print_selection(s.filename)
                elif action=='edit':
                    sdselection.edit_selection(s.file)

    def do_select(self,arg):
        # -- SQL mode (non-documented as not sure if this is here to stay) -- #
        tokens=arg.split()

        column=tokens[0]

        table=tokens[2]
        where_clause=tokens[4:]

        parameter=where_clause

        dry_run=sdsessionparam.get_value('dry_run')

        parameter.append('type=%s'%table.title())
        result=sdquicksearch.run(parameter=parameter,dry_run=dry_run)

        for f in result.files:
            if column in f:
                print f[column]

    def help_selection(self):
        print sdi18n.m0006('selection <action>','Manage selections.',example=sdi18n.m0014)
    def help_cleanup(self):
        print sdi18n.m0006('cleanup','Cleanup data tree (remove empty folder).')
    def help_select(self):
        print sdi18n.m0006('','')
    def help_history(self):
        print sdi18n.m0006('history ','Show local repository changelog.')
    def help_benchmark(self):
        print sdi18n.m0006('benchmark','Bench ESGF indexes')
    def help_priority(self):
        print sdi18n.m0006('priority','Set transfers priority')
    def help_sample(self):
        print sdi18n.m0006('sample sample_type [ project ]','Print samples',example=sdi18n.m0013)
    def help_retry(self):
        print sdi18n.m0006('retry [ all | file ]','Retry failed transfer(s)',example=sdi18n.m0010)

