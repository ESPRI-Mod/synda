from sdt.bin.db.models import Dataset
from sdt.bin.db.models import File
from sdt.bin.db.models import SelectionFile
from sdt.bin.db.models import Selection
from sdt.bin.db.models import FileWithoutSelection
from sdt.bin.db.models import FileWithoutDataset
from sdt.bin.db.session import query
from sdt.bin.db.session import update
from sdt.bin.db.session import raw_query
from sdt.bin.db import session
from sdt.bin.db import utils
from sdt.bin.sdconst import TRANSFER_STATUS_DELETE, TRANSFER_STATUS_ERROR, TRANSFER_STATUS_WAITING
from sqlalchemy import func


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
