#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains Synda core classes."""

import cmd
import sys
import traceback
import sdtools
import sdsessionparam
from sdexception import SDException

class BaseConsole(cmd.Cmd,object):
    """This class contains Cmd module extension routines."""

    doc_header = 'Available commands (type help <topic>):'
    #misc_header = 'misc_header'
    undoc_header = None
    #ruler = '-'

    # overrides std behaviours

    def do_EOF(self,line):
        print
        return True

    def emptyline(self):
        pass

    def default(self,arg):
        print '*** Unknown command: %s'%arg

    def do_quit(self,line):
        return True

    def do_help(self,arg):
        """help
        Print help.
        """

        # Call parent method of same name. This is a tricks to document 'do_help' so to
        # prevent 'undoc_header' menu to show. Using 'super' need new class feature, so
        # we inherit from also 'object'.

        super(BaseConsole,self).do_help(arg)

    def print_topics(self, header, cmds, cmdlen, maxcol):
        """This override is an hack that prevent displaying help topics if header is None."""

        if header is not None:
            if cmds:
                self.stdout.write("%s\n"%str(header))
                if self.ruler:
                    self.stdout.write("%s\n"%str(self.ruler * len(header)))
                self.columnize(cmds, maxcol-1)
                self.stdout.write("\n")

    def cmdloop(self, intro=None):
        """This override is an hack that add an exception handler to Cmd module.

        It provides two things:
            - Better handling of SDException (prevent leaving the console when SDException occur)
            - Better handling of CTRL-C (prevent the console to exit when hitting CTRL-C (just stops the current instruction if any))
                - TODO: currently, this DOESN'T WORK: see below

        Notes:
            This method override Cmd base class method.
            Hack from http://stackoverflow.com/questions/8813291/better-handling-of-keyboardinterrupt-in-cmd-cmd-command-line-interpreter
        """
        print(self.intro) # displays intro msg only once

        while True:
            try:
                super(BaseConsole, self).cmdloop(intro="") # note that we don't display intro here on purpose (else, it would be displayed twice)

                # during normal exit, we come here
                self.postloop()
                break
            except SDException,e: # prevent exiting console when SDException is raised
                sdtools.print_stderr()
                sdtools.print_stderr('*** Error occured ***')
                sdtools.print_stderr()

                sdtools.print_stderr('Error code: %s'%e.code)
                sdtools.print_stderr('Error message: %s'%e.msg)
                sdtools.print_stderr()

                debug=sdsessionparam.get_value('debug')
                if debug:
                    sdtools.print_stderr('Stacktrace:')
                    traceback.print_exc(file=sys.stderr)
            """
            DOESN'T WORK because of the KeyboardInterrupt is transformed into SystemExit in from_signal_to_atexit() func

            except KeyboardInterrupt: # prevent exiting console when CTRL is hit
                print("^C")
            """
