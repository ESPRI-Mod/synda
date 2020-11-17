# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.stderr import FILE_NOT_FOUND
from synda.tests.context.download.selection.models import Context as Base


class Context(Base):

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        assert FILE_NOT_FOUND in captured.err
