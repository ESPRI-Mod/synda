#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""sdtc command (REPL front-end).

Note
    'sdtc' stands for "SynDa Transfer Console".
"""

import atexit
import sys
import os
import readline
import rlcompleter
import re
import signal
import sdapp
from sdexception import SDException
from sdusrcon import UserConsole
import sdconfig

# history load
if os.path.exists(sdconfig.sdtc_history_file):
    readline.read_history_file(sdconfig.sdtc_history_file)

# history save
def save_history(history_path=sdconfig.sdtc_history_file):
    import readline # import must stay here as this func is used by atexit
    readline.write_history_file(history_path)
atexit.register(save_history)

# override default handlers set in 'sdapp' module
#signal.signal(signal.SIGINT, signal.SIG_IGN)
#signal.signal(signal.SIGINT,  signal.SIG_DFL)
#signal.signal(signal.SIGTERM, signal.SIG_DFL)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        UserConsole().onecmd(' '.join(sys.argv[1:]))
    else:
        UserConsole().cmdloop()
