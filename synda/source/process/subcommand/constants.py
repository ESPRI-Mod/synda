# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.subcommand.constants import DEFAULT_LIMITS

from synda.source.config.subcommand.constants import NAMES as SUB_COMMAND_NAMES

from synda.source.process.subcommand.exceptions import ProcessNotImplemented

from synda.source.process.subcommand.autoremove.models import Process as AutoRemove
from synda.source.process.subcommand.certificate.models import Process as Certificate
from synda.source.process.subcommand.check.models import Process as Check
from synda.source.process.subcommand.config.models import Process as Config
from synda.source.process.subcommand.contact.models import Process as Contact
from synda.source.process.subcommand.checkenv.models import Process as CheckEnv
from synda.source.process.subcommand.initenv.models import Process as InitEnv
from synda.source.process.subcommand.help.models import Process as Help
from synda.source.process.subcommand.api.esgf_search.count.models import Process as Count

from synda.source.process.subcommand.download.models import Process as Download
from synda.source.process.subcommand.dump.models import Process as Dump
from synda.source.process.subcommand.facet.models import Process as Facet
from synda.source.process.subcommand.get.models import Process as Get
from synda.source.process.subcommand.getinfo.models import Process as GetInfo
from synda.source.process.subcommand.history.models import Process as History
from synda.source.process.subcommand.install.models import Process as Install
from synda.source.process.subcommand.intro.models import Process as Intro
from synda.source.process.subcommand.list.models import Process as List
from synda.source.process.subcommand.metric.models import Process as Metric
from synda.source.process.subcommand.param.models import Process as Param
from synda.source.process.subcommand.queue.models import Process as Queue
from synda.source.process.subcommand.remove.models import Process as Remove
from synda.source.process.subcommand.replica.models import Process as Replica
from synda.source.process.subcommand.reset.models import Process as Reset
from synda.source.process.subcommand.retry.models import Process as Retry
from synda.source.process.subcommand.search.models import Process as Search
from synda.source.process.subcommand.selection.models import Process as Selection
from synda.source.process.subcommand.show.models import Process as Show
from synda.source.process.subcommand.stat.models import Process as Stat
from synda.source.process.subcommand.update.models import Process as Update
from synda.source.process.subcommand.upgrade.models import Process as Upgrade
from synda.source.process.subcommand.variable.models import Process as Variable
from synda.source.process.subcommand.version.models import Process as Version
from synda.source.process.subcommand.watch.models import Process as Watch
from synda.source.process.subcommand.synda_version.models import Process as SyndaVersion


def get_default_limit(name):
    default_limits_mode = Preferences().interface_default_listing_size
    return DEFAULT_LIMITS[default_limits_mode][name]


def get_process_class(name):

    if name not in SUB_COMMAND_NAMES:
        raise ProcessNotImplemented(name)
    else:
        if name == "autoremove":
            process = AutoRemove
        elif name == "certificate":
            process = Certificate
        elif name == "check":
            process = Check
        elif name == "check-env":
            process = CheckEnv
        elif name == "config":
            process = Config
        elif name == "contact":
            process = Contact
        elif name == "count":
            process = Count
        elif name == "download":
            process = Download
        elif name == "dump":
            process = Dump
        elif name == "facet":
            process = Facet
        elif name == "get":
            process = Get
        elif name == "getinfo":
            process = GetInfo
        elif name == "help":
            process = Help
        elif name == "history":
            process = History
        elif name == "init-env":
            process = InitEnv
        elif name == "install":
            process = Install
        elif name == "intro":
            process = Intro
        elif name == "list":
            process = List
        elif name == "metric":
            process = Metric
        elif name == "help":
            process = Help
        elif name == "param":
            process = Param
        elif name == "queue":
            process = Queue
        elif name == "remove":
            process = Remove
        elif name == "replica":
            process = Replica
        elif name == "reset":
            process = Reset
        elif name == "retry":
            process = Retry
        elif name == "search":
            process = Search
        elif name == "selection":
            process = Selection
        elif name == "show":
            process = Show
        elif name == "stat":
            process = Stat
        elif name == "update":
            process = Update
        elif name == "upgrade":
            process = Upgrade
        elif name == "variable":
            process = Variable
        elif name == "version":
            process = Version
        elif name == "synda_version":
            process = SyndaVersion
        elif name == "watch":
            process = Watch
        else:
            raise ProcessNotImplemented(name)

    return process
