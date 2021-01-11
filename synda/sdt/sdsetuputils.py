# -*- coding: utf-8 -*-

import os
import shutil
import errno

from synda.source.constants import get_env_folder


def check_environment():
    """
    used to make sure ST_HOME is set
    :return:
    """
    if get_env_folder() is None:
        return False
    else:
        return True


def touch(file_path):
    """
    Creates empty file
    :param file_path: path to file to create
    """
    open(file_path, 'a').close()


def copy_file(src, dst):
    """
    layer over shutil copyfile creates dir if not existent
    :param src:
    :param dst:
    :return:
    """
    try:
        shutil.copy(src, dst)
    except IOError as e:
        if e.errno != errno.ENOENT and e.errno != errno.EEXIST:
            raise
        elif e.errno == errno.EEXIST:
            os.mkdir(os.path.join(dst, os.path.basename(src)))

        os.makedirs(os.path.dirname(dst))
        shutil.copy(src, dst)


def copy_tree(src_root, dst_root):
    for item in os.listdir(src_root):
        if os.path.isfile(os.path.join(src_root, item)):
            copy_file(os.path.join(src_root, item), dst_root)
            print('copying {} -> {}'.format(os.path.join(src_root, item), dst_root))
            print('copied')
        elif os.path.isdir(os.path.join(src_root, item)):
            copy_tree(os.path.join(src_root, item), os.path.join(dst_root, item))
