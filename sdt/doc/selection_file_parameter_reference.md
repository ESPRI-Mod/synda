# Selection file parameter reference

This document describes each parameter used in a selection file.

## Search-api parameter

Those parameters are described [here](https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API)

## Synda parameter

Note: those parameters are specific to Synda and cannot be used directly with the Search-api.

This section contains the following sub-groups:

* Synda download parameter
* Synda remote search parameter
* Synda local search parameter
* Synda formatting parameter

### Synda download parameter

#### protocol

Select which protocol to use to download the data. The two currently supported
protocols are http and gridftp.

Type: string

Default: "http"

#### searchapi_host

Set which ESGF index to use for files discovery.

Type: string

Default: &lt;index.default_index&gt; from sdt.conf file (or random index from &lt;index.indexes&gt; in parallel mode)

#### url_replace

Replace all occurrences of substring in url

Type: string

Example:

    url_replace=s|gsiftp://esgf1.dkrz.de/data/cmip6|gsiftp://gridftp.dkrz.de/pool/data/projects/cmip6|

#### priority

Set download priority.

Type: integer

Default: 1000

### Synda remote search parameter

#### timeslice

Select files inside &lt;timeslice&gt;

Type: string

Example:

    synda search atmos mon tasmin CMIP5 CNRM-CM5 timeslice=197001-198512 -f 

### Synda local search parameter

#### local_path

Select files matching &lt;local_path&gt;

Type: string

Example:

    synda list local_path=CMIP5/output1/NCAR/CCSM4/rcp60/mon/land/Lmon/r1i1p1

#### error_msg

Select files matching &lt;error_msg&gt;

Type: string

Example:

    synda list "error_msg=local file already exists," -f

#### insertion_group_id

Select files matching &lt;insertion_group_id&gt;

Type: integer

Example:

    synda list insertion_group_id=71 -f

#### status

Select files matching download &lt;status&gt;

Type: string

Example:

    synda list status=error -f

#### sdget_status

Select files matching &lt;sdget_status&gt;

Type: integer

Example:

    synda list sdget_status=1 -f

### Synda formatting parameter

#### local_path_format

Set local path format. If set to 'treevar', the dataset DRS is used to build the
local path and a folder is added to group files by variable. If set to 'tree',
the dataset DRS is used to build the local path. If set to 'custom', the local
path is built based on template defined in &lt;local_path_drs_template&gt; variable.
If set to 'notree', all files are stored in the same folder.

Type: string

Default: "treevar"

#### local_path_product_format

If set to 'normal', product folders (e.g. 'output1' and 'output2') are kept in
local path. If set to 'remove', product folders level are removed from local
path and products sub-folders are merged. If set to 'merge', product folders are
merged into one folder called 'output' and products sub-folders are merged.

Type: string

Default: "normal"

#### local_path_project_format

If set to 'uc', local path project folder is converted to uppercase.

Type: string

#### local_path_drs_template

Contain the local path custom template.

Type: string

Example:

    local_path_drs_template=%(ensemble)s/%(institute)s-%(rcm_name)s/%(rcm_version)s/%(time_frequency)s/%(variable)s/%(dataset_version)s

Notes:

* To enable this parameter, 'local_path_format' parameter must be set to 'custom'
* Each variable included in 'local_path_drs_template' must be present
as a standalone attribute in the file metadata. If it is missing, you can
use a constant value instead (e.g. 'output' instead of '%(product)s').
