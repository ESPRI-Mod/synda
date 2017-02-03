.. _files:

Synda Files and Folders
=======================

This document describes most important files and folders in use in Synda.

Configuration files
*******************

``credentials.conf``
    This file contains user credentials (e.g. ESGF openid).
    Location is ``$HOME/{sdt,sdp}/conf/credentials.conf`` for source installation
    and ``/etc/synda/{sdt,sdp}/credentials.conf`` for system package installation.

``sdt.conf``
    This file contains configuration parameters for transfer module.
    Location is ``$HOME/sdt/conf/sdt.conf`` for source installation and
    ``/etc/synda/sdt/sdt.conf`` for system package installation.

``sdp.conf``
    This file contains configuration parameters for transfer module.
    Location is ``$HOME/sdp/conf/sdp.conf`` for source installation and
    ``/etc/synda/sdp/sdp.conf`` for system package installation.

Folders
*******

``data``
    This folder contains ESGF files downloaded in tracking mode.
    Location is ``$HOME/sdt/data`` for source installation and
    ``/srv/synda/sdt/data`` for system package installation.

``sandbox``
    This folder contains ESGF files downloaded in non-tracking mode.
    Location is ``$HOME/sdt/sandbox`` for source installation and
    ``/srv/synda/sdt/sandbox`` for system package installation.

``log``
    This folder contains log files.
    Location is ``$HOME/{sdt,sdp}/log`` for source installation and
    ``/var/log/synda/{sdt,sdp}`` for system package installation.

``selection``
    This folder contains selection files.
    Location is ``$HOME/sdt/selection`` for source installation and
    ``/etc/synda/sdt/selection`` for system package installation.

``default``
    This folder contains selection parameters default values.
    Location is ``$HOME/sdt/conf/default`` for source installation and
    ``/etc/synda/sdt/default`` for system package installation.

``pipeline``
    This folder contains pipelines definition scripts.
    Location is ``$HOME/sdp/conf/pipeline`` for source installation and
    ``/etc/synda/sdp/pipeline`` for system package installation.

Databases
*********

``sdt.db``
    This file contains the dataset and file entries to track downloads.
    Location is ``$HOME/sdt/db/sdt.db`` for source installation and
    ``/var/lib/synda/sdt/sdt.db`` for system package installation.

``sdp.db``
    This file contains the post-processing entries to track pipeline execution.
    Location is ``$HOME/sdp/db/sdp.db`` for source installation and
    ``/var/lib/synda/sdp/sdp.db`` for system package installation.


