import os
import subprocess
import datetime
import concurrent.futures
import time

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

from synda.sdt import sdlog
from synda.sdt import sdlogon

from synda.source.process.asynchronous.download.scheduler.models import get_batches

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.user.credentials.models import Config as Credentials
from synda.source.config.file.certificate.x509.models import Config as SecurityFile
esgf_x509_proxy = SecurityFile().get_credentials()

credentials = Credentials()
preferences = Preferences()


def renew_certificate():
    try:
        sdlogon.renew_certificate(
            credentials.openid,
            credentials.password,
            force_renew_certificate=True,
        )

    except Exception as e:
        sdlog.error(
            "SDDMDEFA-502",
            "Exception occured while retrieving certificate ({})".format(e),
        )


def get_status_output2(args, **kwargs):
    index = args[0]
    local_path = args[1]
    url = args[2]
    total_expected_size = args[3]
    output = ''
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    kwargs['universal_newlines'] = False
    kwargs['shell'] = False

    args = [
        '/home_local/journoud/DEV/WORKSPACES/synda/bin/sdget.sh', '-p', '0', '-l',
        '/home_local/journoud/DEV/WORKSPACES/synda/log', '-T', '/home_local/journoud/DEV/WORKSPACES/synda/tmp',
        '-t', '120', '-c', '/home_local/journoud/DEV/WORKSPACES/synda/tmp/1000/.esg',
        u'{}'.format(url),
        u'{}'.format(local_path),
    ]

    downloaded_so_far = 0
    begin = datetime.datetime.now()
    process = subprocess.Popen(args, **kwargs)

    stdout, stderr = process.communicate()
    exit_code = process.returncode

    end = datetime.datetime.now()
    elapsed = end - begin
    speed = (downloaded_so_far // elapsed.total_seconds()) // 1024
    result = {
        "index": index,
        "download speed": speed,
        "file size": total_expected_size,
        "elapsed time": elapsed.total_seconds(),
        "start": begin.strftime(DATE_FORMAT),
        "finish": end.strftime(DATE_FORMAT),
        "strategy": "current32",
        "status_code": exit_code,
        "local_path": local_path,
    }
    print(result)

    if exit_code == 0:
        return exit_code, stdout, stderr
    else:
        print(exit_code)
        pass
        raise Exception(args, exit_code, stdout)


def execute(args):

    with concurrent.futures.ThreadPoolExecutor(max_workers=8, thread_name_prefix="download-task-thread") as executor:
        results = executor.map(get_status_output2, args)
        # for result in results:
        #     print('\t', result)


if __name__ == '__main__':
    batches = get_batches()
    batch = batches[0]
    urls = []
    relative_paths = []
    sizes = []
    for download in batch:
        urls.append(download.url)
        relative_paths.append(download.local_path)
        sizes.append(download.size)

    local_paths = [os.path.join(os.path.join(os.environ["ST_HOME"], "data"), relative_path) for relative_path in relative_paths]

    args = [(index, local_path, url, total_expected_size) for index, local_path, url, total_expected_size in zip(range(len(urls)), local_paths, urls, sizes)]

    strategy = "current32"

    start_time = time.monotonic()
    execute(args)
