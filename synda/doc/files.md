# Synda Files and Folders

This document describes most important files and folders in use in Synda

## Files

### credentials.conf

This file contains user credentials (e.g. ESGF openid).

Location is *$HOME/sdt/conf/credentials.conf* for source installation and
*/etc/synda/sdt/credentials.conf* for system package installation.

--------------------------------------------------------

### sdt.conf

This file contains configuration parameters.

Location is *$HOME/sdt/conf/sdt.conf* for source installation and
*/etc/synda/sdt/sdt.conf* for system package installation.

## Folders

### data

This folder contains ESGF files downloaded in tracking mode.

Location is *$HOME/sdt/data* for source installation and */srv/synda/sdt/data* for
system package installation.

--------------------------------------------------------

### sandbox

This folder contains ESGF files downloaded in non-tracking mode.

Location is *$HOME/sdt/sandbox* for source installation and */srv/synda/sdt/sandbox* for
system package installation.

--------------------------------------------------------

### log

This folder contains log files.

Location is *$HOME/sdt/log* for source installation and
*/var/log/synda/sdt* for system package installation.

--------------------------------------------------------

### configuration

This folder contains configuration files.

Location is *$HOME/sdt/conf* for source installation and
*/etc/synda/sdt* for system package installation.

--------------------------------------------------------

### database

This folder contains database file.

Location is *$HOME/sdt/db* for source installation and
*/var/lib/synda/sdt* for system package installation.

--------------------------------------------------------

### selection

This folder contains selection files.

Location is *$HOME/sdt/selection* for source installation and
*/etc/synda/sdt/selection* for system package installation.

--------------------------------------------------------

### default

This folder contains selection parameters default values.

Location is *$HOME/sdt/conf/default* for source installation and
*/etc/synda/sdt/default* for system package installation.
