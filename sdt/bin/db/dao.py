from sdt.bin.db.models import Dataset
from sdt.bin.db.models import File
from sdt.bin.db.models import SelectionFile
from sdt.bin.db.models import Selection
from sdt.bin.db.models import FileWithoutSelection
from sdt.bin.db.models import FileWithoutDataset
from sdt.bin.db.models import Param
from sdt.bin.db.models import FailedUrl
from sdt.bin.db.session import query
from sdt.bin.db.session import add
from sdt.bin.db.session import create
from sdt.bin.db.session import raw_query

from sdt.bin.db import utils
from sdt.bin.sdconst import TRANSFER_STATUS_DELETE, TRANSFER_STATUS_ERROR, TRANSFER_STATUS_WAITING, \
    TRANSFER_STATUS_RUNNING
from sqlalchemy import text
from sqlalchemy import or_
from sqlalchemy import func
from sqlalchemy import distinct

# misc dependencies
import humanize


def get_datasets(limit=None, **criterion):
    """
    Note
        If 'limit' is None or <=0  retrieve all records matching the search constraints
    """
    datasets = []
    q = query(Dataset)
    q = q.filter_by(**criterion)
    if limit is None:
        datasets = q.all()
    elif limit > 0:
        datasets = q.limit(limit).all()
    return datasets


def get_max_version_datasets_groupby_criterion():
    return utils.dataset_groupby(Dataset, Dataset.path_without_version, Dataset.version)


def insert_datasets(dataset_list):
    """
    inserts into table Dataset.
    :param dataset_list: a list of dataset entities
    """
    for dataset in dataset_list:
        utils.insert(dataset)


def remove_datasets(dataset_list):
    """
    removes list of datasets from Dataset table.
    :param dataset_list: list of dataset entities
    """
    for dataset in dataset_list:
        utils.delete(dataset)


def remove_dataset_by_functional_id(functional_id_list):
    for func_id in functional_id_list:
        utils.delete_by_facet(dataset_functional_id=func_id)


def update_dataset(dataset_list):
    for dataset in dataset_list:
        utils.update(dataset)


def dataset_exists(**criterion):
    q = query(Dataset)
    q = q.filter_by(**criterion)
    datasets = q.all()
    if datasets is not None:
        return True
    else:
        return False


def mark_dataset_transfer_for_delete(dataset_list):
    for d in dataset_list:
        q = query(File)
        q = q.filter_by(dataset_id=d.dataset_id).update({'status': TRANSFER_STATUS_DELETE})
        # q = update(File).where(dataset_id=d.dataset_id).values(status=TRANSFER_STATUS_DELETE)


def get_files_marked_to_delete():
    q = query(File)
    q = q.filter_by(status=TRANSFER_STATUS_DELETE)
    return q.all()


def delete_file(f):
    q = query(File)
    q = q.filter_by(file_id=f.id)
    q.delete()


def retry_all():
    q = query(File)
    q = q.filter_by(status=TRANSFER_STATUS_ERROR).update({'status': TRANSFER_STATUS_WAITING, 'error_msg': None,
                                                          'sdget_status': None, 'sdget_error_msg': None})
    return q


def files_in_error():
    q = query(File)
    q = q.filter_by(status=TRANSFER_STATUS_ERROR)
    return q.count()


def fetch_parameters():
    """Retrieve all parameters
    Returns:
        params (dict)
    """
    params = {}
    q = query(Param)
    for p in q.all():
        if p.name in params:
            params[p.name].append(p.value)
        else:
            params[p.name] = [p.value]
    return params


def truncate_table(table):
    text("TRUNCATE TABLE {}".format(table))


def add_parameter(name, value=None):
    ignore_list = ['pid', 'citation_url']
    if name not in ignore_list:
        new_param = Param(name, value)
        add(new_param)


def exists_parameter_value(name, value):
    q = query(Param)
    q = q.filter_by(name=name, value=value)
    q = q.all()
    if len(q) == 1:
        return True
    elif len(q) == 0:
        return False


def exists_parameter_name(name):
    q = query(Param)
    q = q.filter_by(name=name)
    q = q.all()
    if len(q) == 1:
        return True
    elif len(q) == 0:
        return False


def get_files(limit=None, offset=None, **search_constraints):
    """
    Notes
      - one search constraint must be given at least
      - if 'limit' is None, retrieve all records matching the search constraints
    """
    q = query(File)
    q = q.filter_by(**search_constraints).order_by(File.priority.desc(), File.checksum)
    if limit is not None:
        q = q.limit(limit)
    if offset is not None:
        q = q.offset(offset)
    return q.all()


def update_file(file, next_url_on_error=False):
    # 'url' need to be present when 'sdnexturl' feature is enabled
    if not next_url_on_error:
        del file.url

    q = query(File)
    q = q.update(file)

    rowcount = len(q.all())
    # check
    if rowcount == 0:
        raise SDException("SYNCDDAO-121", "file not found (file_id={})".format(i__tr.file_id, ))
    elif rowcount > 1:
        raise SDException("SYNCDDAO-120", "duplicate functional primary key (file_id={})".format(i__tr.file_id, ))


def get_one_waiting_transfer(datanode=None):
    if datanode is None:
        li = get_files(limit=1, status=TRANSFER_STATUS_WAITING)
    else:
        li = get_files(limit=1, status=TRANSFER_STATUS_WAITING, data_node=datanode)
    if len(li) == 0:
        raise NoTransferWaitingException()
    else:
        t = li[0]

    # retrieve the dataset
    d = get_datasets(limit=1, dataset_id=t.dataset_id)
    t.dataset = d

    return t


def transfer_status_count(status=None):
    assert status is not None
    q = query(File)
    q = q.filter_by(status=status).all()
    return len(q)


def transfer_running_count():
    return transfer_status_count(status=TRANSFER_STATUS_RUNNING)


def transfer_running_count_by_datanode():
    # TODO probably second query is broken
    q = query(File)
    q = q.filter(or_(File.status == TRANSFER_STATUS_RUNNING, File.status == TRANSFER_STATUS_WAITING)).group_by(
        File.data_node)
    rcs = {r.data_node: 0 for r in q.all()}
    qry = raw_query(File.data_node, func.count(File.data_node))
    qry.having(File.status == TRANSFER_STATUS_RUNNING)
    qry.group_by(File.data_node)
    rcs.update({r[0]: r[1] for r in qry.all()})
    return rcs


def insert_into_failed_url(failed_url):
    """

    :param failed_url: FailedUrl entity
    :return:
    """
    utils.insert(failed_url)


def next_url():
    """
    From Jeff Painter's PR #90 on github.
    :return:
    """
    # construct FailedUrl entity
    failed_url = None
    # insert into table next failed_url (url, file_id)
    utils.insert(failed_url)
    # call next_url method.

    pass


def get_download_status(project=None):
    """
    returns file download status
    :param project: optional argument
    :return:
    """
    li = []
    qry = raw_query(File.status, func.count(File.file_id), func.sum(File.size))
    qry.group_by(File.status)
    if project is not None:
        qry.having(File.project == project)
    qry.all()
    for q in qry.all():
        li.append([q[0], q[1], humanize.naturalsize(q[2], gnu=False)])
    return li


def get_file_size_by_status(dataset_id):
    qry = raw_query(File.status, func.sum(File.size))
    qry.group_by(File.status)
    qry.having(File.dataset_id == dataset_id)
    return qry.all()


def get_file_count_by_status(dataset_id):
    qry = raw_query(File.status, func.count(File.file_id))
    qry.group_by(File.status)
    qry.having(File.dataset_id == dataset_id)
    return qry.all()


def get_file_count_variables(dataset_id):
    # -- how many variable, regardless of the file status -- #
    qry = raw_query(func.count(distinct(File.variable)))
    qry.filter(dataset_id == dataset_id)
    return qry.all()
