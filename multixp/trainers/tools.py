import dataclasses
import typing as tp
import torch
from multixp import distrib


@dataclasses.dataclass
class OptimConfig:
    name: str = "Adam"
    lr: float = 0.0001
    step_patience: int = 3
    step_metric: str = "valid/acc"
    step_metric_mode: str = "max"
    params: tp.Any = dataclasses.field(default_factory=dict)


def build_optimizer(
    params: tp.Iterable[torch.Tensor], cfg: OptimConfig
) -> tp.Tuple[torch.optim.Optimizer, torch.optim.lr_scheduler._LRScheduler]:
    optim = getattr(torch.optim, cfg.name)(params, lr=cfg.lr, **cfg.params)
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optim,
        mode="max",
        factor=0.3,
        patience=cfg.step_patience,
        threshold=1e-3,
        threshold_mode="rel",
        cooldown=1,
    )  # guess what, ReduceLROnPlateau is not a lr scheduler...
    return optim, sched  # type: ignore


def distributed_loaders_safety_check(
    loaders: tp.Mapping[str, tp.Iterable[tp.Any]],
    item_getter: tp.Callable[[tp.Any], torch.Tensor],
) -> None:
    task = distrib.TaskEnv.from_env(dataloader=False)
    # dataset safety check
    if task.world_size > 1:
        print("Checking distributed dataloader.")
        vals = {}
        for name, loader in loaders.items():
            iterator = iter(loader)
            batch = next(iterator)
            del iterator  # may free some shared memory
            vals[name] = float(item_getter(batch).float().mean())
            print("Computed", name, vals[name])
        with distrib.SumDict().summed_over(1) as metrics:
            metrics.update(vals)
        metrics.reduce()
        reduced = metrics.export()
        if task.is_main:
            if all(abs(y - reduced[x]) < 1e-6 for x, y in vals.items()):
                raise RuntimeError(
                    f"Distributed samplers seem to send same data to everyone: {vals} Vs {reduced}"
                )
        print("Distributed dataloader has been checked.")
