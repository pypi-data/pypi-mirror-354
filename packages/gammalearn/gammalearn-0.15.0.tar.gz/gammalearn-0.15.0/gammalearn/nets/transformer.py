from collections import OrderedDict
from typing import Tuple

import torch
import torch.nn as nn
from torchvision.models.vision_transformer import EncoderBlock
from typing_extensions import deprecated

from gammalearn.data.image_processing.patchification import (
    get_patch_indices_and_centroids_from_geometry,
    get_patch_indices_and_grid,
)
from gammalearn.nets.checkpointing import get_torch_weights_from_lightning_checkpoint
from gammalearn.nets.domain_adaptation import GradientLayer
from gammalearn.nets.positional_embedding import (
    get_2d_sincos_pos_embedding_from_grid,
    get_2d_sincos_pos_embedding_from_patch_centroids,
)


class BaseMaskedAutoEncoder(nn.Module):
    """
    Auto-encoder model for a transformer model. This is a base class that doesn't implement the positional encoding computation.
    It is specialized to compute the positional encoding on hexagonal or square grids.
    Implementation of
    https://openaccess.thecvf.com/content/CVPR2022/papers/He_Masked_Autoencoders_Are_Scalable_Vision_Learners_CVPR_2022_paper.pdf
    Widely inspired from https://github.com/facebookresearch/mae
    This generic implementation allows to implement an LST and a classical Vision Transformer. The LST implementation
    expect a hegaxonal grid of pixel whereas the image implementation required an input image interpolated on a regular
    grid. As it is the only difference between both implementations, only the position_embedding procedure differs and
    must be overwritten.
    """

    def __init__(self, net_parameters_dic):
        super(BaseMaskedAutoEncoder, self).__init__()
        self.net_parameters_dic = net_parameters_dic
        self.add_token_list = net_parameters_dic["backbone"]["parameters"]["add_token_list"]
        self.mask_ratio = net_parameters_dic["backbone"]["parameters"]["mask_ratio"]
        self.add_pointing = net_parameters_dic["backbone"]["parameters"]["add_pointing"]
        self.norm_pixel_loss = net_parameters_dic["norm_pixel_loss"]

    def position_embedding(self, embed_dim: int) -> torch.Tensor:
        """
        The generic function to override. This function is set as generic because the LST images and the vision images
        have different geometries, thus the positional embedding computation differs.
        Compute the positional embedding. The positional embedding adds spatial information to the image tokens. As it
        is possible to add additional tokens that does not belong to the image, it is also necessary to give them a
        positional embedding but 'far' (in terms of distance) from the image tokens.
        """
        raise NotImplementedError()

    def initialize_mae(self) -> None:
        """
        The initialization of the MAE is a three steps procedure:
        1. Initialization of the encoder
        2. Initialization of the decoder
        3. Initialization of the weights of the network.
        """
        self._initialize_encoder()
        self._initialize_decoder()
        self._initialize_weights()

    def _initialize_encoder(self) -> None:
        """
        Initialization of the encoder.
        """
        # STEP 1: Fetch parameters from the model settings dictionary
        # Define the dimension of the embedding. A classical value defined in the ViT article is 512 for 214x214 images.
        encoder_embed_dim = self.net_parameters_dic["backbone"]["parameters"]["embed_dim"]
        # Define the number of channel of the input images. In the case of LST, we have the pixel charge and peak time.
        encoder_num_channels = self.net_parameters_dic["backbone"]["parameters"]["num_channels"]
        # Define the number of transformers (encoder) block.
        encoder_blocks = self.net_parameters_dic["backbone"]["parameters"]["blocks"]
        # Define the ratio that allows to compute the number of weights (training parameters) in the MLP entity (after
        # the encoder).
        encoder_mlp_ratio = self.net_parameters_dic["backbone"]["parameters"]["mlp_ratio"]
        # Define the number of heads.
        encoder_heads = self.net_parameters_dic["backbone"]["parameters"]["heads"]

        # STEP 2: Compute the encoder positional embedding
        # Get positional embedding. It contains the additional tokens that are defined in the model settings. The
        # positional embedding will be added to the image projection. It can be computed directly as it will remain the
        # same through the whole training.
        pos_emb, patch_size = self.position_embedding(encoder_embed_dim)
        # Even though the positional embedding is constant, set it as a parameter so that PyTorch can set it on the
        # proper device.
        self.pos_embedding = nn.Parameter(pos_emb, requires_grad=False)  # torch.Size([n_tokens, embed_dim])
        self.pos_embedding.unsqueeze_(0)  # torch.Size([1, n_tokens, embed_dim]), unsqueeze to add to batch
        if self.add_token_list:
            # The tokens must be learned, so 'requires_grad' must be set to True
            self.additional_tokens = nn.Parameter(torch.zeros(1, len(self.add_token_list), encoder_embed_dim))

        # STEP 3: Define the model modules
        # Define the number of weights in the MLP as n_weights_mlp = encoder_mlp_ratio * encoder_embed_dim
        encoder_mlp_dim = encoder_embed_dim * encoder_mlp_ratio
        if self.add_pointing:
            # If the pointing direction is added as a token, project it using a Linear layer
            self.pointing_projection = nn.Linear(in_features=2, out_features=encoder_embed_dim)
        # Input projection can be defined using convolution. Furthermore, as the positions of the LST module are
        # following each other, the projection also allows to do the patchification.
        self.patch_projection = nn.Conv1d(
            in_channels=encoder_num_channels, out_channels=encoder_embed_dim, kernel_size=patch_size, stride=patch_size
        )
        self.encoder = nn.Sequential(
            OrderedDict(
                [
                    (
                        "enc_block_{}".format(i),
                        EncoderBlock(
                            num_heads=encoder_heads,
                            hidden_dim=encoder_embed_dim,
                            mlp_dim=encoder_mlp_dim,
                            dropout=0,
                            attention_dropout=0,
                            norm_layer=nn.LayerNorm,
                        ),
                    )
                    for i in range(encoder_blocks)
                ]
            )
        )
        self.encoder_norm = nn.LayerNorm(encoder_embed_dim)

    def _initialize_decoder(self) -> None:
        """
        Initialization of the decoder.
        """
        # STEP 1: Fetch parameters from the model settings dictionary
        # Define the dimension of the encoder embedding. A classical value defined in the ViT article is 512.
        encoder_embed_dim = self.net_parameters_dic["backbone"]["parameters"]["embed_dim"]
        # Define the number of channel of the input images. In the case of LST, we have the pixel charge and peak time.
        encoder_num_channels = self.net_parameters_dic["backbone"]["parameters"]["num_channels"]
        # Define the dimension of the decoder embedding. In the ViT article, it is the same as the encoder embedding.
        decoder_embed_dim = self.net_parameters_dic["decoder"]["parameters"]["embed_dim"]
        # Define the number of transformers (decoder) block.
        decoder_blocks = self.net_parameters_dic["decoder"]["parameters"]["blocks"]
        # Define the ratio that allows to compute the number of weights in the MLP.
        decoder_mlp_ratio = self.net_parameters_dic["decoder"]["parameters"]["mlp_ratio"]
        # Define the number of heads.
        decoder_heads = self.net_parameters_dic["decoder"]["parameters"]["heads"]

        # STEP 2: Compute the decoder positional embedding
        self.mask_token = nn.Parameter(torch.zeros(1, 1, decoder_embed_dim))
        dec_pos_emb, patch_size = self.position_embedding(decoder_embed_dim)
        # Even though the positional embedding is constant, set it as a parameter so that PyTorch can set it on the
        # proper device.
        self.decoder_pos_embedding = nn.Parameter(dec_pos_emb, requires_grad=False)
        self.decoder_pos_embedding.unsqueeze_(0)

        # STEP 3: Define the model modules
        # Define the number of weights in the MLP as n_weights_mlp = decoder_mlp_ratio * decoder_embed_dim
        decoder_mlp_dim = decoder_embed_dim * decoder_mlp_ratio
        self.decoder_embedding = nn.Linear(encoder_embed_dim, decoder_embed_dim)
        self.decoder = nn.Sequential(
            OrderedDict(
                [
                    (
                        "enc_block_{}".format(i),
                        EncoderBlock(
                            num_heads=decoder_heads,
                            hidden_dim=decoder_embed_dim,
                            mlp_dim=decoder_mlp_dim,
                            dropout=0,
                            attention_dropout=0,
                            norm_layer=nn.LayerNorm,
                        ),
                    )
                    for i in range(decoder_blocks)
                ]
            )
        )
        self.decoder_norm = nn.LayerNorm(decoder_embed_dim)
        self.decoder_prediction = nn.Linear(decoder_embed_dim, patch_size * encoder_num_channels)

    def _initialize_weights(self) -> None:
        """
        Initialization of the weights of the model.
        """
        # Init projection embedding like Linear instead of Conv
        nn.init.xavier_uniform_(self.patch_projection.weight.data)

        if self.add_token_list:
            nn.init.normal_(self.additional_tokens, std=0.02)
        nn.init.normal_(self.mask_token, std=0.02)

        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(m) -> None:
        if isinstance(m, nn.Linear):
            # We use xavier_uniform following official JAX ViT:
            torch.nn.init.xavier_uniform_(m.weight)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    def patchify(self, images: torch.Tensor) -> torch.Tensor:
        """
        images:  (N, C, image_length)
        x: (N, L, patch_size * C)
        """
        batch, channels, img_size = images.shape
        num_patches, patch_size = self.patch_indices.shape
        assert img_size % patch_size == 0, "the image must be divisible by patch size"
        x = images.reshape(batch, channels, num_patches, patch_size)
        x = torch.einsum("ncmp->nmpc", x)
        x = torch.reshape(x, (batch, num_patches, channels * patch_size))
        return x

    def unpatchify(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (N, L, patch_size * C)
        images:  (N, C, image_length)
        """
        batch, seq_len, token_size = x.shape
        num_patches, patch_size = self.patch_indices.shape
        assert seq_len == num_patches
        assert token_size % patch_size == 0
        num_channels = token_size // patch_size
        x = x.reshape(batch, num_patches, patch_size, num_channels)
        x = torch.einsum("nmpc->ncmp", x)
        images = x.reshape(batch, num_channels, patch_size * num_patches)
        return images

    @staticmethod
    def apply_random_mask(
        tokens: torch.Tensor, mask_ratio: float | torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Perform per-sample random masking by per-sample shuffling.
        Per-sample shuffling is done by argsort random noise.
        tokens: [N, L, D], sequence
        mask_ratio: the ratio of image to discard
        """
        batch, seq_len, token_size = tokens.shape
        len_keep = int(seq_len * (1 - mask_ratio))
        noise = torch.rand(batch, seq_len, device=tokens.device)
        # sort noise for each sample
        ids_shuffle = torch.argsort(noise, dim=1)  # ascend: small is kept, large is removed
        ids_restore = torch.argsort(ids_shuffle, dim=1)
        # keep the first subset
        ids_keep = ids_shuffle[:, :len_keep]
        masked_tokens = torch.gather(tokens, dim=1, index=ids_keep.unsqueeze(-1).repeat(1, 1, token_size))
        # generate the binary mask: 0 is kept, 1 is removed
        mask = torch.ones([batch, seq_len], device=tokens.device)
        mask[:, :len_keep] = 0
        # unshuffle to get the binary mask
        mask = torch.gather(mask, dim=1, index=ids_restore)
        return masked_tokens, mask, ids_restore

    def _unmask_tokens(self, tokens: torch.Tensor, ids_restore: torch.Tensor) -> torch.Tensor:
        """
        Unmask the tokens before feeding the decoder. The mask_token is shared across all the masked position
        tokens: tokens computed on the selected image patches by the encoder and projected in the decoder embedding size
        ids_restore: ids to restore token order as is before masking
        """
        batch, token_seq, token_size = tokens.shape
        seq_len = ids_restore.shape[1]
        # append mask tokens to sequence
        mask_tokens = self.mask_token.repeat(batch, seq_len - token_seq, 1)
        unmasked_tokens = torch.cat([tokens, mask_tokens], dim=1)
        # unshuffle
        unmasked_tokens = torch.gather(
            unmasked_tokens, dim=1, index=ids_restore.unsqueeze(-1).repeat(1, 1, token_size)
        )
        return unmasked_tokens

    def forward_encoder(
        self, images: torch.Tensor, pointing: torch.Tensor = None
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # Embed image patches (project them into a new representation to be learned)
        x = self.patch_projection(images)  # torch.Size([batch_size, encoder_embed_dim, n_patches])
        x = x.transpose(1, 2)  # torch.Size([batch_size, n_patches, encoder_embed_dim])
        tot_add_token_len = len(self.add_token_list) + 1 if self.add_pointing else len(self.add_token_list)

        # Add positional embedding
        x = x + self.pos_embedding[:, tot_add_token_len:, :]

        # Random masking of the image tokens
        x, mask, ids_restore = self.apply_random_mask(x, self.mask_ratio)

        # Append additional tokens and add their positional embedding
        # self.pos_emvedding contains the positional embedding concatenated with anything added in self.position_embedding()
        # for instance the pointing information or the pedestal mean value could be concatenated
        if self.add_token_list:
            add_tokens = self.additional_tokens + self.pos_embedding[:, : len(self.add_token_list), :]
            add_tokens = add_tokens.expand(x.shape[0], -1, -1)
            x = torch.cat((add_tokens, x), dim=1)

        # Append telescope pointing token and add its positional embedding
        if self.add_pointing:
            assert pointing is not None
            point_token = self.pointing_projection(pointing.unsqueeze(1))
            point_token = (
                point_token + self.pos_embedding[:, len(self.add_token_list) : len(self.add_token_list) + 1, :]
            )
            x = torch.cat((point_token, x), dim=1)

        # Transformer encoder
        x = self.encoder(x)
        x = self.encoder_norm(x)
        return x, mask, ids_restore

    def forward_decoder(self, tokens: torch.Tensor, ids_restore: torch.Tensor) -> torch.Tensor:
        # Embed tokens (project them into a new representation to be learned)
        x = self.decoder_embedding(tokens)

        # Unmask tokens
        tot_add_token_len = len(self.add_token_list) + 1 if self.add_pointing else len(self.add_token_list)
        x_image = self._unmask_tokens(x[:, tot_add_token_len:, :], ids_restore)

        # Append additional tokens
        x = torch.cat([x[:, :tot_add_token_len], x_image], dim=1)

        # Add pos embedding
        x = x + self.decoder_pos_embedding

        # Transformer decoder
        x = self.decoder(x)
        x = self.decoder_norm(x)

        # Predict pixels
        x = self.decoder_prediction(x)

        # Remove additional tokens
        if self.add_pointing:
            x = x[:, len(self.add_token_list) + 1 :, :]
        else:
            x = x[:, len(self.add_token_list) :, :]

        return x

    def forward_loss(self, images: torch.Tensor, predictions: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """
        We compute the loss only for the patches that were discarded (and thus reconstructed) during the masking
        operation.
        images: [N, C, D]
        predictions: [N, L, p*C]
        mask: [N, L], 0 is keep, 1 is remove,
        """
        targets = self.patchify(images)
        if self.norm_pixel_loss:
            # normalize the input pixels per module
            mean = targets.mean(dim=-1, keepdim=True)
            var = targets.var(dim=-1, keepdim=True)
            targets = (targets - mean) / (var + 1e-6) ** 0.5
        # loss per patch
        loss = (predictions - targets) ** 2
        loss = loss.mean(dim=-1)
        # keep only masked patches
        loss = (loss * mask).sum() / mask.sum()
        return loss

    def forward(self, images: torch.Tensor, pointing: torch.Tensor = None) -> torch.Tensor:
        """
        Parameters
        ----------
        images: (torch.Tensor) For LST, torch.Size([batch_size, num_channels, 1855])
        pointing: (torch.Tensor) torch.Size([batch_size, 2])
        Returns
        -------
        loss: (torch.Tensor) Scalar
        """
        latent_tokens, mask, ids_restore = self.forward_encoder(images, pointing)
        predictions = self.forward_decoder(latent_tokens, ids_restore)
        loss = self.forward_loss(images, predictions, mask)
        return loss


@deprecated("Transformers using interpolated images are deprecated and will be removed in a future release!")
class ImageMaskedAutoEncoder(BaseMaskedAutoEncoder):
    """Transformer model that computes positional embedding on interpolated images"""

    def __init__(self, net_parameters_dic):
        super(ImageMaskedAutoEncoder, self).__init__(net_parameters_dic)

        image_size = net_parameters_dic["backbone"]["parameters"]["image_size"]
        self.patch_size = net_parameters_dic["backbone"]["parameters"]["patch_size"]
        self.patch_indices, self.grid = get_patch_indices_and_grid(image_size, self.patch_size)

        self.initialize_mae()

    def position_embedding(self, embed_dim: int) -> Tuple[torch.Tensor, int]:
        """
        Compute the positional embedding. The positional embedding adds spatial information to the image tokens. As it
        is possible to add additional tokens that does not belong to the image, it is also necessary to give them a
        positional embedding but 'far' (in terms of distance) from the image tokens.
        """
        pos_emb = get_2d_sincos_pos_embedding_from_grid(self.grid, embed_dim, self.add_token_list, self.add_pointing)

        return pos_emb, self.patch_size * self.patch_size


class LSTMaskedAutoEncoder(BaseMaskedAutoEncoder):
    """Transformer model that computes positional embedding on square grids"""

    def __init__(self, net_parameters_dic):
        super(LSTMaskedAutoEncoder, self).__init__(net_parameters_dic)

        # The geometry is injected in the net_parameters_dic via utils.inject_geometry_into_parameters in
        # experiment_runner.py. Therefore, it must not be specified in the experiment setting file.
        geom = net_parameters_dic["backbone"]["parameters"]["camera_geometry"]
        self.patch_indices, self.patch_centroids = get_patch_indices_and_centroids_from_geometry(geom)
        self.patch_size = self.patch_indices.shape[-1]

        self.initialize_mae()

    def position_embedding(self, embed_dim):
        """
        Compute the positional embedding. The positional embedding adds spatial information to the image tokens. As it
        is possible to add additional tokens that does not belong to the image, it is also necessary to give them a
        positional embedding but 'far' (in terms of distance) from the image tokens.
        """
        pos_emb = get_2d_sincos_pos_embedding_from_patch_centroids(
            self.patch_centroids, embed_dim, self.add_token_list, self.add_pointing
        )

        return pos_emb, self.patch_size


class GammaPhysNetPrime(LSTMaskedAutoEncoder):
    """
    Implementation of
    https://openaccess.thecvf.com/content/CVPR2022/papers/He_Masked_Autoencoders_Are_Scalable_Vision_Learners_CVPR_2022_paper.pdf
    Widely inspired from https://github.com/facebookresearch/mae
    for LST

    This is the model that takes a encoder from a trained auto-encoder, adds the token tasks and can be fine tuned for predicitions of supervised tasks.
    """

    def __init__(self, net_parameters_dic: dict):
        super().__init__(net_parameters_dic)
        encoder_embed_dim = net_parameters_dic["backbone"]["parameters"]["embed_dim"]
        encoder_weights = net_parameters_dic["backbone"]["parameters"].get("weights", None)
        freeze_weights = net_parameters_dic["backbone"]["parameters"].get("freeze_weights", False)

        # --------------------------------------------------------------------------------------------------------------
        # Decoder
        # We create one linear layer by task, predicting directly from the corresponding tokens
        self.targets = net_parameters_dic["targets"].keys()
        for t, output_size in net_parameters_dic["targets"].items():
            self.add_module(t, nn.Linear(encoder_embed_dim, output_size))

        self.decoder = None
        self.decoder_pos_embedding = None
        self.decoder_embedding = None
        self.decoder_prediction = None
        self.mask_token = None
        self.decoder_norm = None
        # --------------------------------------------------------------------------------------------------------------

        if encoder_weights is not None:
            encoder_weights = get_torch_weights_from_lightning_checkpoint(encoder_weights)
            self.load_pretrained_weights(encoder_weights)

        if freeze_weights:
            self.freeze_pretrained_weights(encoder_weights)

    def load_pretrained_weights(self, weights: OrderedDict):
        if weights is not None:
            for name, param in self.named_parameters():
                if name in weights.keys() and not param.requires_grad:
                    weights.pop(name)
            self.load_state_dict(weights, strict=False)

    def freeze_pretrained_weights(self, weights: OrderedDict):
        if weights is not None:
            for k, v in self.named_parameters():
                if k in weights.keys():
                    v.requires_grad = False

    def forward_predictor(self, tokens: torch.Tensor, **kwargs) -> dict:
        # get prediction tokens
        pointing_token = 1 if self.add_pointing else 0
        tot_add_token_len = len(self.add_token_list) + pointing_token
        prediction_tokens = tokens[:, pointing_token:tot_add_token_len]
        output = {t: self._modules[t](prediction_tokens[:, i]) for i, t in enumerate(self.targets)}
        return output

    def forward(self, images, **kwargs) -> dict:
        pointing = kwargs.get("pointing", None)
        latent_tokens, mask, ids_restore = self.forward_encoder(images, pointing)
        predictions = self.forward_predictor(latent_tokens, **kwargs)
        return predictions


class GammaPhysNetMegatron(GammaPhysNetPrime):
    """
    Domain adversarial implementation of GammaPhysNetPrime.

    DANN version of the GammaPhysNetPrime. Still experimental, doesn't yet work
    """

    def __init__(self, net_parameters_dic: dict):
        super().__init__(net_parameters_dic)
        encoder_embed_dim = net_parameters_dic["backbone"]["parameters"]["embed_dim"]

        output_size = net_parameters_dic["targets"]["domain_class"]
        self.add_module("domain_class", nn.Linear(encoder_embed_dim, output_size))

    def forward_predictor(self, tokens: torch.Tensor, **kwargs) -> dict:
        # get prediction tokens
        pointing_token = 1 if self.add_pointing else 0
        tot_add_token_len = len(self.add_token_list) + pointing_token
        prediction_tokens = tokens[:, pointing_token:tot_add_token_len]
        K = kwargs.get("grad_weight", 1.0)  # In the case the weighting is applied on the gradients
        output = {}
        for i, t in enumerate(self.targets):
            if t == "domain_class":
                output[t] = self._modules[t](GradientLayer.apply(prediction_tokens[:, i], K, True))
            else:
                output[t] = self._modules[t](prediction_tokens[:, i])
        return output
