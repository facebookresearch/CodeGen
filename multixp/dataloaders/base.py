import dataclasses
from pathlib import Path
import typing as tp
import torch
from torchvision import datasets
from torchvision import transforms
from multixp.core import Register


BatchInt = tp.Tuple[torch.Tensor, int]
register: Register[tp.Mapping[str, tp.Iterable[tp.Any]]] = Register()


class UnitTestDataset(torch.utils.data.IterableDataset[BatchInt]):

    in_shape = (2, 6, 6)
    out_shape = (4,)

    def __iter__(self) -> tp.Iterator[BatchInt]:
        for _ in range(12):
            im = torch.rand(*self.in_shape)
            yield im, 0

    def __len__(self) -> int:
        return 128


@dataclasses.dataclass
class DatasetConfig:
    name: str = "unittest"
    num_workers: int = 8
    batch_size: int = 32
    _in_shape: tp.Tuple[int, ...] = ()
    _out_shape: tp.Tuple[int, ...] = ()


@register("vision")
def build_vision_dataset(cfg: DatasetConfig) -> tp.Mapping[str, tp.Iterable[tp.Any]]:
    # pylint: disable=protected-access
    dsname = cfg.name
    opts: tp.Any = dict(batch_size=cfg.batch_size, num_workers=cfg.num_workers)
    if dsname == "CIFAR10":
        transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ]
        )
        datapath = Path("/datasets01/cifar-pytorch/11222017/")
        datapath = Path() / "datasets" if not datapath.exists() else datapath
        ds = {
            name: datasets.CIFAR10(datapath, train=name == "train", transform=transform)
            for name in ["train", "valid"]
        }
        cfg._in_shape = (32, 32)
        cfg._out_shape = (1000,)
    elif dsname == "unittest":
        ds = {name: UnitTestDataset() for name in ["train", "valid"]}
        cfg._in_shape = UnitTestDataset.in_shape
        cfg._out_shape = UnitTestDataset.out_shape
    else:
        raise ValueError(f"Unknown dataset {dsname}")
    return {name: torch.utils.data.DataLoader(d, **opts) for name, d in ds.items()}
