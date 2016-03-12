# Synda configuration file

### daemon.max_parallel_download

Default: 8

--------------------------------------------------------

### daemon.post_processing

Default: 0

--------------------------------------------------------

### daemon.download_manager

Default: default

--------------------------------------------------------

### post_processing.host

Default: localhost

--------------------------------------------------------

### post_processing.port

Default: 8090

--------------------------------------------------------

### log.verbosity_level

Default: info

--------------------------------------------------------

### log.scheduler_profiling

Default: 0

--------------------------------------------------------

### path.data_path


Default: 

--------------------------------------------------------

### path.db_path

Default: 

--------------------------------------------------------

### interface.unicode_term

Default: 0

--------------------------------------------------------

### interface.progress

Default: 0

--------------------------------------------------------

### behaviour.onemgf

Default: false

--------------------------------------------------------

### behaviour.check_parameter

Default: 1

--------------------------------------------------------

### behaviour.ignorecase

Default: true

--------------------------------------------------------

### behaviour.nearest

Default: false

--------------------------------------------------------

### behaviour.nearest_mode

Nearest replica algorithm

(possible values are: "geolocation", "rtt")

Default: geolocation

--------------------------------------------------------

### behaviour.lfae_mode

Default: abort

'lfae' means "local file already exists"

(possible values are: "keep", "replace", "abort")

--------------------------------------------------------

### behaviour.incorrect_checksum_action

remove => if checksum doesn't match, set transfer status to error and remove file from local repository
keep   => if checksum doesn't match, set transfer status to done, log a warning and keep file in local repository

Default: remove

--------------------------------------------------------

### index.indexes

Default: pcmdi.llnl.gov

--------------------------------------------------------

### index.default_index

Default: pcmdi.llnl.gov

--------------------------------------------------------

### locale.country

Default: 

--------------------------------------------------------

### globus.esgf_endpoints

Default: /esg/config/esgf_endpoints.xml

--------------------------------------------------------

### globus.destination_endpoint

Default: destination#endpoint
