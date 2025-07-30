# Based on https://github.com/fkodom/yet-another-retnet/blob/main/yet_another_retnet/retention.py
# Copyright (c) 2022 Frank Odom
# Copyright (c) 2025 Lior Cohen
from dataclasses import dataclass
from functools import lru_cache
from math import ceil, log
from typing import Union, Callable, Optional, List, Sequence, Tuple, Literal

import numpy as np
from loguru import logger

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch._dynamo
from einops import rearrange, einsum, repeat
from torch import Tensor

from flash_pop.fused_retention import fused_chunk_retention
from flash_pop.xpos_emb import XPos
from flash_pop.retnet import ActivationString, _get_activation_fn, MultiScaleRetention
from flash_pop.modules.adaln import AdaLayerNorm, AdaLayerNormZero
from flash_pop.modules.timestep import TimestepEmbedder
from flash_pop.recurrent_state import RecurrentState


class DiffusionRetNetDecoderLayer(nn.Module):

    # NOTE: Mostly pulled from 'nn.TransformerDecoderLayer', but with changes:
    #   - use MultiScaleRetention instead of MultiheadAttention
    #   - no cross-attention layer, since retention doesn't play well with that

    @dataclass(kw_only=True)
    class Config:
        num_heads: int
        head_dim_v: int
        head_dim_qk: int = None
        dim_feedforward: int = 2048
        dropout: float = 0.1
        use_post_retention_dropout: bool = True
        head_decays_range: tuple[float, float] = None
        activation: Union[ActivationString, Callable[[Tensor], Tensor]] = "swish"
        layer_norm_eps: float = 1e-6
        ada_ln_lora_dim: Optional[int] = None
        device: Optional[Union[torch.device, str]] = torch.device('cuda')
        dtype: Optional[torch.dtype] = torch.bfloat16
        use_fused_version: bool = True
        chunk_size: int = 512  # only valid when `use_fused_version` is False.

    def __init__(
        self,
        config: Config,
        xpos_embedder: Optional[XPos] = None
    ) -> None:
        """

        :param num_heads: number of attention heads
        :param head_dim_v: the dimension of each attention head. This defines d_model, i.e., embedding dimension,
        through d_model = num_heads * head_dim_v.
        :param head_dim_qk: the query and key dimension of each attention head. If none, `head_dim_v` is used.
        Lower values (around 0.5-0.75*head_dim_v) were shown to be effective while reducing computational cost.
        :param dim_feedforward: the dimension of feedforward layer (hidden)
        :param dropout:
        :param activation:
        :param norm_first:
        :param layer_norm_eps:
        :param device:
        :param dtype:
        """
        self.config = config
        activation = config.activation
        if isinstance(config.activation, str):
            activation = _get_activation_fn(config.activation)

        super().__init__()
        self.dropout = nn.Dropout(config.dropout)
        self.use_post_retention_dropout = config.use_post_retention_dropout
        self.activation = activation
        d_model = config.num_heads * config.head_dim_v
        # retention block
        self.ada_ln1 = AdaLayerNormZero(
            d_model,
            eps=config.layer_norm_eps,
            lora_hidden_dim=config.ada_ln_lora_dim,
            device=config.device,
            dtype=config.dtype,
        )
        self.retention = self._build_multi_scale_retention(xpos_embedder=xpos_embedder)
        # feedforward block
        self.ada_ln2 = AdaLayerNormZero(
            d_model,
            eps=config.layer_norm_eps,
            lora_hidden_dim=config.ada_ln_lora_dim,
            device=config.device,
            dtype=config.dtype,
        )
        self.linear1 = nn.Linear(d_model, config.dim_feedforward, device=config.device, dtype=config.dtype)
        self.linear2 = nn.Linear(config.dim_feedforward, d_model, device=config.device, dtype=config.dtype)

        self._reset_parameters()

    def _build_multi_scale_retention(self, xpos_embedder: Optional[XPos] = None):
        return MultiScaleRetention(
            MultiScaleRetention.Config(
                num_heads=self.config.num_heads,
                head_dim_v=self.config.head_dim_v,
                head_dim_qk=self.config.head_dim_qk,
                dropout=self.config.dropout,
                head_decays_range=self.config.head_decays_range,
                activation=self.activation,
                device=self.config.device,
                dtype=self.config.dtype,
                use_fused_version=self.config.use_fused_version,
                chunk_size=self.config.chunk_size,
            ),
            xpos_embedder=xpos_embedder,
        )

    def _reset_parameters(self):
        # TODO: Check that we're following the same initialization as the paper
        nn.init.xavier_normal_(self.linear1.weight)
        nn.init.constant_(self.linear1.bias, 0)
        nn.init.xavier_normal_(self.linear2.weight)
        nn.init.constant_(self.linear2.bias, 0)

    def _feedforward_block(self, x: Tensor) -> Tensor:
        x = self.activation(self.linear1(x))
        x = self.dropout(x)
        x = self.linear2(x)
        x = self.dropout(x)
        return x

    def forward_chunkwise(
            self, x: Tensor, c: Tensor, start_idx: int, prev_state: Optional[Tensor] = None
    ) -> Tuple[Tensor, Tensor]:
        # retention block
        x, gate = self.ada_ln1(x, c)
        y, state = self.retention.forward_chunkwise(x, start_idx=start_idx, prev_state=prev_state)
        y = y * gate
        if self.use_post_retention_dropout:
            y = self.dropout(y)
        x = x + y
        x, gate = self.ada_ln2(x, c)
        x = x + self._feedforward_block(x) * gate

        return x, state

    def forward_recurrent(
            self, x: Tensor, c: Tensor, seq_idx: int, prev_state: Optional[Tensor] = None
    ) -> Tuple[Tensor, Tensor]:
        # retention block
        x, gate = self.ada_ln1(x, c)
        y, state = self.retention.forward_recurrent(
            x, seq_idx=seq_idx, prev_state=prev_state
        )
        y = y * gate
        if self.config.use_post_retention_dropout:
            y = self.dropout(y)
        x = x + y
        x, gate = self.ada_ln2(x, c)
        x = x + self._feedforward_block(x) * gate

        return x, state

    def forward(self, x: Tensor, c: Tensor, start_idx: int = 0, prev_state: Optional[Tensor] = None) -> Tuple[Tensor, Tensor]:
        return self.forward_chunkwise(x, c, start_idx=start_idx, prev_state=prev_state)
    

class DiffusionRetNetFinalLayer(nn.Module):
    @dataclass(kw_only=True)
    class Config:
        layer_config: DiffusionRetNetDecoderLayer.Config
        out_dim: int

    def __init__(self, config: Config):
        super().__init__()
        layer_config = config.layer_config
        d_model = layer_config.head_dim_v * layer_config.num_heads
        device = layer_config.device
        dtype = layer_config.dtype

        self.final_ada_ln = AdaLayerNorm(
            d_model,
            eps=layer_config.layer_norm_eps,
            lora_hidden_dim=layer_config.ada_ln_lora_dim,
            device=device,
            dtype=dtype,
        )
        self.final_linear = nn.Linear(d_model, config.out_dim, device=device, dtype=dtype)

    def forward(self, x: Tensor, c: Tensor):
        x = self.final_ada_ln(x, c)
        x = self.final_linear(x)

        return x


class DiffusionRetNetDecoder(nn.Module):
    """
    Class for Diffusion RetNet (similar to DiT).
    This extends the base RetNet with AdaLN / AdaLN-Zero layers
    for conditioning (on diffusion time steps and other signals).

    Note: This class excludes the final layer, which contains 
    only AdaLN + Linear components, to allow the user to
    use separate final layers for different subsets of outputs.
    This is useful e.g., when combining multiple modalities.

    Also, we implement a generic interface for conditioning, as one may
    choose arbitrary conditioning signals in addition to the diffusion times.
    Hence, we provide the TimestepEmbedder module as an external asset to be 
    used in a wrapper model together with the final layer.
    """

    @dataclass(kw_only=True)
    class Config:
        layer_config: DiffusionRetNetDecoderLayer.Config
        num_layers: int

    def __init__(self, config: Config):
        super().__init__()
        layer_config = config.layer_config
        if layer_config.head_dim_qk is None:
            layer_config.head_dim_qk = layer_config.head_dim_v
        self.layer_config = config.layer_config
        device = layer_config.device
        dtype = layer_config.dtype
        self.num_layers = config.num_layers
        self.xpos_embedder = XPos(layer_config.head_dim_qk, device=device, dtype=dtype)
        
        self.layers = nn.ModuleList(self._build_layers(config.num_layers))

    def _build_layers(self, num_layers: int):
        return [DiffusionRetNetDecoderLayer(self.layer_config, self.xpos_embedder) for _ in range(num_layers)]

    def forward_recurrent(
            self, x: Tensor, recurrent_state: RecurrentState = None
    ) -> Tuple[Tensor, RecurrentState]:
        self._validate_and_init_state(recurrent_state)

        states: List[Tensor] = []
        for layer, state_i in zip(self.layers, recurrent_state.state):
            assert isinstance(layer, DiffusionRetNetDecoderLayer)
            x, state = layer.forward_recurrent(x, recurrent_state.index, state_i)
            states.append(state)

        return x, RecurrentState(torch.stack(states), recurrent_state.index + 1)

    def forward_chunkwise(
            self, x: Tensor, c: Tensor, recurrent_state: RecurrentState = None
    ) -> Tuple[Tensor, RecurrentState]:
        """
        x: Input sequence of shape (B, T, D) = (batch, temportal dim, features dim)
        c: Conditioning signal. Can take various shapes:
        (B, T, D)
        (B, T', D): where T % T' == 0. In this case we assume the sequence is composed of 
        fixed length subsequences, and each temporal conditioning element
        is shared by all elements of its corresponding subsequence.
        (B, D): all time steps share the same conditioning signal.
        """
        self._validate_and_init_state(recurrent_state)

        states: List[Tensor] = []
        for layer, state_i in zip(self.layers, recurrent_state.state):
            assert isinstance(layer, DiffusionRetNetDecoderLayer)
            x, state = layer.forward_chunkwise(x, c, recurrent_state.index, state_i)
            states.append(state)

        return x, RecurrentState(torch.stack(states), recurrent_state.index + x.size(1))

    def forward(self, x: Tensor, c: Tensor, recurrent_state: RecurrentState = None) -> Tuple[Tensor, RecurrentState]:
        return self.forward_chunkwise(x=x, c=c, recurrent_state=recurrent_state)
    
    def _validate_and_init_state(self, recurrent_state: RecurrentState):
        if recurrent_state is None:
            recurrent_state = RecurrentState()
        if recurrent_state.state is None:
            recurrent_state.state = [None] * self.num_layers
            recurrent_state.index = 0
        elif len(recurrent_state.state) != len(self.layers):
            raise ValueError(
                f"Expected {len(self.layers)} previous states, got {len(recurrent_state.state)}"
            )
        assert recurrent_state.state is not None and recurrent_state.index is not None

        return recurrent_state
