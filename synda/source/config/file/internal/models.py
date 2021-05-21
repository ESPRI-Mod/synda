# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
"""
from synda.source.config.file.models import Config as Base
from synda.source.config.file.env.constants import ENV_NOT_FOUND
from synda.source.config.file.internal.constants import IDENTIFIER
from synda.source.config.file.internal.constants import DEFAULT_OPTIONS
from synda.source.config.file.internal.constants import FULL_FILENAME_USED_IF_INIT_ENV_NOT_FOUND
from synda.source.config.file.internal.constants import DEFAULT_FULL_FILENAME
from synda.source.config.file.internal.constants import FILENAME, DIRECTORY
from synda.source.config.file.internal.exceptions import NotFound

from synda.source.config.file.user.readers import get_parser


class Config(Base):

    def __init__(self, full_filename=DEFAULT_FULL_FILENAME):
        Base.__init__(self, IDENTIFIER, full_filename)

        if not self.exists():
            # print(ENV_NOT_FOUND)
            # Use of the 'sdt.conf' located into the synda resource directory
            full_filename = FULL_FILENAME_USED_IF_INIT_ENV_NOT_FOUND

        self.set_data(get_parser(full_filename, DEFAULT_OPTIONS))

    # LOGGERS SECTION

    @property
    def logger_feeder(self):
        return self.get_data().get('logger', 'feeder_name')
    @property
    def logger_consumer(self):
        return self.get_data().get('logger', 'consumer_name')
    @property
    def logger_domain(self):
        return self.get_data().get('logger', 'domain_name')
    @property
    def logger_feeder_file(self):
        return self.get_data().get('logger', 'feeder_file')
    @property
    def logger_consumer_file(self):
        return self.get_data().get('logger', 'consumer_file')
    @property
    def logger_domain_file(self):
        return self.get_data().get('logger', 'domain_file')

    # FILENAMES SECTION

    @property
    def checksum_type_md5(self):
        return self.get_data().get('checksum', 'type_md5')
    @property
    def checksum_type_sha256(self):
        return self.get_data().get('checksum', 'type_sha256')

    # PROCESSES SECTION

    @property
    def processes_chunksize(self):
        return self.get_data().getint('processes', 'chunksize')
    @property
    def processes_transfer_protocol(self):
        return self.get_data().get('processes', 'transfer_protocol')
    @property
    def processes_http_client(self):
        return self.get_data().get('processes', 'http_client')
    @property
    def is_processes_get_files_caching(self):
        return self.get_data().getboolean('processes', 'get_files_caching')

    # API SECTION

    @property
    def api_esgf_search_domain_name(self):
        return self.get_data().get('api', 'esgf_search_domain_name')

    # HACK SECTION

    @property
    def hack_projects_with_one_variable_per_dataset(self):
        return [e.strip() for e in self.get_data().get('hack', 'projects_with_one_variable_per_dataset').split(',')]
