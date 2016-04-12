# Configuration parameter reference

This document describes each parameter used in "std.conf" file to configure Synda.

### daemon.user

Set daemon user.

Note: the daemon must be started by root for this parameter to work.

Type: string

Default: ""

--------------------------------------------------------

### daemon.group

Set daemon group.

Note: the daemon must be started by root for this parameter to work.

Type: string

Default: ""

--------------------------------------------------------

### download.max_parallel_download

Set the number of parallel download.

Type: int

Default: 8

--------------------------------------------------------

### download.hpss

Gives HPSS service some time to move data from tape to disk.

Type: boolean

Default: 0

--------------------------------------------------------

### module.post_processing

If true, send download completion events to the post-processing module.

Type: boolean

Default: 0

--------------------------------------------------------

### module.globustransfer

If true, use Globus Transfer platform to download files.

Type: boolean

Default: 0

--------------------------------------------------------

### post_processing.host

Post-processing daemon host

Type: string

Default: localhost

--------------------------------------------------------

### post_processing.port

Post-processing daemon port

Type: int

Default: 8090

--------------------------------------------------------

### log.verbosity_level

Log verbosity level

Type: string

Default: info

--------------------------------------------------------

### log.scheduler_profiling

If true, log code profiling information

Type: boolean

Default: 0

--------------------------------------------------------

### core.data_path

Override the default data path

Type: string

Default: '$HOME/sdt/data' for source installation and '/srv/synda/sdt' for system package installation.

--------------------------------------------------------

### core.db_path

Override the default database path

Type: string

Default: '$HOME/sdt/db' for source installation and '/var/lib/synda/sdt' for system package installation.

--------------------------------------------------------

### interface.unicode_term

If true, use unicode characters for progress bar.

Type: boolean

Default: 0

--------------------------------------------------------

### interface.progress

If true, show progress bar for time consuming task.

Type: boolean

Default: 0

--------------------------------------------------------

### behaviour.onemgf

Improve search performance (experimental).

Type: boolean

Default: false

--------------------------------------------------------

### behaviour.check_parameter

If true, perform parameter typo detection (name and value).

Example

If behaviour.check_parameter is true,

    $ synda search cmip5 taz

will raises an exception and informs the user that 'taz' value is not found.

Type: boolean

Default: 1

--------------------------------------------------------

### behaviour.ignorecase

If true, automatically fix incorrect case

Example

    $ synda search MOHC-HADGEM3-RA

This command normally raises an exception as the correct case should be 'MOHC-HadGEM3-RA'.

But if behaviour.ignorecase is true, the model name will be automatically corrected and no exception will occur.

Type: boolean

Default: true

--------------------------------------------------------

### behaviour.nearest

If true, automatically select the nearest file replica

Type: boolean

Default: false

--------------------------------------------------------

### behaviour.nearest_mode

Set nearest replica algorithm.

Possible values are: "geolocation" and "rtt"

Type: string

Default: geolocation

--------------------------------------------------------

### behaviour.lfae_mode

Set which policies to adopt when a download starts and local file already exists.

Possible values are: "keep", "replace" and "abort"

Type: string

Default: abort

--------------------------------------------------------

### behaviour.incorrect_checksum_action

Set which policies to adopt when checksum doesn't match

Possible values are: "remove" and "keep"

"remove": set transfer status to error and remove the downloaded file

"keep": set transfer status to done, log a warning and keep the downloaded file

Type: string

Default: remove

--------------------------------------------------------

### index.indexes

Set the indexes list to use for large operation

Note: this parameter is used for load-balancing on several indexes, to speed up large search-API requests

Type: string

Default: pcmdi.llnl.gov

--------------------------------------------------------

### index.default_index

Set the index to use in priority

Type: string

Default: pcmdi.llnl.gov

--------------------------------------------------------

### locale.country

Set the country in which synda is installed

Note: used to compute nearest replicat when "geolocation" mode is used

Type: string

Default: ""

--------------------------------------------------------

### globus.esgf_endpoints

Set globus endpoints

Type: string

Default: /esg/config/esgf_endpoints.xml

--------------------------------------------------------

### globus.destination_endpoint

Set destination endpoint

Type: string

Default: destination#endpoint
