# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import sys

from synda.sdt import main as synda
from synda.source.identifier import Identifier


class Process(Identifier):

    def __init__(self, name, arguments=None, exceptions_codes=None):
        super(Process, self).__init__(name)

        # initializations
        self.exceptions_codes = []

        self.arguments = dict(
            positional=[],
            optional=[],
        )

        # settings
        self.arguments = arguments
        self.exceptions_codes = exceptions_codes

    def get_subcommand_name(self):
        return self.get_identifier()

    def set_exceptions_codes(self, exceptions_codes):
        self.exceptions_codes = exceptions_codes

    def set_arguments(self, arguments):
        self.arguments = arguments

    def get_arguments(self):
        return self.arguments

    def get_optional_arguments(self):
        return self.arguments["optional"]

    def get_positional_arguments(self):
        return self.arguments["positional"]

    def get_sys_argv(self):
        argv = ['synda', self.get_subcommand_name()]
        argv.extend(
            [p for p in self.get_arguments()["positional"]]
        )
        argv.extend(
            [p for p in self.get_arguments()["optional"]]
        )
        return argv

    def execute(self):
        success = False

        sys.argv = self.get_sys_argv()

        try:
            synda.run()
        except Exception as exception:

            assert exception.value.code in self.exceptions_codes
            if isinstance(exception.value.code, int):
                if exception.value.code in [0, 1]:
                    success = True

        return success


if __name__ == '__main__':

    url = 'gsiftp://aimsdtn3.llnl.gov:2811//cmip5_css01_data/cmip5/output1/CNRM-CERFACS/CNRM-CM5/amip/mon/atmos/Amon/r1i1p1/v20111006/tasmin/tasmin_Amon_CNRM-CM5_amip_r1i1p1_197901-200812.nc'
    arguments = dict(
        positional=[url],
        optional=["--yes"],
    )

    sub_command = Process(
        "install",
        arguments=arguments,
        exceptions_codes=[0],
    )

    success = sub_command.execute()
    pass
