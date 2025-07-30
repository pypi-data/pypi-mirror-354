# From https://github.com/kornia/kornia/blob/master/kornia/losses/focal.py
import torch


def one_hot(labels, num_classes, device=None, dtype=None, eps=1e-6):
    """Converts an integer label 2D tensor to a one-hot 3D tensor.

    Parameters
    ----------
    labels : torch.Tensor
        Tensor with labels of shape :math:`(N, H, W)`, where N is the batch size.
        Each value is an integer representing the correct classification.
    num_classes : int
        Number of classes in labels.
    device : torch.device, optional
        The desired device of returned tensor, by default None.
    dtype : torch.dtype, optional
        The desired data type of returned tensor, by default None.
    eps : float, optional
        Very small value to add to the encoding, so they are not exactly 0, by default 1e-6

    Returns
    -------
    torch.Tensor
        Labels as a 3D one-hot tensor.

    Raises
    ------
    TypeError
        If `labels` is not a `torch.tensor`.
    ValueError
        If `labels` number of dimensions is 1.
    ValueError
        If `labels` dtype is not `torch.int64`
    ValueError
        If `num_classes` is strictly less than 1.
    """

    if not torch.is_tensor(labels):
        raise TypeError("Input labels type is not a torch.Tensor. Got {}".format(type(labels)))
    if not len(labels.shape) == 1:
        raise ValueError("Invalid depth shape, we expect B. Got: {}".format(labels.shape))
    if not labels.dtype == torch.int64:
        raise ValueError("labels must be of the same dtype torch.int64. Got: {}".format(labels.dtype))
    if num_classes < 1:
        raise ValueError("The number of classes must be bigger than one." " Got: {}".format(num_classes))
    batch_size = labels.shape[0]
    one_h = torch.zeros(batch_size, num_classes, device=device, dtype=dtype)
    return one_h.scatter_(1, labels.unsqueeze(1), 1.0) + eps
