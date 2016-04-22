# Selection file parameter reference

This document describes each parameter used in a selection file.

## Search-api parameter

Those parameters are described [here](https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API)

## Synda parameter

Those parameters are specific to Synda and cannot be used directly with the Search-api.

This section contains the following sub-groups:

* Synda local search parameter
* Synda remote search parameter
* Synda download parameter
* Synda formatting parameter

### Synda local search parameter

#### local_path

This parameter select local files using local path.

Type: string

--------------------------------------------------------

#### error_msg

This parameter select local files using error message.

Type: string

--------------------------------------------------------

#### insertion_group_id

This parameter select local files using insertion group identifier.

Type: integer

--------------------------------------------------------

#### status

This parameter select local files using download status.

Type: string

--------------------------------------------------------

#### sdget_status

This parameter select local files using sdget_status.

Type: integer

### Synda remote search parameter

#### timeslice

This parameter select files using filename timestamp.

Type: string

--------------------------------------------------------

### Synda download parameter

#### protocol

Select which protocol to use to download the data. Currently, the two supported
protocols are http and gridftp.

Type: string

Default: "http"

--------------------------------------------------------

#### searchapi_host

Set which ESGF index to use.

Type: string

Default: <index.default_index> from sdt.conf file (or random index from <index.indexes> in parallel mode)

--------------------------------------------------------

#### priority

Set download priority.

Type: integer

Default: 1000

### Synda formatting parameter

#### local_path_format

Set local path format. If set to 'treevar', the dataset DRS is used to build the
local path and a folder is added to group files by variable. If set to 'tree',
the dataset DRS is used to build the local path. If set to 'custom', the local
path is built based on template defined in <local_path_drs_template> variable.
If set to 'notree', all files are stored in the same folder.

Type: string

Default: "treevar"

--------------------------------------------------------

#### local_path_product_format

If set to 'normal', product folders (e.g. 'output1' and 'output2') are kept in
local path. If set to 'remove', product folders level are removed from local
path and products sub-folders are merged. If set to 'merge', product folders are
merged into one folder called 'output' and products sub-folders are merged.

Type: string

Default: "normal"

--------------------------------------------------------

#### local_path_project_format

If set to 'uc', local path project folder is converted to uppercase.

Type: string

--------------------------------------------------------

#### local_path_drs_template

Contain the local path custom template.

Type: string
