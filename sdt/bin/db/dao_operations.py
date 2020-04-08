import os
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy.sql import label

from sdt.bin.db import session
from sdt.bin.db import dao
from sdt.bin.db import models

from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdexception

from sdt.bin.commons.search import sdquicksearch
from sdt.bin.models.sdtypes import DatasetVersions

"""
This module contains functions that mainly interact with db but are not DAO operations per se. 
The idea is to remove the clutter from dao.py and keep it sqlalchemy operations only all while keeping these
operations in the same vicinity.
"""


def delete_transfers(limit=None, remove_all=True):
    """Perform the deletion of METADATA.

    Returns
        how many files with TRANSFER_STATUS_DELETE status remain

    Notes
        - Can be called from the daemon code (deferred mode), or from
          interactive code (immediate mode).
        - 'limit' is used to delete only a subset of all files marked for
          deletion each time this func is called. If 'limit' is None,
          all files marked for deletion are removed.
    """
    with session.create():
        transfer_list = dao.get_files(status=sdconst.TRANSFER_STATUS_DELETE, limit=limit)
    try:
        for tr in transfer_list:
            if remove_all:
                immediate_delete(tr)
            else:
                immediate_md_delete(tr)
    except Exception as e:
        sdlog.error("SDDELETE-880", "Error occurs during files suppression ({})".format(str(e), ))
        raise  # fatal error
    with session.create():
        transfer_count = dao.transfer_status_count(status=sdconst.TRANSFER_STATUS_DELETE)
    return transfer_count


def immediate_delete(tr):
    """Delete file (metadata and data).

    Notes
        - This method remove files but not directories (directories are removed in "cleanup.sh" script)
    """
    sdlog.info("SDDELETE-055", "Delete transfer ({})".format(tr.get_full_local_path()))

    if os.path.isfile(tr.get_full_local_path()):
        try:
            os.remove(tr.get_full_local_path())
            # note: if data cannot be removed (i.e. exception is raised), we don't remove metadata
            with session.create():
                dao.delete_file(tr)

        except Exception as e:
            sdlog.error("SDDELETE-528",
                        "Error occurs during file suppression ({},{})".format(tr.get_full_local_path(), str(e)))
            raise
    else:
        if tr.status == sdconst.TRANSFER_STATUS_DONE:
            # this case is not normal as the file should exist on filesystem when status is done

            sdlog.error("SDDELETE-123", "Can't delete file: file not found ({})".format(tr.get_full_local_path()))
        else:
            # this case is for 'waiting' and 'error' status (in these cases, data do not exist, so we just remove metadata)
            with session.create():
                dao.delete_file(tr)


def immediate_md_delete(tr):
    """Delete file (metadata only)."""
    sdlog.info("SDDELETE-080", "Delete metadata ({})".format(tr.get_full_local_path()))
    try:
        with session.create():
            dao.delete_file(tr)
    except Exception as e:
        sdlog.error("SDDELETE-128",
                    "Error occurs during file metadata suppression ({},{})".format(tr.get_full_local_path(), str(e)))


def next_url(tr):
    """
    Returns
    True: url has been switched to a new one
    False: nothing changed (same url)
    """
    # Fetch all url and protocols
    urlps = get_urls(tr.file_functional_id)
    # Fetch all urls that have failed for the file id in question
    failed_urls = None
    # Filter urlps from already tried and failed urlps
    urlps = urlps - failed_urls
    # Remove unsupported protocols
    urls = remove_unsupported_urls(urlps)
    # switch tr url with the first element if the urlps list
    if len(urls) > 0:
        old_url = tr.url
        # (highest priority of non attempted urls with supported protocol)
        new_url = urls[0]
        tr.url = new_url
        sdlog.info('SDNEXTUR-008', 'URL successfully switched (file functional id = {}, old url = {}, new url = {}'.
                   format(tr.file_function_id, old_url, new_url))
    else:
        sdlog.info('SDNEXTUR-009', 'Next URL not found for file function id = {}'.format(tr.file_functional_id))
        raise sdexception.NextUrlNotFoundException


def remove_unsupported_urls(urlps):
    """
    Cleans the list of urls & protocols from unsupported items
    :param urlps:
    :return:
    """
    return [urlp[0] for urlp in urlps if urlp[1].find('opendap') < 0]


def get_urls(file_functional_id):
    """
    Uses search api to retrieve a list of urls, prioritized, associated to a given file functional identifier.
    :param file_functional_id:
    :return:
    """
    try:
        result = sdquicksearch.run(parameter=['limit=4', 'fields={}'.format(url_fields), 'type=File',
                                              'instance_id={}'.format(file_functional_id)], post_pipeline_mode=None)
    except Exception as e:
        sdlog.debug("SDNEXTUR-015", "exception %s.  instance_id=%s" % (e, file_functional_id))
        raise e

    li = result.get_files()
    sdlog.info("SDNEXTUR-016", "sdquicksearch returned %s sets of file urls: %s" % (len(li), li))
    if li == []:
        # No urls found. Try again, but wildcard the file id. (That leads to a string search on all
        # fields for the wildcarded file id, rather than a match of the instance_id field only.)
        result = sdquicksearch.run(parameter=['limit=4', 'fields={}'.format(url_fields), 'type=File',
                                              'instance_id={}'.format(file_functional_id) + '*'],
                                   post_pipeline_mode=None)
        li = result.get_files()
        sdlog.info("SDNEXTUR-017", "sdquicksearch 2nd call {} sets of file urls: {}".format(len(li), li))
    # result looks like
    # [ {protocol11:url11, protocol12:url12, attached_parameters:dict, score:number, type:'File',
    #    size:number} }, {[another dict of the same format}, {another dict},... ]
    # with no more than limit=4 items in the list, and no more than three protocols.
    # We'll return something like urlps = [ [url1,protocol1], [url2,protocol2],... ]
    # The return value could be an empty list.
    # Note: These nested lists are ugly; it's just a quick way to code something up.
    urlps = []
    for dic in li:
        urlps += [[dic[key], key] for key in dic.keys() if key.find('url_') >= 0 and dic[key].find('//None') < 0]
        # ... protocol keys are one of 'url_opendap', 'url_http', 'url_gridftp'
        # The search for //None bypasses an issue with the SOLR lookup where there is no
        # url_gridftp possibility.
    return prioritize_urlps(urlps)


def prioritize_urlps(urlps):
    """Orders a list urlps so that the highest-priority urls come first.  urlps is a list of
    lists of the form [url,protocol].  First, GridFTP urls are preferred over everything else.
    Then, prefer some data nodes over others."""

    def priprotocol(protocol):
        if protocol.find('gridftp') > 0:  return 0
        if protocol.find('http') > 0:     return 1
        return 2

    def priurl(url):
        if url.find('llnl') > 0:  return 0
        if url.find('ceda') > 0:  return 1
        if url.find('dkrz') > 0:  return 2
        if url.find('ipsl') > 0:  return 3
        if url.find('nci') > 0:   return 4
        return 5

    return sorted(urlps, key=(lambda urlp: (priprotocol(urlp[1]), priurl(urlp[0]))))


def get_dataset_versions(path_without_version, compute_stats):
    """
    Returns DatasetVersions object for a specified path_without_version
    :param path_without_version: string
    :param compute_stats: boolean
    """
    datasetVersions = DatasetVersions()
    with session.create():
        datasets = get_datasets(path_without_version=path_without_version)
    for dataset in datasets:
        if compute_stats:
            dataset.statistics = get_dataset_stats(dataset)
            datasetVersions.add_dataset_version(dataset)
    return datasetVersions


def get_dataset_stats(d):
    stat = {}
    stat['size'] = {}
    stat['count'] = {}

    # init everything to zero
    for status in sdconst.TRANSFER_STATUSES_ALL:
        stat['size'][status] = 0
        stat['count'][status] = 0
        stat['variable_count'] = 0

    with session.create():
        # -- size by status -- #
        sizes_by_status = dao.get_file_size_by_status(d.dataset_id)
        for sbs in sizes_by_status:
            stat['size'][sbs[0]] = sbs[1]

        # -- count by status -- #
        count_by_status = dao.get_file_count_by_status(d.dataset_id)
        for cbs in count_by_status:
            stat['count'][cbs[0]] = cbs[1]

        # -- how many variable, regardless of the file status -- #
        count = dao.get_file_count_variables(d.dataset_id)
        stat['variable_count'] = count
        return stat


def get_old_versions_datasets():
    """Return old versions datasets list."""
    lst = []
    with session.create():
        for d in dao.get_datasets():
            datasetVersions = get_dataset_versions(d.path_without_version, True)
            if d.latest == False:  # this version is not the latest
                if datasetVersions.exists_version_with_latest_flag_set_to_true():  # latest exists
                    if not datasetVersions.is_version_higher_than_latest(d):  # version is not higher than latest
                        # should never occurs because of the previous tests
                        if datasetVersions.is_most_recent_version_number(d):
                            raise sdexception.SDException("SDSTAT-042",
                                                          "fatal error (version={},path_without_version={})"
                                                          .format(d.version, d.get_name_without_version()))
                        lst.append(d)
    return lst


def get_metrics(group_string_id, metric, project_, dry_run=False):
    li = []
    # check
    assert group_string_id in ['data_node', 'project', 'model']
    assert metric in ('rate', 'size')
    # WARNING: we don't check project_ for sql injection here.
    # This MUST be done in the calling func. TODO: check for sql injection here
    # prepare metric calculation
    group = {
        'data_node': models.File.data_node,
        'project': models.File.project,
        'model': models.File.model,
    }
    # creating db session
    with session.create():
        # Adding the group constraint if a group is selected
        # Adding the metric requested by user as a filter.
        if metric == 'rate':
            query = session.raw_query(group[group_string_id], label('metric', func.avg(models.File.rate)))
        elif metric == 'size':
            query = session.raw_query(group[group_string_id], label('metric', func.sum(models.File.size)))
        query = query.filter(models.File.rate.isnot(None))
        query = query.filter(models.File.size.isnot(None))
        if group_string_id == 'model':
            query = query.filter_by(project=project_)
        query = query.order_by(desc('metric'))
        query = query.group_by(group[group_string_id])
        if group_string_id == 'project':
            query = query.filter_by(models.File.project)
        # if dry_run, simply print out the generated query and return an empty list.
        if dry_run:
            print('{}'.format(str(query)))
            return []
        qry = query.all()
        for rs in qry:
            group_column_value = rs[0]
            metric_column_value = rs[1]
            li.append((group_column_value, metric_column_value))
        return li
