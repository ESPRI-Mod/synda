# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import hashlib

from synda.source.config.file.constants import CHECKSUM


def get_hash_obj(checksum_type):

    if checksum_type == CHECKSUM['type']["sha256"]:
        hash_obj = hashlib.sha256()
    elif checksum_type == CHECKSUM['type']["md5"]:
        hash_obj = hashlib.md5
    else:
        hash_obj = None

    return hash_obj


class Checksum(object):

    def __init__(self, checksum_type=CHECKSUM['type']["sha256"], checksum_value=""):
        super(Checksum, self).__init__()
        self.type = ""
        self.value = ""

        self.init(checksum_type, checksum_value)

    def init(self, checksum_type, checksum_value):
        self.type = checksum_type
        self.value = checksum_value

    def get_type(self):
        return self.type

    def set_value(self, value):
        self.value = value

    def are_equals(self, value):
        return self.value == value

    def calculate(self, full_filename):
        value = ""

        hash_obj = get_hash_obj(self.type)

        if hash_obj:
            with open(full_filename, 'rb') as f:
                while True:
                    chunk = f.read(16 * 1024)
                    if not chunk:
                        break
                    hash_obj.update(chunk)
                value = hash_obj.hexdigest()

        return value

    def set_calculated_value(self, full_filename):
        value = self.calculate(full_filename)
        self.set_value(value)

    def validate(self, full_filename):
        calculated_checksum = self.calculate(full_filename)
        assert self.are_equals(
            calculated_checksum,
        )
