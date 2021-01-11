# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

from synda.tests.context.models import Context as Base
from synda.tests.tests.constants import DATASET_EXAMPLE


class Context(Base):

    def __init__(self, dataset="", capsys=None):
        super(Context, self).__init__(capsys=capsys)
        # init
        self.dataset = ""
        # settings
        self.dataset = dataset

    def get_dataset(self):
        return self.dataset

    def set_dataset(self, dataset):
        self.dataset = dataset

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        assert DATASET_EXAMPLE["version"] in captured.out
