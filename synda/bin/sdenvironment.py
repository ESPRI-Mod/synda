#!/usr/bin/env python

"""Sets up the environment as needed for the daemon to run."""
# This has to be done before many 'import' statements.
# This may not be needed at all installations, and may have to be edited at others.
# I wish there were a cleaner way to accomplish this.

import os
import sys

# Needed sdconst import because it references const which references test/constant...
sys.path.append( os.path.normpath( os.path.join( os.path.dirname(os.path.abspath(__file__)),
                                                 '../..' )))
sys.path.append( os.path.normpath( os.path.join( os.path.dirname(os.path.abspath(__file__)),
                                                 '../lib/python2.7/site-packages' )))
# This also seems necessary for one of the imports.
if 'ST_HOME' not in os.environ:
    os.environ['ST_HOME'] = '/etc/synda/sdt'
