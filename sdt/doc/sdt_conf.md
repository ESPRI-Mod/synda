# Configuration parameter reference

This document describes each parameter used in "std.conf" file to configure Synda.

### daemon.user

Set daemon user.

Note: the daemon must be started by root for this parameter to work.

Default: ""

--------------------------------------------------------

### daemon.group

Set daemon group.

Note: the daemon must be started by root for this parameter to work.

Default: ""

--------------------------------------------------------

### download.max_parallel_download

Set the number of parallel download.

Default: 8

--------------------------------------------------------

### download.hpss

Gives HPSS service some time to move data from tape to disk.

Default: 0

--------------------------------------------------------

### module.post_processing

If true, send download completion events to the post-processing module.

Default: 0

--------------------------------------------------------

### module.globusonline

If true, use globus online platform to download files.

Default: 0

--------------------------------------------------------

### post_processing.host

Post-processing daemon host

Default: localhost

--------------------------------------------------------

### post_processing.port

Post-processing daemon port

Default: 8090

--------------------------------------------------------

### log.verbosity_level

Log verbosity level

Default: info

--------------------------------------------------------

### log.scheduler_profiling

If true, log code profiling information

Default: 0

--------------------------------------------------------

### core.data_path

Override the default data path

Default: '$HOME/sdt/data' for source installation and '/srv/synda/sdt' for system package installation.

--------------------------------------------------------

### core.db_path

Override the default database path

Default: '$HOME/sdt/db' for source installation and '/var/lib/synda/sdt' for system package installation.

--------------------------------------------------------

### interface.unicode_term

If true, use unicode characters for progress bar.

Default: 0

--------------------------------------------------------

### interface.progress

If true, show progress bar for time consuming task.

Default: 0

--------------------------------------------------------

### behaviour.onemgf

Improve search performance (experimental).

Default: false

--------------------------------------------------------

### behaviour.check_parameter

If true, perform parameter typo detection (name and value).

Example

If behaviour.check_parameter is true,

    $ synda search cmip5 taz

will raises an exception and informs the user that 'taz' value is not found.

Default: 1

--------------------------------------------------------

### behaviour.ignorecase

If true, automatically fix incorrect case

Example

    $ synda search MOHC-HADGEM3-RA

This command normally raises an exception as the correct case should be 'MOHC-HadGEM3-RA'.

But if behaviour.ignorecase is true, the model name will be automatically corrected and no exception will occur.

Default: true

--------------------------------------------------------

### behaviour.nearest

If true, automatically select the nearest file replica

Default: false

--------------------------------------------------------

### behaviour.nearest_mode

Set nearest replica algorithm.

Possible values are: "geolocation" and "rtt"

Default: geolocation

--------------------------------------------------------

### behaviour.lfae_mode

Set which policies to adopt when a download starts and local file already exists.

Possible values are: "keep", "replace" and "abort"

Default: abort

--------------------------------------------------------

### behaviour.incorrect_checksum_action

Set which policies to adopt when checksum doesn't match

Possible values are: "remove" and "keep"

"remove": set transfer status to error and remove the downloaded file

"keep": set transfer status to done, log a warning and keep the downloaded file

Default: remove

--------------------------------------------------------

### index.indexes

Set the indexes list to use for large operation

Note: this parameter is used for load-balancing on several indexes, to speed up large search-API requests

Default: pcmdi.llnl.gov

--------------------------------------------------------

### index.default_index

Set the index to use in priority

Default: pcmdi.llnl.gov

--------------------------------------------------------

### locale.country

Set the country in which synda is installed

Note: used to compute nearest replicat when "geolocation" mode is used

Default: ""

--------------------------------------------------------

### globus.esgf_endpoints

Set globus endpoints

Default: /esg/config/esgf_endpoints.xml

--------------------------------------------------------

### globus.destination_endpoint

Set destination endpoint

Default: destination#endpoint
