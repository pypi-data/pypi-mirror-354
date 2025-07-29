import copy

import torch

from ttfemesh.types import TensorTrain


def zorder_kron(left: TensorTrain, right: TensorTrain) -> TensorTrain:
    """
    Compute the Kronecker product of two TT-tensors using the Z-ordering
    (a.k.a. *transposed* or *level-wise* ordering).
    The ordering is column-major, i.e., for every index z in the resulting tensor,
    the relationship to index (i, j) in the left and right tensors is: z = i + j * 2.
    This is consistent with the little-endian ordering of the binary index
    commonly used in QTT literature.

    Args:
        left (TensorTrain): Left TT-tensor.
        right (TensorTrain): Right TT-tensor.

    Returns:
        TensorTrain resulting from the Kronecker product of left and right.

    Raises:
        ValueError: If the TT-length of left and right tensors are not equal.
    """

    cores_left = left.cores
    cores_right = right.cores

    if len(cores_left) != len(cores_right):
        raise ValueError(
            f"TT-length of left ({len(cores_left)})"
            f" and right ({len(cores_right)}) tensors must be equal."
        )

    cores = [torch.kron(b, a) for a, b in zip(cores_left, cores_right)]

    return TensorTrain(cores)


def zorder_linfunc2d(c: float, cx: float, X: TensorTrain, cy: float, Y: TensorTrain) -> TensorTrain:
    """
    Compute the linear combination of two TT-tensors using the Z-ordering
    (a.k.a. *transposed* or *level-wise* ordering):
    c + cx * X + cy * Y.
    Note that both X and Y must be of the same TT-length and have at least rank 2.

    Args:
        c (float): Scalar constant.
        cx (float): Scalar factor for X.
        X (TensorTrain): First TT-tensor.
        cy (float): Scalar factor for Y.
        Y (TensorTrain): Second TT-tensor.

    Returns:
        TensorTrain resulting from the linear combination of c, X, and Y.

    Raises:
        ValueError: If X and Y have different TT-lengths or ranks smaller than 2.
    """

    X_cores, Y_cores = X.cores, Y.cores
    if len(X_cores) != len(Y_cores):
        raise ValueError("X and Y must have the same TT-length.")

    ranks_X, ranks_Y = X.R, Y.R
    for i in range(1, len(ranks_X) - 1):
        if ranks_X[i] == 1:
            raise ValueError("X must have at least rank 2.")
        if ranks_Y[i] == 1:
            raise ValueError("Y must have at least rank 2.")

    result = copy.deepcopy(X_cores)
    result[0][:, :, 0] = cx * X_cores[0][:, :, 0] + cy * Y_cores[0][:, :, 0]
    result[-1][1, :, :] = cx * X_cores[-1][1, :, :] + (c + cy * Y_cores[-1][1, :, :])

    d = len(result)
    for k in range(1, d - 1):
        result[k][1, :, 0] = cx * X_cores[k][1, :, 0] + cy * Y_cores[k][1, :, 0]

    return TensorTrain(result)


# Aliases
transpose_kron = zorder_kron
levelwise_kron = zorder_kron
