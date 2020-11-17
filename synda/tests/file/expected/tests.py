# # -*- coding: utf-8 -*-
# ##################################
# #  @program        synda
# #  @description    climate models data transfer program
# #  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
# #                             All Rights Reserved"
# #  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
# ##################################
# import os
# import unittest
#
# from sdt.tests.constants import DATADIR
# from .reader import Reader
# from sdt.tests.file.exceptions import InvalidIndex
# from sdt.tests.file.exceptions import IndexError
# from sdt.tests.file.exceptions import NotFound
#
#
# class ReadingTest(unittest.TestCase):
#
#     def setUp(self):
#         folder = os.path.join(
#             DATADIR,
#             "testenv",
#         )
#
#         self.fullfilename = os.path.join(
#             folder,
#             "test_by_dataset_and_config_file.txt",
#         )
#
#     def test_validated_file(self):
#         self.assertTrue(
#             Reader(self.fullfilename),
#         )
#
#     def test_file_not_found(self):
#         fullfilename = ""
#         self.assertRaises(
#             NotFound,
#             Reader,
#             fullfilename,
#         )
#
#     def test_filename_entry_found(self):
#         reader = Reader(self.fullfilename)
#         value = reader.get_checksum("areacella_fx_CanCM4_decadal1972_r0i0p0.nc")
#         expected_value = '336fd5fcc367f8f1b71c67fe9b48a68d033cdab6b2152b24164c30a39050dda6'
#         msg = "Checksum / error / expected value is '{}' / observed is = {} ".format(
#             expected_value,
#             value,
#         )
#         self.assertTrue(
#             value == expected_value,
#             msg,
#         )
#
#
# if __name__ == '__main__':
#     unittest.main()
