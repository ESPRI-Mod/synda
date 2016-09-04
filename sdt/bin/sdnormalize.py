#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains model normalization functions.

Example
     'CESM1(CAM5.1,FV2)' become 'CESM1-CAM5-1-FV2'
"""

import string
import sdapp
import sdconst
import sdexception

def normalize_model_name(model_name):
    """Replace special characters with hyphen.

    Model names differ from search-API and DRS. text below described the mapping rule between both naming spaces

        i.e.
            this returns row
                http://esgf-index1.ceda.ac.uk/esg-search/search?model=CESM1%28CAM5.1,FV2%29
            this does not
                http://esgf-index1.ceda.ac.uk/esg-search/search?model=CESM1-CAM5-1-FV2

    Spec from http://cmip-pcmdi.llnl.gov/cmip5/docs/CMIP5_output_metadata_requirements.pdf

        <model> should be identical to model_id, one of the global attributes described
        in a subsequent section, except that the following characters, if they appear
        in model_id should be replaced by a hyphen (i.e., by '-'):

        _ ( ) . ; , [ ] : / * ? < > " ' { } & and/or a “space”. 

        If, after substitution, any hyphens are found at the end of the string, they should be removed.

    See below for official model names list

        The official model names are shown at
        http://cmip-pcmdi.llnl.gov/cmip5/availability.html and in the document
        http://cmip-pcmdi.llnl.gov/cmip5/docs/CMIP5_modeling_groups.pdf, reachable from
        various places on the CMIP5 website.
    """

    # translate special characters
    #
    # Note:
    #   - str() func is used to prevent this error: 'Reason: character mapping must return integer, None or unicode'
    #     (from details at http://stackoverflow.com/questions/10367302/what-is-producing-typeerror-character-mapping-must-return-integer-in-this-p)
    #
    mode_name_without_special_character=str(model_name).translate(string.maketrans("""_().;,[]:/*?<>"'"{}& """, "---------------------"))

    # remove last hyphen if any
    if mode_name_without_special_character[-1] == "-":
        normalized_mode_name=mode_name_without_special_character[:-1] # remove last hyphen
    else:
        normalized_mode_name=mode_name_without_special_character

    return normalized_mode_name

def normalize_checksum_type(checksum_type):

    if checksum_type is None:
        return None
    elif "md5" in checksum_type.lower():
        return sdconst.CHECKSUM_TYPE_MD5
    elif 'sha' in checksum_type.lower() and '256' in checksum_type:
        return sdconst.CHECKSUM_TYPE_SHA256
    elif checksum_type=='None':
        return None
    else:
        raise sdexception.UnknownChecksumType("SDNORMAL-001","Unknown checksum type (%s)"%(checksum_type,))
