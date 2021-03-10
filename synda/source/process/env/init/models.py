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
import sys
import tarfile

from synda.source.identifier import Identifier

from synda.source.constants import get_env_folder

from synda.source.config.file.env.models import Config as EnvFile

from synda.source.config.env.init.constants import INFORMATION_HEADER
from synda.source.config.env.init.constants import INFORMATION_CONTENT_TEMPLATE

from synda.source.process.env.init.constants import IDENTIFIER
from synda.source.process.env.check.models import Config as CheckEnv


def confirm():
    answer = ""
    while answer == '' or answer not in ['y', 'n']:
        answer = input(
            'Synda environment needs a few key files. \n'
            'Would you like to init the stubs of these files? y/n: ',
        ).lower()

    if answer == 'y':
        confirmed = True
    else:
        sys.exit('Warning: Environment not set up for synda to operate properly. Exiting.')

    return confirmed


class Config(Identifier):

    def __init__(
            self,
    ):
        Identifier.__init__(self, IDENTIFIER)

    def untar(self, source, destination):

        tar = tarfile.open(
            source,
            "r:gz",
        )

        try:
            tar.extractall(destination)
        finally:
            tar.close()

    def create(self, destination, source=""):
        if not source:
            # default tar file
            source = EnvFile().get()
        self.untar(source, destination)

    def process(self, destination, source="", interactive_mode=False):
        if interactive_mode:
            print(INFORMATION_HEADER)
            confirmed = confirm()
            if confirmed:
                self.create(destination, source=source)
                print(
                    INFORMATION_CONTENT_TEMPLATE.format(
                        get_env_folder(),
                    ),
                )
                CheckEnv(get_env_folder()).process(interactive_mode=True)
        else:
            self.create(destination, source=source)
