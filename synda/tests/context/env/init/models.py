# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.tests.tests.constants import ST_HOME_TESTS
from synda.source.process.env.init.models import Config

from synda.source.config.env.init.constants import INFORMATION_HEADER
from synda.source.config.env.init.constants import INFORMATION_CONTENT_TEMPLATE

from synda.tests.context.models import Context as Base


class Context(Base, Config):

    def __init__(self, capsys=None):
        assert isinstance(capsys, object)
        Base.__init__(self, capsys=capsys)
        Config.__init__(self)

    def validation_after_subcommand_execution(self):
        captured = self.get_capsys().readouterr()
        assert INFORMATION_HEADER in captured.out
        assert INFORMATION_CONTENT_TEMPLATE.format(
                ST_HOME_TESTS,
            ) in captured.out
