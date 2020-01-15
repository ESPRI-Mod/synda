#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains security related functions."""

import os
import argparse
import webbrowser
import json
import globus_sdk
import sdconfig
from sdtools import print_stderr


client_id = '83ec00c1-e67a-4356-9f1f-f7e31177e31a'
redirect_uri = 'https://auth.globus.org/v2/web/auth-code'
scopes = ('openid email profile '
          'urn:globus:auth:scope:transfer.api.globus.org:all')


try:
    input = raw_input
except NameError:
    pass


def load_tokens_from_file(filepath):
    """Load a set of saved tokens."""
    with open(filepath, 'r') as f:
        tokens = json.load(f)
    return tokens


def save_tokens_to_file(filepath, tokens):
    """Save a set of tokens for later use."""
    directory = os.path.dirname(filepath)
    if not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print_stderr("Could not create {} directory for a Globus OAuth2 token.\n{}".format(directory, e))
    with open(filepath, 'w') as f:
        json.dump(tokens, f)


def is_remote_session():
    return os.environ.get('SSH_TTY', os.environ.get('SSH_CONNECTION'))


def do_native_app_authentication(client_id, redirect_uri,
                                 requested_scopes=None):
    """
    Does a Native App authentication flow and returns a
    dict of tokens keyed by service name.
    """
    client = globus_sdk.NativeAppAuthClient(client_id=client_id)
    client.oauth2_start_flow(
            requested_scopes=requested_scopes,
            redirect_uri=redirect_uri,
            refresh_tokens=True)
    url = client.oauth2_get_authorize_url()
    print("Native App Authorization URL: \n{}".format(url))
    if not is_remote_session():
        webbrowser.open(url, new=1)
    auth_code = input("Enter the auth code: ").strip()
    token_response = client.oauth2_exchange_code_for_tokens(auth_code)
    # return a set of tokens, organized by resource server name
    return token_response.by_resource_server


def renew_tokens():
    tokens = do_native_app_authentication(
            client_id=client_id,
            redirect_uri=redirect_uri,
            requested_scopes=scopes)
    try:
        save_tokens_to_file(sdconfig.globus_tokens, tokens)
    except:
        pass


def print_tokens():
    try:
        tokens = load_tokens_from_file(sdconfig.globus_tokens)
        print(json.dumps(tokens, indent=4))
    except:
        print_stderr("Globus tokens not found (use 'renew' command to retrieve new tokens).")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    renew_tokens()

    print_stderr("Access/refresh tokens successfully renewed")
