import torch


def get_torch_weights_from_lightning_checkpoint(checkpoint):
    """
    Used to load the weights of the encoder, when fine-tuning the transformers (supervised training part after the unsupervised)

    Parameters
    ----------
    checkpoint

    Returns
    -------
    Torch state dict
    """
    try:
        checkpoint = torch.load(checkpoint, map_location="cpu")
        state_dict = checkpoint["state_dict"]
        torch_state_dict = {}
        for k, v in state_dict.items():
            key = k[4:] if k.startswith("net.") else k
            torch_state_dict[key] = v
        return torch_state_dict
    except Exception:
        return None
