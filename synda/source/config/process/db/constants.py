# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.user.preferences.models import Config as Preferences

from synda.source.config.file.downloading.models import Config as Filedownloading


def get_timeout():

    # When a database is accessed by multiple connections, and one of the processes
    # modifies the database, the SQLite database is locked until that transaction is
    # committed. The timeout parameter specifies how long the connection should wait
    # for the lock to go away until raising an exception. The default for the timeout
    # parameter is 5.0 (five seconds).
    #
    # more info here => http://www.sqlite.org/faq.html#q5
    #
    fd = Filedownloading()
    if fd.process_is_active():

        # we set a high sqlite timeout value if the downloading process is active
        timeout = Preferences().download_async_db_timeout
    else:
        timeout = Preferences().download_direct_db_timeout

    return timeout
