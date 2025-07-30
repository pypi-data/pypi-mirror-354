def compute_total_parameter_number(net):
    """
    Compute the total number of parameters of a network

    Parameters
    ----------
    net (nn.Module): the network

    Returns
    -------
    int: the number of parameters
    """
    return sum(param.clone().cpu().data.view(-1).size(0) for name, param in net.named_parameters())
