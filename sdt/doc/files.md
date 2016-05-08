# Synda Files 

This document describes most important files and folders used in Synda.

### credentials.conf

Contains user credentials (e.g. ESGF openid)

location:
$HOME/sdt/conf/credentials.conf
/etc/synda/sdt/credentials.conf
/etc/synda/sdt/credentials.conf

--------------------------------------------------------

### data

Contains ESGF files downloaded in tracking mode

$HOME/sdt/data
Set daemon user.

Type: string

Default: ""

Note: the daemon must be started by root for this parameter to work.

--------------------------------------------------------

### sandbox

Contains ESGF files downloaded in no-tracking mode

$HOME/sdt/data
Set daemon user.

Type: string

Default: ""

Note: the daemon must be started by root for this parameter to work.

--------------------------------------------------------

### log

Note: log files are stored in '$HOME/sdt/log' folder (source installation) and
'/var/log/synda/sdt' folder (system package installation).
in $HOME/sdt/log
Set daemon user.

Type: string

Default: ""

Note: the daemon must be started by root for this parameter to work.

--------------------------------------------------------

