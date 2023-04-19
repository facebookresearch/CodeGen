import math
import typing as tp
from einops import rearrange, repeat
import torch
from torch import nn
from torch import Tensor


class CAPE1d(nn.Module):
    def __init__(
        self,
        d_model: int,
        max_global_shift: float = 0.0,
        max_local_shift: float = 0.0,
        max_global_scaling: float = 1.0,
        normalize: bool = False,
        freq_scale: float = 1.0,
        batch_first: bool = False,
    ):
        super().__init__()

        assert (
            max_global_shift >= 0
        ), f"""Max global shift is {max_global_shift},
        but should be >= 0."""
        assert (
            max_local_shift >= 0
        ), f"""Max local shift is {max_local_shift},
        but should be >= 0."""
        assert (
            max_global_scaling >= 1
        ), f"""Global scaling is {max_global_scaling},
        but should be >= 1."""

        self.max_global_shift = max_global_shift
        self.max_local_shift = max_local_shift
        self.max_global_scaling = max_global_scaling
        self.normalize = normalize
        self.freq_scale = freq_scale
        self.batch_first = batch_first

        freq = freq_scale * torch.exp(
            -2.0 * torch.floor(torch.arange(d_model) / 2) * (math.log(1e4) / d_model)
        )
        self.register_buffer("freq", freq)

        _sin2cos_phase_shift = torch.tensor(math.pi) / 2.0
        cos_shifts = _sin2cos_phase_shift * (torch.arange(d_model) % 2)
        self.register_buffer("cos_shifts", cos_shifts)

    def forward(
        self,
        x: Tensor,
        x_lengths: tp.Optional[Tensor] = None,
        positions_delta: tp.Optional[tp.Union[int, Tensor]] = None,
    ) -> Tensor:
        return x + self.compute_pos_emb(x, x_lengths, positions_delta)

    def compute_pos_emb(
        self,
        x: Tensor,
        x_lengths: tp.Optional[Tensor] = None,
        positions_delta: tp.Optional[tp.Union[int, Tensor]] = None,
    ) -> Tensor:
        if self.batch_first:
            batch_size, n_tokens, _ = x.shape  # b, t, c
        else:
            n_tokens, batch_size, _ = x.shape  # t, b, c

        positions = repeat(
            torch.arange(n_tokens), "t -> new_axis t", new_axis=batch_size
        ).to(x)

        if positions_delta is None:
            positions_delta = 1
        else:
            if (
                torch.is_tensor(positions_delta)
                and len(positions_delta.shape) == 1  # type:ignore
            ):
                positions_delta = rearrange(positions_delta, "b -> b 1")  # type: ignore
            positions *= positions_delta

        if x_lengths is not None:
            padding_mask = positions > x_lengths[:, None]
            positions[padding_mask] = float("nan")

        if self.normalize:
            positions -= torch.nanmean(positions, axis=1, keepdim=True)  # type: ignore

        positions = self.augment_positions(positions, positions_delta)

        positions = rearrange(positions, "b t -> b t 1")
        product = positions * self.freq.to(x)

        pos_emb = torch.sin(product + self.cos_shifts.to(x))

        if not self.batch_first:
            pos_emb = rearrange(pos_emb, "b t c -> t b c")

        pos_emb[pos_emb != pos_emb] = 0  # torch.nan_to_num(pos_emb, nan=0)

        return pos_emb

    @tp.no_type_check  # TODO reactivate
    def augment_positions(
        self,
        positions: Tensor,
        positions_delta: tp.Optional[tp.Union[int, Tensor]] = None,
    ):
        if self.training:
            batch_size, n_tokens = positions.shape

            if self.max_global_shift:
                delta = torch.FloatTensor(batch_size, 1).uniform_(
                    -self.max_global_shift, self.max_global_shift
                )
                delta = delta.to(positions.device)
            else:
                delta = 0

            if self.max_local_shift:
                epsilon = self.max_local_shift
                delta_local = torch.FloatTensor(batch_size, n_tokens)
                delta_local = delta_local.uniform_(-epsilon, epsilon)
                delta_local = delta_local.to(positions.device)
                if positions_delta is not None:
                    if (
                        torch.is_tensor(positions_delta)
                        and len(positions_delta.shape) == 1
                    ):
                        positions_delta = rearrange(positions_delta, "b -> b 1")
                    delta_local *= positions_delta
            else:
                delta_local = 0

            if self.max_global_scaling > 1.0:
                log_lambdas = torch.FloatTensor(batch_size, 1)
                log_lambdas = log_lambdas.uniform_(
                    -math.log(self.max_global_scaling),
                    math.log(self.max_global_scaling),
                )
                log_lambdas = log_lambdas.to(positions.device)
            else:
                log_lambdas = torch.zeros(1).to(positions.device)

            positions = (positions + delta + delta_local) * torch.exp(log_lambdas)

        return positions


# def cape_positions_1d(
#     positions_1d: np.ndarray,
#     mean_normalize: bool,
#     augment: bool,  # True during training
#     max_global_shift,  # delta max
#     max_local_shift,  # epsilon max
#     max_scale,  # lambda max
#     rng=np.random.RandomState(42),
# ):
#     """
#     Takes original positions, returns modified ones.
#     Can reuse sin/cos embedding from "Attention is all you need".
#     Code handles NaNs is positions_1d input as if those correspond to pad tokens
#     """
#     assert max_scale >= 1
#     batch_size, n_tokens = positions_1d.shape
#     if mean_normalize:
#         positions_1d -= np.nanmean(positions_1d, axis=1, keepdims=True)
#     if augment:
#         delta = rng.uniform(-max_global_shift, +max_global_shift, size=[batch_size, 1])
#         delta_local = rng.uniform(
#             -max_local_shift, +max_local_shift, size=[batch_size, n_tokens]
#         )
#         log_lambdas = rng.uniform(
#             -np.log(max_scale), +np.log(max_scale), size=[batch_size, 1]
#         )
#         new_positions = (positions_1d + delta + delta_local) * np.exp(log_lambdas)
#         return new_positions
#     else:
#         return positions_1d
