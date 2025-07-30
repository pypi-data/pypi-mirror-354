# ######################################################################################################################
# DH Specific: Stripped to minimum
# ######################################################################################################################

"""Utilities to handle multiclass/multioutput target in classifiers."""

# Author: Arnaud Joly, Joel Nothman, Hamzeh Alsalhi
#
# License: BSD 3 clause

import warnings
from collections.abc import Sequence

import numpy as np
from scipy.sparse import issparse

from ..utils._array_api import get_namespace
from ..utils.fixes import VisibleDeprecationWarning
from .validation import _assert_all_finite, check_array


def _is_integral_float(y):
    xp, is_array_api_compliant = get_namespace(y)
    return xp.isdtype(y.dtype, "real floating") and bool(
        xp.all(xp.astype((xp.astype(y, xp.int64)), y.dtype) == y)
    )


def is_multilabel(y):
    """Check if ``y`` is in a multilabel format.

    Parameters
    ----------
    y : ndarray of shape (n_samples,)
        Target values.

    Returns
    -------
    out : bool
        Return ``True``, if ``y`` is in a multilabel format, else ```False``.

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.utils.multiclass import is_multilabel
    >>> is_multilabel([0, 1, 0, 1])
    False
    >>> is_multilabel([[1], [0, 2], []])
    False
    >>> is_multilabel(np.array([[1, 0], [0, 0]]))
    True
    >>> is_multilabel(np.array([[1], [0], [0]]))
    False
    >>> is_multilabel(np.array([[1, 0, 0]]))
    True
    """
    xp, is_array_api_compliant = get_namespace(y)
    if hasattr(y, "__array__") or isinstance(y, Sequence) or is_array_api_compliant:
        # DeprecationWarning will be replaced by ValueError, see NEP 34
        # https://numpy.org/neps/nep-0034-infer-dtype-is-object.html
        check_y_kwargs = dict(
            accept_sparse=True,
            allow_nd=True,
            force_all_finite=False,
            ensure_2d=False,
            ensure_min_samples=0,
            ensure_min_features=0,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("error", VisibleDeprecationWarning)
            try:
                y = check_array(y, dtype=None, **check_y_kwargs)
            except (VisibleDeprecationWarning, ValueError) as e:
                if str(e).startswith("Complex data not supported"):
                    raise

                # dtype=object should be provided explicitly for ragged arrays,
                # see NEP 34
                y = check_array(y, dtype=object, **check_y_kwargs)

    if not (hasattr(y, "shape") and y.ndim == 2 and y.shape[1] > 1):
        return False

    if issparse(y):
        if y.format in ("dok", "lil"):
            y = y.tocsr()
        labels = xp.unique_values(y.data)
        return (
            len(y.data) == 0
            or (labels.size == 1 or (labels.size == 2) and (0 in labels))
            and (y.dtype.kind in "biu" or _is_integral_float(labels))  # bool, int, uint
        )
    else:
        labels = xp.unique_values(y)

        return labels.shape[0] < 3 and (
            xp.isdtype(y.dtype, ("bool", "signed integer", "unsigned integer"))
            or _is_integral_float(labels)
        )


def type_of_target(y, input_name=""):
    """Determine the type of data indicated by the target.

    Note that this type is the most specific type that can be inferred.
    For example:

        * ``binary`` is more specific but compatible with ``multiclass``.
        * ``multiclass`` of integers is more specific but compatible with
          ``continuous``.
        * ``multilabel-indicator`` is more specific but compatible with
          ``multiclass-multioutput``.

    Parameters
    ----------
    y : {array-like, sparse matrix}
        Target values. If a sparse matrix, `y` is expected to be a
        CSR/CSC matrix.

    input_name : str, default=""
        The data name used to construct the error message.

        .. versionadded:: 1.1.0

    Returns
    -------
    target_type : str
        One of:

        * 'continuous': `y` is an array-like of floats that are not all
          integers, and is 1d or a column vector.
        * 'continuous-multioutput': `y` is a 2d array of floats that are
          not all integers, and both dimensions are of size > 1.
        * 'binary': `y` contains <= 2 discrete values and is 1d or a column
          vector.
        * 'multiclass': `y` contains more than two discrete values, is not a
          sequence of sequences, and is 1d or a column vector.
        * 'multiclass-multioutput': `y` is a 2d array that contains more
          than two discrete values, is not a sequence of sequences, and both
          dimensions are of size > 1.
        * 'multilabel-indicator': `y` is a label indicator matrix, an array
          of two dimensions with at least two columns, and at most 2 unique
          values.
        * 'unknown': `y` is array-like but none of the above, such as a 3d
          array, sequence of sequences, or an array of non-sequence objects.

    Examples
    --------
    >>> from sklearn.utils.multiclass import type_of_target
    >>> import numpy as np
    >>> type_of_target([0.1, 0.6])
    'continuous'
    >>> type_of_target([1, -1, -1, 1])
    'binary'
    >>> type_of_target(['a', 'b', 'a'])
    'binary'
    >>> type_of_target([1.0, 2.0])
    'binary'
    >>> type_of_target([1, 0, 2])
    'multiclass'
    >>> type_of_target([1.0, 0.0, 3.0])
    'multiclass'
    >>> type_of_target(['a', 'b', 'c'])
    'multiclass'
    >>> type_of_target(np.array([[1, 2], [3, 1]]))
    'multiclass-multioutput'
    >>> type_of_target([[1, 2]])
    'multilabel-indicator'
    >>> type_of_target(np.array([[1.5, 2.0], [3.0, 1.6]]))
    'continuous-multioutput'
    >>> type_of_target(np.array([[0, 1], [1, 1]]))
    'multilabel-indicator'
    """
    xp, is_array_api_compliant = get_namespace(y)
    valid = (
        (isinstance(y, Sequence) or issparse(y) or hasattr(y, "__array__"))
        and not isinstance(y, str)
        or is_array_api_compliant
    )

    if not valid:
        raise ValueError(
            "Expected array-like (array or non-string sequence), got %r" % y
        )

    sparse_pandas = y.__class__.__name__ in ["SparseSeries", "SparseArray"]
    if sparse_pandas:
        raise ValueError("y cannot be class 'SparseSeries' or 'SparseArray'")

    if is_multilabel(y):
        return "multilabel-indicator"

    # DeprecationWarning will be replaced by ValueError, see NEP 34
    # https://numpy.org/neps/nep-0034-infer-dtype-is-object.html
    # We therefore catch both deprecation (NumPy < 1.24) warning and
    # value error (NumPy >= 1.24).
    check_y_kwargs = dict(
        accept_sparse=True,
        allow_nd=True,
        force_all_finite=False,
        ensure_2d=False,
        ensure_min_samples=0,
        ensure_min_features=0,
    )

    with warnings.catch_warnings():
        warnings.simplefilter("error", VisibleDeprecationWarning)
        if not issparse(y):
            try:
                y = check_array(y, dtype=None, **check_y_kwargs)
            except (VisibleDeprecationWarning, ValueError) as e:
                if str(e).startswith("Complex data not supported"):
                    raise

                # dtype=object should be provided explicitly for ragged arrays,
                # see NEP 34
                y = check_array(y, dtype=object, **check_y_kwargs)

    try:
        # TODO(1.7): Change to ValueError when byte labels is deprecated.
        # labels in bytes format
        first_row_or_val = y[[0], :] if issparse(y) else y[0]
        if isinstance(first_row_or_val, bytes):
            warnings.warn(
                (
                    "Support for labels represented as bytes is deprecated in v1.5 and"
                    " will error in v1.7. Convert the labels to a string or integer"
                    " format."
                ),
                FutureWarning,
            )
        # The old sequence of sequences format
        if (
            not hasattr(first_row_or_val, "__array__")
            and isinstance(first_row_or_val, Sequence)
            and not isinstance(first_row_or_val, str)
        ):
            raise ValueError(
                "You appear to be using a legacy multi-label data"
                " representation. Sequence of sequences are no"
                " longer supported; use a binary array or sparse"
                " matrix instead - the MultiLabelBinarizer"
                " transformer can convert to this format."
            )
    except IndexError:
        pass

    # Invalid inputs
    if y.ndim not in (1, 2):
        # Number of dimension greater than 2: [[[1, 2]]]
        return "unknown"
    if not min(y.shape):
        # Empty ndarray: []/[[]]
        if y.ndim == 1:
            # 1-D empty array: []
            return "binary"  # []
        # 2-D empty array: [[]]
        return "unknown"
    if not issparse(y) and y.dtype == object and not isinstance(y.flat[0], str):
        # [obj_1] and not ["label_1"]
        return "unknown"

    # Check if multioutput
    if y.ndim == 2 and y.shape[1] > 1:
        suffix = "-multioutput"  # [[1, 2], [1, 2]]
    else:
        suffix = ""  # [1, 2, 3] or [[1], [2], [3]]

    # Check float and contains non-integer float values
    if xp.isdtype(y.dtype, "real floating"):
        # [.1, .2, 3] or [[.1, .2, 3]] or [[1., .2]] and not [1., 2., 3.]
        data = y.data if issparse(y) else y
        if xp.any(data != xp.astype(data, int)):
            _assert_all_finite(data, input_name=input_name)
            return "continuous" + suffix

    # Check multiclass
    if issparse(first_row_or_val):
        first_row_or_val = first_row_or_val.data
    if xp.unique_values(y).shape[0] > 2 or (y.ndim == 2 and len(first_row_or_val) > 1):
        # [1, 2, 3] or [[1., 2., 3]] or [[1, 2]]
        return "multiclass" + suffix
    else:
        return "binary"  # [1, 2] or [["a"], ["b"]]
