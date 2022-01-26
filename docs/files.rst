.. _files:

Synda Files and Folders
=======================

This document describes most important files and folders in use in Synda.

$HOME is the directory in which you want to place your Synda environment.

notes
  Synda environment can be as a workspace.


Configuration files
*******************

``credentials.conf``
    This file contains user credentials (e.g. ESGF openid).
    Location is ``$HOME/conf/credentials.conf``.

``sdt.conf``
    This file contains configuration parameters.
    Location is ``$HOME/conf/sdt.conf``.

``internal.conf``
    This file contains internal configuration parameters.
    Location is ``$HOME/conf/internal.conf``.

Folders
*******

``conf``
    This folder contains configuration files and default folder.
    Location is ``$HOME/conf``.

``default``
    This folder contains selection parameters default values.
    Location is ``$HOME/conf/default``.

``data``
    This folder contains ESGF files downloaded in tracking mode.
    Location is ``$HOME/data``.

``sandbox``
    This folder contains ESGF files downloaded in non-tracking mode.
    Location is ``$HOME/sandbox``.

``log``
    This folder contains log files.
    Location is ``$HOME/log``.

``selection``
    This folder contains selection files.
    Location is ``$HOME/selection``.

Database
*********

``sdt.db``
    This file contains the dataset and file entries to track downloads.
    Location is ``$HOME/db/sdt.db``.
