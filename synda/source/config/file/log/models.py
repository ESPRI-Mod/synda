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
import os
import uuid

from synda.source.containers import Container
from synda.source.identifier import Identifier

from synda.source.config.file.log.constants import IDENTIFIER

from synda.source.config.file.internal.models import Config as Internal

from synda.source.config.file.log.constants import FILE_DEBUG

from synda.source.config.path.tree.models import Config as TreePath


class Config(Container, Identifier):

    def __init__(self):
        Container.__init__(self)
        Identifier.__init__(self, IDENTIFIER)

        internal = Internal()

        self.identifiers = ["feeder", "domain", "consumer", "stack_trace", "debug"]

        self.filenames = dict()
        self.filenames[self.identifiers[0]] = internal.logger_feeder_file
        self.filenames[self.identifiers[1]] = internal.logger_domain_file
        self.filenames[self.identifiers[2]] = internal.logger_consumer_file

        self.filenames[self.identifiers[3]] = "sdt_stacktrace_{}.log".format(
            uuid.uuid4(),
        )
        self.filenames[self.identifiers[4]] = FILE_DEBUG

        path = TreePath()

        if path.provides("log"):
            log_path = path.get("log")

            paths = dict()
            for identifier, filename in self.filenames.items():
                paths[identifier] = os.path.join(
                    log_path,
                    filename,
                )

            self.set_data(paths)

    def get_filenames(self):
        return self.filenames.values()

    def get(self, filename_identifier):
        return self.get_data()[filename_identifier]


if __name__ == '__main__':
    pass
