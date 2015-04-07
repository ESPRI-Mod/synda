#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""syndac command (REPL front-end).

Note
    'syndac' stands for "SYNchro-DAta Console".
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
if os.path.exists(sdconfig.syndac_history_path):
    readline.read_history_file(sdconfig.syndac_history_path)

# history save
def save_history(history_path=sdconfig.syndac_history_path):
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
