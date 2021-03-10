# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.internal.models import Config as Internal

ALLOWED_HTTP_CLIENTS = ["wget", "urllib"]


def remove_not_allowed(choices, allowed):
    for choice in choices:
        if choice not in allowed:
            choices.remove(choice)


def validate_http_clients(choices):

    # remove not allowed requested choices

    remove_not_allowed(choices, ALLOWED_HTTP_CLIENTS)

    http_clients = dict(choices=ALLOWED_HTTP_CLIENTS)

    http_client_default = dict(
        default="wget",
    )

    if len(choices) > 0:
        choices = [choice.lower() for choice in choices]
        if "wget" in choices:
            http_clients["wget"] = "wget"
            http_clients.update(
                http_client_default,
            )

        if "urllib" in choices:
            http_clients["urllib"] = "urllib"
            if "default" not in list(http_clients.keys()):
                http_clients["default"] = "urllib"
    else:
        http_clients["wget"] = "wget"
        http_clients.update(
            http_client_default,
        )

    return http_clients


def get_http_clients(requested=Internal().processes_http_clients):

    return validate_http_clients(requested)

# PROTOCOLS


ALLOWED_TRANSFER_PROTOCOLS = ["http", "gridftp"]


def validate_transfer_protocols(choices):

    # remove not allowed requested choices

    remove_not_allowed(choices, ALLOWED_TRANSFER_PROTOCOLS)

    transfer_protocols = dict(choices=ALLOWED_TRANSFER_PROTOCOLS)

    transfer_protocols_default = dict(
        default="http",
    )

    if len(choices) > 0:

        choices = [choice.lower() for choice in choices]

        if "http" in choices:
            transfer_protocols["http"] = "http"
            transfer_protocols.update(
                transfer_protocols_default,
            )

        if "gridftp" in choices:
            transfer_protocols["gridftp"] = "gridftp"
            if "default" not in list(transfer_protocols.keys()):
                transfer_protocols["default"] = "gridftp"
    else:
        transfer_protocols["http"] = "http"
        transfer_protocols.update(
            transfer_protocols_default,
        )

    return transfer_protocols


def get_transfer_protocols(requested=Internal().processes_transfer_protocols):
    return validate_transfer_protocols(requested)


TRANSFER_STATUS_DELETE = "delete"
TRANSFER_STATUS_DONE = "done"
TRANSFER_STATUS_ERROR = "error"
TRANSFER_STATUS_NEW = "new"
TRANSFER_STATUS_PAUSE = "pause"
TRANSFER_STATUS_RUNNING = "running"
TRANSFER_STATUS_WAITING = "waiting"

TRANSFER_STATUSES_PENDING = [
    TRANSFER_STATUS_WAITING,
    TRANSFER_STATUS_RUNNING,
    TRANSFER_STATUS_ERROR,
    TRANSFER_STATUS_PAUSE,
]

TRANSFER_STATUSES_ALL = [TRANSFER_STATUS_NEW, TRANSFER_STATUS_DONE, TRANSFER_STATUS_DELETE] + TRANSFER_STATUSES_PENDING

TRANSFER = dict(
    statuses=dict(
        all=TRANSFER_STATUSES_ALL,
        pending=TRANSFER_STATUSES_PENDING,
    ),
    status=dict(
        new=TRANSFER_STATUS_NEW,
        waiting=TRANSFER_STATUS_WAITING,
        running=TRANSFER_STATUS_RUNNING,
        done=TRANSFER_STATUS_DONE,
        error=TRANSFER_STATUS_ERROR,
        delete=TRANSFER_STATUS_DELETE,
        pause=TRANSFER_STATUS_PAUSE,
    ),
)
