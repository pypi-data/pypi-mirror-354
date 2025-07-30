import torch

from hyptorch.config import NumericalConstants


def norm(tensor: torch.Tensor, *, safe: bool = False) -> torch.Tensor:
    """
    Compute the L2 norm of tensors along the last dimension.

    This function computes the Euclidean norm (L2 norm) of input tensors,
    with an optional safety mechanism to prevent division by zero in
    subsequent operations.

    Parameters
    ----------
    tensor : torch.Tensor
        Input tensor of any shape (..., dim).
    safe : bool, optional
        If True, clamps the norm to be at least MIN_NORM_THRESHOLD to
        prevent numerical issues. Default is False. This is keyword-only.

    Returns
    -------
    torch.Tensor
        L2 norm along the last dimension. Shape (..., 1).
        The last dimension is kept for broadcasting compatibility.
    """
    norm = torch.linalg.norm(tensor, dim=-1, keepdim=True)
    if safe:
        return torch.clamp_min(norm, NumericalConstants.MIN_NORM_THRESHOLD)
    return norm


def squared_norm(tensor: torch.Tensor) -> torch.Tensor:
    """
    Compute the squared L2 norm of tensors along the last dimension.

    This function computes the squared Euclidean norm, which is more
    efficient than computing the norm when the square root is not needed.

    Parameters
    ----------
    tensor : torch.Tensor
        Input tensor of any shape

    Returns
    -------
    torch.Tensor
        Squared L2 norm along the last dimension.
        The last dimension is kept for broadcasting compatibility.
    """
    return torch.sum(tensor.pow(2), dim=-1, keepdim=True)


def dot_product(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """
    Compute the dot product between tensors along the last dimension.

    This function computes the inner product (dot product) between
    corresponding vectors in two tensors, handling arbitrary batch dimensions.

    Parameters
    ----------
    x : torch.Tensor
        First input tensor.
    y : torch.Tensor
        Second input tensor. Must have the same shape as x.

    Returns
    -------
    torch.Tensor
        Dot product along the last dimension. Shape (..., 1).
        The last dimension is kept for broadcasting compatibility.
    """
    return torch.sum(x * y, dim=-1, keepdim=True)
