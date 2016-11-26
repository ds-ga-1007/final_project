
from collections import Iterable


def _make_op_dict(ops, callback):
    # Convert a dict of column-ops into column-functions with op-function
    # converter @callback
    # TODO: better documentation
    opdict = {}
    for k, v in ops.items():
        opdict[k] = callback(v)
    return opdict


def _make_op_list(ops, callback):
    # Convert a list of ops into functions with op-function converter
    # @callback
    # TODO: better documentation
    oplist = []
    for op in ops:
        oplist.append(callback(op))
    return oplist


def _make_op(ops, callback):
    # Convert a single element or an iterable of elements into functions
    # according to @callback function.
    # @callback is a function which takes an argument of arbitrary type
    # and returns a function (or raises errors)
    if isinstance(ops, dict):
        return _make_op_dict(ops, callback)
    elif isinstance(ops, Iterable) and not isinstance(ops, str):
        return _make_op_list(ops, callback)
    else:
        return callback(ops)


def _apply_op(ops, dataset, name, callback):
    # Apply an operation to the entire dataset or a list of operations
    # per-column.
    if isinstance(ops, Iterable):
        if isinstance(ops, dict):
            pairs = ops.items()
        elif len(dataset.columns) != len(ops):
            raise ValueError(
                    'number of columns does not match that of %s' % name
                    )
        else:
            pairs = zip(dataset.columns, ops)

        for c, op in pairs:
            callback(dataset, c, op)
    else:
        for c in dataset.columns:
            callback(dataset, c, ops)
    return dataset
