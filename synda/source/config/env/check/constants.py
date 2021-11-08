# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.user.credentials.constants import FILENAME as CREDENTIALS_FILENAME
from synda.source.config.file.user.preferences.constants import FILENAME as PREFERENCES_FILENAME
from synda.source.config.file.internal.constants import FILENAME as INTERNAL_FILENAME
from synda.source.config.file.db.constants import FILENAME as DB_FILENAME

ERROR_ENVIRONMENT_VARIABLE_PREFIX = "Please set the environment variable"

REQUIRED_FILES = [
    'bin/sdcleanup_tree.sh',
    'bin/sdconvert.sh',
    'bin/sdgetg.sh',
    'bin/sdget.sh',
    'bin/sdparsewgetoutput.sh',

    'conf/{}'.format(PREFERENCES_FILENAME),
    'conf/{}'.format(CREDENTIALS_FILENAME),
    'conf/{}'.format(INTERNAL_FILENAME),

    'db/{}'.format(DB_FILENAME),
]

REQUIRED_DIRECTORIES = [
    'tmp',
    'log',
    'selection'
]

ERROR_KEY_FILE_MISSING_TEMPLATE = 'Key file missing: {}'
ERROR_KEY_DIRECTORY_MISSING_TEMPLATE = 'Key directory missing: {}'

CHECK_COMPLETE = 'Check complete.'
CHECK_ERROR = 'Check with error(s).'
