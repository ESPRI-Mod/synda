#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
# 						 All Rights Reserved
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module compute local path for both file and dataset."""
import re
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdexception
from sdt.bin.commons.utils import sdtools
from sdt.bin.commons.utils import sdproduct
from sdt.bin.commons.pipeline import sdpostpipelineutils


def run(files, mode='file'):
    # set dataset localpath keyname
    if mode == 'file':
        dataset_localpath_keyname = "dataset_local_path"
    elif mode == 'dataset':
        dataset_localpath_keyname = "local_path"
    else:
        assert False

    # warning: dot not change blocks order below

    # add dataset localpath attribute
    files = add_dataset_local_path(files, dataset_localpath_keyname)

    # add file localpath attribute
    if mode == 'file':
        files = add_file_local_path(files)

    return files


def add_dataset_local_path(files, key):
    for f in files:
        f[key] = sdlocalpathutils.build_dataset_local_path(f)

    files = transform_local_path_product(files, key)
    files = transform_local_path_project(files, key)

    return files


def add_file_local_path(files):
    for f in files:
        f["local_path"] = sdlocalpathutils.build_file_local_path(f)

    return files


def transform_local_path_project(files, key):
    def extract_project(path):
        m = re.search('^([^/]+)/', path)
        if m != None:
            project = m.group(1)

            return project
        else:
            raise sdexception.SDException('SDLOCALP-006', 'Incorrect value (path={})'.format(path))

    for f in files:
        fmt = sdpostpipelineutils.get_attached_parameter(f, 'local_path_project_format',
                                                         sdconst.DEFAULT_LOCAL_PATH_PROJECT_FORMAT)
        if fmt == "uc":
            path = f[key]

            project = extract_project(path)

            f[key] = re.sub('^' + project, project.upper(), path)

    return files


def transform_local_path_product(files, key):
    for f in files:
        fmt = sdpostpipelineutils.get_attached_parameter(f, 'local_path_product_format',
                                                         sdconst.DEFAULT_LOCAL_PATH_PRODUCT_FORMAT)

        if fmt == "normal":
            pass
        elif fmt == "merge":
            f[key] = sdproduct.replace_output12_product_with_output_product(f[key])
        elif fmt == "remove":
            f[key] = sdproduct.remove_product(f[key])
        else:
            raise sdexception.SDException('SDLOCALP-002', "'local_path_product_format' is incorrect ({})".format(fmt))

    return files


def build_file_local_path(f):
    fmt = sdpostpipelineutils.get_attached_parameter(f, 'local_path_format', sdconst.DEFAULT_LOCAL_PATH_FORMAT)

    if fmt == "treevar":
        path = "%(dataset_local_path)s/%(variable)s/%(filename)s" % f
    elif fmt == "tree":
        path = "%(dataset_local_path)s/%(filename)s" % f
    elif fmt == "custom":
        path = "%(dataset_local_path)s/%(filename)s" % f
    elif fmt == "customvar":  # TAGJ34234JK24
        path = "%(dataset_local_path)s/%(variable)s/%(filename)s" % f
    elif fmt == "homemade":
        path = "%(dataset_local_path)s/%(filename)s" % f
    elif fmt == "notree":
        path = "%(filename)s" % f
    else:
        raise sdexception.SDException('SDLOCALP-001', "'local_path_format' is incorrect (%s)" % fmt)

    return path


def build_dataset_local_path(f):
    fmt = sdpostpipelineutils.get_attached_parameter(f, 'local_path_format', sdconst.DEFAULT_LOCAL_PATH_FORMAT)

    if fmt == "treevar":
        path = "%(dataset_path)s" % f  # note that we don't add var folder here (we do it only for the file local path)
    elif fmt == "tree":
        path = "%(dataset_path)s" % f
    elif fmt == "custom" or fmt == "customvar":  # TAGJ34234JK24

        # note: 'sdreducecol' filter must be disabled when using this format

        custom_dataset_template = sdpostpipelineutils.get_attached_parameter(f, 'local_path_drs_template')
        if custom_dataset_template is not None:
            keys = sdtools.extract_keys_from_template(custom_dataset_template)
            # check that only scalar facets are involved here
            # (i.e. we raise an exception if a facet is used in 'custom_dataset_template'
            # and contains more than one value)
            for key in keys:
                if key in f:
                    val = f[key]
                    if isinstance(val, list):
                        if len(val) == 0:
                            raise sdexception.SDException('SDLOCALP-018',
                                                          "'%s' key used in 'local_path_drs_template' but value missing "
                                                          "in file's attributes (%s,%s)" % (
                                                          key, f['dataset_functional_id'], val))
                        elif len(val) > 1:
                            raise sdexception.SDException('SDLOCALP-016',
                                                          "Only scalar value can be used in 'local_path_drs_template' "
                                                          "(%s,%s)" % (f['dataset_functional_id'], val))
                else:
                    raise sdexception.SDException('SDLOCALP-020',
                                                  "'%s' key used in 'local_path_drs_template' but value missing in "
                                                  "file's attributes (%s)" % (key, f['dataset_functional_id'],))

            # hack
            #
            # cast list to scalar if any
            #
            # this is needed when an attribute type is 'list' AND the attribute contains exactly one item.
            #
            # currently, it is used only for the following case:
            #     - we trigger CDF event for CORDEX dataset (ie which is a project with one var per dataset)
            #     - at TAGJ43KJ234JK, we build a dataset local path in a DATASET pipeline context,
            #       which mean that the variable attribute have the 'list' type (see sdpostxptransform for details)
            #     - so we solve this case here by casting list to scalar (this is ok because there is only
            #       one item in the dataset variable attribute with the CORDEX project (not true for every project)
            #
            values = {}
            for key in keys:
                values[key] = sdtools.scalar(f[key])

            path = custom_dataset_template % values
        else:
            raise SDException('SDLOCALP-014',
                              "'local_path_drs_template' must be set when 'local_path_format' is set to 'custom'.")

    elif fmt == "homemade":
        # note: 'sdreducecol' filter must be disabled when using this format
        path = local_path_homemade_transform(f)
    elif fmt == "notree":
        path = ""
    else:
        raise SDException('SDLOCALP-010', "'local_path_format' is incorrect ({})".format(fmt))
    return path
