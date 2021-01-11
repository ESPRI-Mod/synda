# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.process.constants import is_daemon as current_process_is_a_daemon


def get_timeout():

    # When a database is accessed by multiple connections, and one of the processes
    # modifies the database, the SQLite database is locked until that transaction is
    # committed. The timeout parameter specifies how long the connection should wait
    # for the lock to go away until raising an exception. The default for the timeout
    # parameter is 5.0 (five seconds).
    #
    # more info here => http://www.sqlite.org/faq.html#q5
    #
    if current_process_is_a_daemon():

        # we set a high sqlite timeout value for the daemon,
        # so it doesn't exit on timeout error when we are running
        # huge query in Synda IHM (e.g. synda install CMIP5)
        #
        # by doing so, so we are able to use Synda IHM and sqlite3
        # to run manual query without stopping the daemon.

        timeout = Preferences().download_async_db_timeout

    else:

        # we do not need to set a high sqlite timeout value for Synda IHM,
        # as daemon do not perform huge queries, so Synda IHM do not have
        # to wait for long until the sqlite lock is release.

        timeout = Preferences().download_direct_db_timeout

    return timeout
