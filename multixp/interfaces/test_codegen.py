from pathlib import Path
import torch
import pytest
import multixp

from . import codegen


def test_transformer() -> None:
    cfg = codegen.TransformerConfig()
    cfg._dico = codegen.DeobfCfg.transform().dico
    out = codegen.build_transformer(cfg)
    assert isinstance(out, torch.nn.Module)


def test_optim() -> None:
    cfg = codegen.TransformerConfig()
    cfg._dico = codegen.DeobfCfg.transform().dico
    model = codegen.build_transformer(cfg)
    out = codegen.build_optimizer(model.parameters(), codegen.OptimConfig())
    assert isinstance(out[0], torch.optim.Optimizer)


def test_transformer_reload() -> None:
    path = Path(
        "/checkpoint/broz/DOBF_saved_models/XLM_size/MLM-XLM-size/checkpoint.pth"
    )
    if not path.exists():
        pytest.skip("Model to reload unavailable")
    cfg = codegen.TransformerConfig(reload_model=str(path))
    cfg._dico = codegen.DeobfCfg.transform().dico
    out = codegen.build_transformer(cfg)
    assert isinstance(out, torch.nn.Module)


def test_iter(tmp_path: Path) -> None:
    code = Path(multixp.__file__).parent
    for name in ["train", "valid"]:
        (tmp_path / name).symlink_to(code)
    out = codegen.TypeInferenceIteratorConfig(
        input_path=tmp_path, loading=codegen.LoadingCfg(batch_size=32)
    ).build()
    out = next(iter(out["valid"]))
    assert hasattr(out, "x")


def test_codegen_iterator() -> None:
    cfg = codegen.CodegenLoaderCfg()
    if not Path(cfg.data_path).exists():
        pytest.skip("No data to experiment with")
    loaders = multixp.dataloaders.register.build(cfg)
    batch = next(iter(loaders["train"]))
    assert isinstance(batch.x, torch.Tensor)
