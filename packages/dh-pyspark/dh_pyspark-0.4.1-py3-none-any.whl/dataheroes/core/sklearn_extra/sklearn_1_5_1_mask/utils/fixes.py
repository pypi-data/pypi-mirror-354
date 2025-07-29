# ######################################################################################################################
# DH Specific: Stripped to minimum
# ######################################################################################################################

"""Compatibility fixes for older version of python, numpy and scipy

If you add content to this file, please give the version of the package
at which the fix is no longer needed.
"""

# Authors: Emmanuelle Gouillart <emmanuelle.gouillart@normalesup.org>
#          Gael Varoquaux <gael.varoquaux@normalesup.org>
#          Fabian Pedregosa <fpedregosa@acm.org>
#          Lars Buitinck
#
# License: BSD 3 clause

import numpy as np

from ..externals._packaging.version import parse as parse_version


np_version = parse_version(np.__version__)

def _object_dtype_isnan(X):
    return X != X


# For +1.25 NumPy versions exceptions and warnings are being moved
# to a dedicated submodule.
if np_version >= parse_version("1.25.0"):
    from numpy.exceptions import ComplexWarning, VisibleDeprecationWarning
else:
    from numpy import ComplexWarning, VisibleDeprecationWarning  # type: ignore  # noqa


# TODO: remove when SciPy 1.12 is the minimum supported version
def _preserve_dia_indices_dtype(
    sparse_container, original_container_format, requested_sparse_format
):
    """Preserve indices dtype for SciPy < 1.12 when converting from DIA to CSR/CSC.

    For SciPy < 1.12, DIA arrays indices are upcasted to `np.int64` that is
    inconsistent with DIA matrices. We downcast the indices dtype to `np.int32` to
    be consistent with DIA matrices.

    The converted indices arrays are affected back inplace to the sparse container.

    Parameters
    ----------
    sparse_container : sparse container
        Sparse container to be checked.
    requested_sparse_format : str or bool
        The type of format of `sparse_container`.

    Notes
    -----
    See https://github.com/scipy/scipy/issues/19245 for more details.
    """
    if original_container_format == "dia_array" and requested_sparse_format in (
        "csr",
        "coo",
    ):
        if requested_sparse_format == "csr":
            index_dtype = _smallest_admissible_index_dtype(
                arrays=(sparse_container.indptr, sparse_container.indices),
                maxval=max(sparse_container.nnz, sparse_container.shape[1]),
                check_contents=True,
            )
            sparse_container.indices = sparse_container.indices.astype(
                index_dtype, copy=False
            )
            sparse_container.indptr = sparse_container.indptr.astype(
                index_dtype, copy=False
            )
        else:  # requested_sparse_format == "coo"
            index_dtype = _smallest_admissible_index_dtype(
                maxval=max(sparse_container.shape)
            )
            sparse_container.row = sparse_container.row.astype(index_dtype, copy=False)
            sparse_container.col = sparse_container.col.astype(index_dtype, copy=False)


# TODO: remove when SciPy 1.12 is the minimum supported version
def _smallest_admissible_index_dtype(arrays=(), maxval=None, check_contents=False):
    """Based on input (integer) arrays `a`, determine a suitable index data
    type that can hold the data in the arrays.

    This function returns `np.int64` if it either required by `maxval` or based on the
    largest precision of the dtype of the arrays passed as argument, or by the their
    contents (when `check_contents is True`). If none of the condition requires
    `np.int64` then this function returns `np.int32`.

    Parameters
    ----------
    arrays : ndarray or tuple of ndarrays, default=()
        Input arrays whose types/contents to check.

    maxval : float, default=None
        Maximum value needed.

    check_contents : bool, default=False
        Whether to check the values in the arrays and not just their types.
        By default, check only the types.

    Returns
    -------
    dtype : {np.int32, np.int64}
        Suitable index data type (int32 or int64).
    """

    int32min = np.int32(np.iinfo(np.int32).min)
    int32max = np.int32(np.iinfo(np.int32).max)

    if maxval is not None:
        if maxval > np.iinfo(np.int64).max:
            raise ValueError(
                f"maxval={maxval} is to large to be represented as np.int64."
            )
        if maxval > int32max:
            return np.int64

    if isinstance(arrays, np.ndarray):
        arrays = (arrays,)

    for arr in arrays:
        if not isinstance(arr, np.ndarray):
            raise TypeError(
                f"Arrays should be of type np.ndarray, got {type(arr)} instead."
            )
        if not np.issubdtype(arr.dtype, np.integer):
            raise ValueError(
                f"Array dtype {arr.dtype} is not supported for index dtype. We expect "
                "integral values."
            )
        if not np.can_cast(arr.dtype, np.int32):
            if not check_contents:
                # when `check_contents` is False, we stay on the safe side and return
                # np.int64.
                return np.int64
            if arr.size == 0:
                # a bigger type not needed yet, let's look at the next array
                continue
            else:
                maxval = arr.max()
                minval = arr.min()
                if minval < int32min or maxval > int32max:
                    # a big index type is actually needed
                    return np.int64

    return np.int32
