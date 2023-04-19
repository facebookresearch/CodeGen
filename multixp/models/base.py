import typing as tp
import dataclasses
import numpy as np
import torch
from multixp.core import Register


register: Register[torch.nn.Module] = Register()


@dataclasses.dataclass
class BasicConfig:
    _in_shape: tp.Tuple[int, ...] = ()
    _out_shape: tp.Tuple[int, ...] = ()


@register("dense")
class BasicDense(torch.nn.Module):
    def __init__(self, cfg: BasicConfig) -> None:
        super().__init__()
        self.cfg = cfg
        neurons = [int(np.prod(cfg._in_shape)), 128, 256, int(np.prod(cfg._out_shape))]
        seq: tp.List[tp.Any] = []
        for k, (n_in, n_out) in enumerate(zip(neurons, neurons[1:])):
            if k:
                seq.append(torch.nn.ReLU())
            seq.append(torch.nn.Linear(n_in, n_out))
        self.sequence = torch.nn.Sequential(*seq)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.view(x.size()[0], -1)
        x = self.sequence(x)
        x = x.view(x.size()[0], *self.cfg._out_shape)
        return x
