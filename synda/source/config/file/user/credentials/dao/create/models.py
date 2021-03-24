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
import configparser


class Create(object):

    def __init__(self, full_filename):

        header = [
            "{}\n".format(
                "# Description",
            ),
            "{}\n".format(
                "#   This file contains user esgf credentials",
            ),
            "{}\n".format(
                "# Notes",
            ),
            "{}\n".format(
                "#   - Line comments using leading '#' or ';' are supported in this file",
            ),
            "{}\n".format(
                "#   - Trailing comment are not supported in this file",
            ),
            "{}\n".format(
                "",
            ),
        ]

        config = configparser.ConfigParser()

        config.add_section('esgf_credential')
        config.set('esgf_credential', 'openid', 'https://esgf-node.ipsl.fr/esgf-idp/openid/foo')
        config.set('esgf_credential', 'password', 'foobar')

        with open(full_filename, 'w') as fh:
            for line in header:
                fh.write(line)
            config.write(fh)


if __name__ == '__main__':
    pass
