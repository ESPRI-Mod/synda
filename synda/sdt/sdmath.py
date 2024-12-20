#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains math routines."""

from synda.sdt import sdapp
import itertools
import operator

def monotone_increasing(lst):
    pairs = list(zip(lst, lst[1:]))
    return all(itertools.starmap(operator.le, pairs))

def monotone_decreasing(lst):
    pairs = list(zip(lst, lst[1:]))
    return all(itertools.starmap(operator.ge, pairs))

def monotone(lst):
    """
    from http://stackoverflow.com/questions/4983258/python-how-to-check-list-monotonicity
    """

    return monotone_increasing(lst) or monotone_decreasing(lst)
