import torch
import torch.nn as nn
from typing import Tuple, Optional

"""
The AdaLN implementations were taken from 
https://github.com/kwsong0113/diffusion-forcing-transformer/blob/main/algorithms/dfot/backbones/dit/dit_blocks.py

Adapted implementation to support LoRA as in Cosmos (Nvidia)
"""


def modulate(x: torch.Tensor, shift: torch.Tensor, scale: torch.Tensor):
    assert (
        x.shape == shift.shape == scale.shape
    ), f"Got x: {x.shape}, shift: {shift.shape}, scale: {scale.shape}"
    return x * (1 + scale) + shift


def apply_modulation(c, modulation_op, x_shape):
    assert len(x_shape) == 3, f"Expected x to have 3 dims, got {len(x_shape)}"
    if c.dim() == 3 and x_shape[1] != c.size(1):
        # For per-frame time step, where frames are fixed length sequences
        assert x_shape[1] % c.size(1) == 0, f"Got incompatible shapes: {x_shape}, {c.shape}"
        multiplier = x_shape[1] // c.size(1)
        c = modulation_op(c.unsqueeze(2)).expand(c.size(0), c.size(1), multiplier, -1).flatten(1, 2)

    elif c.dim() != len(x_shape):
        assert c.dim() == 2, f"Got c.dim={c.dim()} != 2"
        c = modulation_op(c.unsqueeze(1)).expand(c.size(0), x_shape[1], -1)
    else:
        assert c.shape == x_shape, f"Shape mismatch: {c.shape}!={x_shape}"
        c = modulation_op(c)

    return c


class AdaLayerNorm(nn.Module):
    """
    Adaptive layer norm (AdaLN).
    """

    def __init__(
        self,
        hidden_size: int,
        lora_hidden_dim: Optional[int] = None,
        eps: float = 1e-6,
        device=None,
        dtype=None,
    ):
        super().__init__()
        self.lora_hidden_dim = lora_hidden_dim
        if lora_hidden_dim is None:
            self.modulation = nn.Sequential(
                nn.SiLU(),
                nn.Linear(
                    hidden_size, 2 * hidden_size, bias=True, device=device, dtype=dtype
                ),
            )
        else:
            self.modulation = nn.Sequential(
                nn.SiLU(),
                nn.Linear(
                    hidden_size, lora_hidden_dim, bias=False, device=device, dtype=dtype
                ),
                nn.Linear(
                    lora_hidden_dim,
                    2 * hidden_size,
                    bias=True,
                    device=device,
                    dtype=dtype,
                ),
            )
        self.norm = nn.LayerNorm(
            hidden_size,
            elementwise_affine=False,
            eps=eps,
            device=device,
            dtype=torch.float32,  # crucial for maintaining numerical precision!
        )
        self.initialize_weights()

    def initialize_weights(self):
        # Zero-out:
        nn.init.zeros_(self.modulation[-1].weight)
        nn.init.zeros_(self.modulation[-1].bias)
        if self.lora_hidden_dim is not None:
            nn.init.zeros_(self.modulation[-2].weight)

    def forward(self, x: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the AdaLN layer.
        Args:
            x: Input tensor of shape (B, T, D).
            c: Conditioning tensor of shape (B, D) or (B, T, D).
        """
        c = apply_modulation(c, self.modulation, x.shape)
        shift, scale = c.chunk(2, dim=-1)
        return modulate(self.norm(x.float()).to(dtype=x.dtype), shift, scale)


class AdaLayerNormZero(nn.Module):
    """
    Adaptive layer norm zero (AdaLN-Zero).
    """

    def __init__(
        self,
        hidden_size: int,
        lora_hidden_dim: Optional[int] = None,
        eps: float = 1e-6,
        device=None,
        dtype=None,
    ):
        super().__init__()
        self.lora_hidden_dim = lora_hidden_dim
        if lora_hidden_dim is None:
            self.modulation = nn.Sequential(
                nn.SiLU(),
                nn.Linear(
                    hidden_size, 3 * hidden_size, bias=True, device=device, dtype=dtype
                ),
            )
        else:
            self.modulation = nn.Sequential(
                nn.SiLU(),
                nn.Linear(
                    hidden_size, lora_hidden_dim, bias=False, device=device, dtype=dtype
                ),
                nn.Linear(
                    lora_hidden_dim,
                    3 * hidden_size,
                    bias=True,
                    device=device,
                    dtype=dtype,
                ),
            )
        self.norm = nn.LayerNorm(
            hidden_size,
            elementwise_affine=False,
            eps=eps,
            device=device,
            dtype=torch.float32,  # crucial for maintaining numerical precision!
        )
        self.initialize_weights()

    def initialize_weights(self):
        # Zero-out:
        nn.init.zeros_(self.modulation[-1].weight)
        nn.init.zeros_(self.modulation[-1].bias)
        if self.lora_hidden_dim is not None:
            nn.init.zeros_(self.modulation[-2].weight)

    def forward(
        self, x: torch.Tensor, c: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass of the AdaLN-Zero layer.
        Args:
            x: Input tensor of shape (B, T, D).
            c: Conditioning tensor of shape (B, D) or (B, T', D). Either T=T'
             or T = T' * K
        """
        c = apply_modulation(c, self.modulation, x.shape)
        shift, scale, gate = c.chunk(3, dim=2)
        return modulate(self.norm(x.float()).to(dtype=x.dtype), shift, scale), gate
