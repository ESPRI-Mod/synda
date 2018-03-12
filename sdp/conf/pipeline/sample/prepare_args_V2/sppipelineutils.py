#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS. All Rights Reserved€
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""
Contains post-processing pipeline utils.

"""

import os
import simplejson as json
from copy import copy
from collections import OrderedDict
import spconfig
import spconst
import splog


def set_path_type(kw):
    if kw.variable != '':
        kw.path_type = 'variable'
    else:
        kw.path_type = 'dataset'


def read_config(path):
    with open(path) as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def decode_dataset_pattern(kw):
    # Read JSON with DRS formats
    cfg = read_config('{0}/DRS.json'.format(spconfig.pipeline_folder))
    from_keys = cfg[kw.project]
    from_values = kw.dataset_pattern.strip('/').split('/')
    if kw.path_type == 'variable' and kw.project not in spconst.PROJECT_WITH_ONE_VARIABLE_PER_DATASET:
        from_values.append(kw.variable)
    elif kw.path_type == 'dataset':
        from_keys.remove('variable')
    assert len(from_keys) == len(from_values)
    from_facets = dict(zip(from_keys, from_values))
    assert kw.project == from_facets['project']
    return from_keys, from_values, from_facets


def get_args(self, kw):
    # Instantiate argument dict
    args = dict()
    args['project'] = kw.project
    # Set path type
    set_path_type(kw)
    # Set variable arg depending on path type (dataset or variable)
    if kw.path_type == 'dataset':
        args['variable'] = 'None'
    else:
        args['variable'] = kw.variable
    # Decode input dataset pattern
    decode_dataset_pattern(kw)
    from_keys, from_values, from_facets = decode_dataset_pattern(kw)
    # Read JSON with facets transition-specific
    # e.g., IPSL and IPSL_DATASET refer to the same IPSL.json
    cfg = read_config('{0}/{1}.json'.format(spconfig.pipeline_folder, kw.pipeline.split('_')[0]))
    if kw.variable in cfg[self.name][self.destination][kw.project].keys():
        attrs = cfg[self.name][self.destination][kw.project][kw.variable]
    else:
        attrs = cfg[self.name][self.destination][kw.project]
    # Build input/output directories
    for arg in ['input', 'output']:
        arg_dir = '{0}-dir'.format(arg)
        arg_drs = '{0}-drs'.format(arg)
        if attrs[arg_dir] is not None:
            to_facets = copy(from_facets)
            to_keys = copy(from_keys)
            for key in attrs[arg_dir].keys():
                att = attrs[arg_dir][key]
                if isinstance(att, list):
                    assert len(att) == 3
                    value, pos, rank = att
                    if pos == "before":
                        to_keys.insert(to_keys.index(rank), key)
                    elif pos == "after":
                        to_keys.insert(to_keys.index(rank) + 1, key)
                    if key == 'bias_adjustment' and kw.project == 'CORDEX':
                        to_keys.remove("rcm_version")
                        del to_facets["rcm_version"]
                        value = '{0}-{1}'.format(from_facets['rcm_version'], value)
                    to_facets.update({key: value})
                else:
                    if att == "remove":
                        to_keys.remove(key)
                        del to_facets[key]
                    else:
                        to_facets.update({key: att})
            args[arg_dir] = kw.data_folder
            args[arg_drs] = ""
            for key in to_keys:
                if to_facets[key] is not None:
                    args[arg_dir] = os.path.join(args[arg_dir], to_facets[key])
                    args[arg_drs] = os.path.join(args[arg_drs], key)
            # Add trailing slash mandatory for rsync command
            args[arg_dir] = os.path.join(args[arg_dir], '')
            args[arg_drs] = os.path.join(args[arg_drs], '')
    # Return argument dict
    return args
