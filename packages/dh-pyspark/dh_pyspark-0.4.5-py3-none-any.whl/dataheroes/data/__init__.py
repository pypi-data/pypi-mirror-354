from .common import (
    DataParams,
    FeatureField, IndexField, TargetField,
    DefaultIndexField, SeqIndexField,
    get_working_directory,
    Dataset
)
from .sql import DataManagerSqlite
from .hdf5 import DataManagerHDF5
from .manager import DataManagerBase, DataManagerMem
from ..utils import user_warning
from .common import DataParams

# DefaultDataManager = DataManagerSqlite
DefaultDataManager = DataManagerHDF5


def resolve_manager_cls(name):
    try:
        return eval(name) if name else None
    except BaseException as e:
        try:
            user_warning(str(e))
        except:
            pass
    return None
