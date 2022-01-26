# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import asyncio
import humanize
import numpy as np

from synda.sdt import sdtime
from synda.sdt.sdtools import print_stderr

from synda.source.process.subcommand.required.env.models import Process as Base

from synda.source.process.subcommand.get.constants import VERIFY_CHECKSUM_ERROR

from synda.source.process.subcommand.get.constants import RENEW_CERTIFICATE_ERROR

from synda.source.process.subcommand.get.constants import CONFIG_CREDENTIALS_ERROR
from synda.source.process.subcommand.get.constants import CONFIG_OPENID_CREDENTIALS_ERROR

from synda.source.process.subcommand.get.constants import CLI_CREDENTIALS_ERROR
from synda.source.process.subcommand.get.constants import CLI_OPENID_CREDENTIALS_ERROR

from synda.source.config.file.downloading.models import Config as File
from synda.source.config.file.user.credentials.models import validate_openid


def downloads_validated(verbosity):
    from synda.sdt import sdutils

    confirmed = False
    if verbosity:
        if sdutils.query_yes_no('Do you want to continue?', default="yes"):
            confirmed = True
    else:
        print_stderr("Download(s) in progress...")
        confirmed = True
    return confirmed


class Process(Base):

    def __init__(self, payload):
        super(Process, self).__init__("get", payload)
        self.pid_file = File()
        self.args = None

    def create_downloading_file(self):
        # First, we create a file that contains the pid of the current process
        # The existence of this particular file is the proof that a downloading process is in progress
        self.pid_file.set_content(f"{os.getpid()}")

    def delete_downloading_file(self):
        error = self.pid_file.delete()

    def overwrite_verbosity(self):
        if self.args.quiet:
            self.args.verbosity = not self.args.quiet

    def validate(self):
        validated = self.validate_network_bandwidth_test()
        if validated:
            oid, pwd = self.validate_credentials()
            validated = oid and pwd
            if validated:
                validated = self.renew_certificate(oid, pwd)
        return validated

    def validate_credentials_set_by_cli(self):
        validated = True if self.args.openid and self.args.password else False
        if validated:
            oid = self.args.openid
            pwd = self.args.password
            if oid:
                openid_validated = validate_openid(oid)
                if not openid_validated:
                    print_stderr(
                        f'{CLI_OPENID_CREDENTIALS_ERROR} ({oid}).',
                    )
                    oid = ""
        else:
            print_stderr(
                f'{CLI_CREDENTIALS_ERROR}.',
            )
            oid = ""
            pwd = ""
        return oid, pwd

    def validate_credentials_set_by_config(self):
        oid = ""
        credentials = self.get_payload().get_authority().get_user_credentials()
        credentials_file = credentials.get()
        try:
            oid = credentials.openid
            pwd = credentials.password
        except Exception as e:
            oid = ""
            pwd = ""
            print_stderr(
                f'{CONFIG_CREDENTIALS_ERROR} ({credentials_file}) Error message : {str(e)}.',
            )
        finally:
            if oid:
                openid_validated = validate_openid(oid)
                if not openid_validated:
                    oid = ""
                    print_stderr(
                        f'{CONFIG_OPENID_CREDENTIALS_ERROR} ({credentials_file}).',
                    )

        return oid, pwd

    def validate_credentials(self):
        # Credentials can be set by CLI (Command Line Interface) or by config file (credentials.conf)
        are_credentials_set_by_cli = True if self.args.openid or self.args.password else False
        if are_credentials_set_by_cli:
            oid, pwd = self.validate_credentials_set_by_cli()
        else:
            oid, pwd = self.validate_credentials_set_by_config()

        return oid, pwd

    def validate_network_bandwidth_test(self):
        checked = True
        if self.args.verify_checksum and self.args.network_bandwidth_test:
            print_stderr(VERIFY_CHECKSUM_ERROR)
            checked = False

        return checked

    def renew_certificate(self, oid, pwd):
        from synda.sdt import sdlogon
        # retrieve certificate
        checked = sdlogon.renew_certificate(
            oid,
            pwd,
            force_renew_certificate=False,
        )
        # for tests only
        # checked = False
        if not checked:
            print_stderr(
                RENEW_CERTIFICATE_ERROR,
            )

        return checked

    def get_files_from_urls(self, urls):
        files = []
        for url in urls:
            if self.args.network_bandwidth_test:
                local_path = '/dev/null'
            else:
                filename = os.path.basename(url)
                local_path = filename

            f = dict(local_path=local_path, url=url)

            files.append(f)
        return files

    def get_files_from_stream(self, stream):
        from synda.sdt import sdrfile
        from synda.sdt import sddeferredafter

        # no url in stream: switch to search-api operator mode
        sddeferredafter.add_forced_parameter(stream, 'local_path_format', 'notree')

        # yes: this is the second time we run sdinference filter, but it doesn't hurt as sdinference is idempotent
        files = sdrfile.get_files(
            stream=stream,
            post_pipeline_mode='file',
            dry_run=self.args.dry_run,
        )

        return files

    def inform_about_downloads_unknown_weight(self, files):
        print_stderr(
            '{} file(s) will be downloaded (from url total size can not be estimated).'.format(
                len(files),
            ),
        )

    def inform_about_downloads_weight(self, files):
        if len(files) > 0:
            if not self.args.dry_run:
                # compute metric
                total_size = sum(int(f['size']) for f in files)
                total_size = humanize.naturalsize(total_size, gnu=False)

                print_stderr(
                    '{} file(s) will be downloaded for a total size of {}.'.format(
                        len(files),
                        total_size,
                    ),
                )
            else:
                for f in files:
                    size = humanize.naturalsize(f['size'], gnu=False)
                    print(
                        '%-12s %s'.format(
                            size,
                            f['filename'],
                        ),
                    )

    def validate_args_when_parameter_are_urls(self):
        return False if self.args.verify_checksum else True

    def get_db_file_instances(self, files):
        from synda.sdt.sdtypes import File
        if self.args.dest_folder is None:
            # current working directory
            local_path_prefix = os.getcwd()
        else:
            local_path_prefix = self.args.dest_folder

        db_files = []
        for file_ in files:
            # check
            assert 'url' in file_
            assert 'local_path' in file_

            # cast
            f = File(**file_)
            f.local_path = f.get_full_local_path(prefix=local_path_prefix)

            # check
            download_required = True
            if not self.args.network_bandwidth_test:
                if os.path.isfile(f.local_path):
                    if self.args.force:
                        os.remove(f.local_path)
                    else:
                        download_required = False
                        print_stderr(
                            'Warning: download cancelled as local file already exists ({})'.format(
                                f.local_path,
                            ),
                        )
            if download_required:
                f.start_date = sdtime.now()
                db_files.append(f)
        return db_files

    def choose_uniq_files(self, files):
        from synda.sdt import sdutils
        ufiles = []
        local_paths = [file["local_path"] for file in files]
        file_functional_ids = [file["file_functional_id"] for file in files]
        w_local_paths = np.array(local_paths)
        w_file_functional_ids = np.array(file_functional_ids)
        unique, counts = np.unique(local_paths, return_counts=True)
        for local_path, count in zip(unique, counts):
            indexes = np.where(w_local_paths == local_path)[0]
            if count > 1:
                question = "Which file do you want to download ?"
                user_message = "Several files found"
                items = w_file_functional_ids[indexes]
                choice = sdutils.which_item(question, items, user_message)
                if choice > -1:
                    ufiles.append(files[indexes[choice]])
            else:
                ufiles.append(files[indexes[0]])
        return ufiles

    def run(self, args):
        from synda.sdt import syndautils
        from synda.sdt import sdearlystreamutils
        self.args = args

        self.overwrite_verbosity()
        validated = self.validate()

        if validated:
            stream = syndautils.get_stream(
                subcommand=self.args.subcommand,
                parameter=self.args.parameter,
                selection_file=self.args.selection_file,
            )
            # BEWARE
            #
            # when set in CLI parameter, url is usually an ESGF facet, and as so should
            # be sent to the search-api as other facets
            # BUT
            # we want a special behaviour here (i.e. with 'synda get' command) with url:
            # if url is set by user, we DON'T call search-api operator. Instead, we
            # download the url directly.

            urls = sdearlystreamutils.get_facet_values_early(stream, 'url')
            search_api_call_required = len(urls) == 0

            files = []
            if search_api_call_required:
                # url(s) not found in stream => search-api operator needed
                files = self.get_files_from_stream(stream)
                files = self.choose_uniq_files(files)
                self.inform_about_downloads_weight(files)
            else:
                # url(s) found in stream: search-api operator not needed (download url directly)
                validated = self.validate_args_when_parameter_are_urls()
                if validated:
                    files = self.get_files_from_urls(urls)
                    self.inform_about_downloads_unknown_weight(files)
                else:
                    print_stderr(
                        "To perform checksum verification, "
                        "ESGF file identifier (e.g. title, id, tracking id..)  must be used instead of file url.",
                    )

            if validated and files:
                # Some downloads have been found
                if downloads_validated(self.args.verbosity):
                    db_file_instances = self.get_db_file_instances(files)
                    # prepare attributes
                    if db_file_instances:
                        do_post_download_controls = False if \
                            self.args.network_bandwidth_test else self.args.verify_checksum
                        # Run the downloading process
                        from synda.source.process.asynchronous.download.subcommand.get.scheduler.models import scheduler
                        from synda.source.process.asynchronous.download.subcommand.get.task.provider.models import \
                            Provider as TaskProvider
                        task_provider = TaskProvider(db_file_instances)
                        config = dict(
                            do_post_download_controls=do_post_download_controls,
                            verbosity=args.verbosity,
                        )

                        asyncio.run(
                            scheduler(
                                task_provider,
                                config=config,
                                verbose=False,
                                build_report=False,
                            )
                        )
                        # self.delete_downloading_file()
            else:
                print_stderr("File not found")


        return 0
