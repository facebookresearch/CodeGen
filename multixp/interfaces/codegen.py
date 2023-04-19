import inspect
import logging
import dataclasses
import typing as tp
from pathlib import Path
import torch
import multixp
from codegen_sources.dataloaders import transforms
from codegen_sources.dataloaders import utils
from codegen_sources.dataloaders.utils import Batch as Batch
from codegen_sources.dataloaders import typeinference
from codegen_sources.dataloaders import deobfuscator as deobf
import codegen_sources.model.src.model.transformer as transf_mod
import codegen_sources.model.src.model as build
import codegen_sources.model.src.optim as cgoptim
from codegen_sources.model.src.data.loader import check_data_params, load_data


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class TransformerConfig:
    fp16: bool = False
    # model parameters
    emb_dim: int = 1024
    n_layers: int = 6
    n_heads: int = 8
    dropout: float = 0.1
    attention_dropout: float = 0
    gelu_activation: bool = False
    share_inout_emb: bool = True
    sinusoidal_embeddings: bool = False
    layer_dropout: float = 0.0
    min_layers: int = 2
    spans_emb_encoder: bool = False
    efficient_attn: tp.Optional[str] = None  # "auto"
    # CAPE relative embeddings
    cape_embeddings: bool = False
    cape_global_shift: float = 5.0
    cape_local_shift: float = 0.5
    cape_global_scaling: float = 1.0
    discrete_cape_max: int = 0
    use_lang_emb: bool = True
    # reloading
    reload_model: str = ""
    reload_emb: str = ""
    # added later  # where is that from?
    _emb_dim_encoder: tp.Optional[int] = None
    _emb_dim_decoder: tp.Optional[int] = None
    _is_encoder: bool = True  # internal for choosing between encoder and decoder
    _n_words: int = -1
    _eos_index: int = -1
    _pad_index: int = -1
    _n_classes_classif: int = -1
    _n_langs: int = 0
    _langs: tp.List[str] = dataclasses.field(default_factory=list)
    _id2lang: tp.Dict[int, str] = dataclasses.field(default_factory=dict)
    _lang2id: tp.Dict[str, int] = dataclasses.field(default_factory=dict)
    _dico: tp.Any = None


@multixp.models.register("cg_transformer")
def build_transformer(cfg: TransformerConfig) -> torch.nn.Module:
    # pylint: disable=protected-access
    dico = cfg._dico
    if dico is None:
        raise RuntimeError("_dico field should have been filled in")
    cfg._n_words = len(dico)
    cfg._eos_index = dico.eos_index
    cfg._pad_index = dico.pad_index
    out = {}
    is_enc = cfg._is_encoder
    for field in dataclasses.fields(cfg):
        if field.name in (
            "_is_encoder",
            "_emb_dim_encoder",
            "reload_model",
            "reload_emb",
            "_dico",
        ):
            continue
        name = field.name.lstrip("_")
        val = getattr(cfg, field.name)
        out[name] = val
        if name in ["n_layers", "emb_dim"]:
            out[name + ("_encoder" if is_enc else "_decoder")] = val
    # fill interaction between encoder and decoder
    for name in ["encoder", "decoder"]:
        val = getattr(cfg, f"_emb_dim_{name}")
        out[f"emb_dim_{name}"] = cfg.emb_dim if val is None else val
    cg_config = transf_mod.TransformerConfig(**out)
    cg_config.id2lang = {0: "python"}
    cg_config.lang2id = {"python": 0}
    cg_config.n_langs = 1
    transformer = transf_mod.TransformerModel(
        cg_config, is_encoder=is_enc, dico=dico.word2id, with_output=True
    )
    # reload pretrained word embeddings
    cg_config.lgs_mapping = ""  # type: ignore # HACK
    if cfg.reload_emb != "":
        word2id, embeddings = build.load_embeddings(cfg.reload_emb, cg_config)
        build.set_pretrain_emb(transformer, dico, word2id, embeddings, gpu=False)
    if cfg.reload_model != "":
        logger.info("============ Model Reloading")
        build.reload_transformer(
            cg_config,
            cfg.reload_model,
            dico,
            transformer,
            "encoder" if is_enc else "decoder",
            gpu=False,
            model_number=0,
        )
    return transformer


@dataclasses.dataclass
class LoadingCfg:
    """Config for loading the iterators in parallel using
    pytorch dataloader and batch optimizer
    """

    train_overlap: bool = True  # this must be dealt with externally
    num_workers: tp.Optional[int] = 8
    batch_size: int = 32
    max_num_tokens: int = 8000  # ???
    max_sequence_length: int = 2000
    buffer_size: int = 1000
    seed: tp.Optional[int] = None

    def __post_init__(self) -> None:
        if self.max_sequence_length > 2048:
            raise ValueError("Sequence length is max 2048 in transformers.py")

    def wrap_iterator(
        self, iterator: tp.Iterable[utils.Batch],
    ) -> tp.Iterable[utils.Batch]:
        """Wraps an iterable with pytorch dataloader and batch optimizer
        so as to provide more efficient loading
        if `num_workers` is None, the Dataset is not wrapped in a DataLoader
        (= sequential loading, no parallelization)
        """
        if hasattr(iterator, "max_sequence_length"):  # "soft"-propagate max length
            # this helps prevening computation early and makes dataloader faster
            iterator.max_sequence_length = self.max_sequence_length  # type: ignore
        if self.num_workers is not None:
            opts: tp.Dict[str, tp.Any] = dict(
                batch_size=self.batch_size,
                num_workers=self.num_workers,
                collate_fn=utils.Batch.collate_fn,
                persistent_workers=True,
            )
            try:
                torch.multiprocessing.set_start_method("spawn")  # avoids memory issues
            except RuntimeError as e:
                logger.warning(f"Skipping start method: {e}")
            iterator = torch.utils.data.DataLoader(iterator, **opts)  # type: ignore
        if self.seed is None:
            raise RuntimeError("A seed must be provided before wrapping")
        # torch dataloader for parallelization
        return utils.BatchOptimizer(
            iterator,
            max_num_tokens=self.max_num_tokens,
            buffer_size=self.buffer_size,
            seed=self.seed,
            max_sequence_length=self.max_sequence_length,
        )


@multixp.dataloaders.register.builder("cg_type")
@dataclasses.dataclass
class TypeInferenceIteratorConfig(typeinference.TypeInferenceIteratorConfig):
    input_path: Path
    keep_comments: bool = False
    process_strings: bool = True
    skip_no_types: bool = True
    seed: int = 12
    unmask_probability: float = 0.0  # only for train
    #
    loading: LoadingCfg = dataclasses.field(default_factory=LoadingCfg)

    def build(self) -> tp.Mapping[str, tp.Iterable[tp.Any]]:  # type: ignore
        """Creates the test/valid/train dataloaders for type hint inference
        """
        self.input_path = Path(self.input_path)
        configs = {}
        for k, name in enumerate(["train", "valid", "test"]):
            sub = dataclasses.replace(
                self, input_path=self.input_path / name, no_overlap=True
            )
            sub.seed += k * 1000
            if sub.loading.seed is None:
                sub.loading.seed = sub.seed
            if name != "train":
                sub.unmask_probability = 0.0
                sub.loading.buffer_size //= 2  # no need to be as efficient
            configs[name] = sub
        configs["train"].no_overlap = not self.loading.train_overlap
        return {
            name: cfg.loading.wrap_iterator(typeinference.TypeInferenceIterator(cfg))
            for name, cfg in configs.items()
        }


@multixp.dataloaders.register.builder("deobf")
@dataclasses.dataclass
class DeobfCfg(deobf.DeobfIteratorConfig):
    input_path: Path
    #
    loading: LoadingCfg = dataclasses.field(default_factory=LoadingCfg)

    def build(self) -> tp.Mapping[str, tp.Iterable[tp.Any]]:  # type: ignore
        """Creates the test/valid/train dataloaders for type hint inference
        """
        configs = {}
        if self.loading.seed is None:
            self.loading.seed = self.seed
        for folder in self.input_path.iterdir():
            sub = dataclasses.replace(self, input_path=folder, no_overlap=False)
            # train dataset is the full dataset for simplicity's sake,
            # so we need to skip (rare) test/valid samples in it
            if folder.name not in ("train", "valid", "test"):
                raise RuntimeError(
                    f"Only train/valid/test subdirs are allowed, got {folder}"
                )
            assert folder.is_dir(), f"{folder} should be a dir"
            sub.skip_no_train = True
            if folder.name != "train":
                sub.loading.buffer_size //= 2  # no need to be as efficient
                # force overlap for exactly train only
                sub.no_overlap = True
                sub.skip_no_train = False
            configs[folder.name] = sub
        assert len(configs), f"No split found in {self.input_path}"
        return {
            name: cfg.loading.wrap_iterator(deobf.DeobfIteratorConfig.build(cfg))
            for name, cfg in configs.items()
        }


class SubIter(torch.utils.data.IterableDataset):
    def __init__(self, iterable: torch.utils.data.IterableDataset, count: int) -> None:
        self.iterable = iterable
        self.count = count

    def __iter__(self) -> tp.Iterator[tp.Any]:
        iterator = iter(self.iterable)
        for _ in range(self.count):
            try:
                yield next(iterator)
            except StopIteration:
                break


@dataclasses.dataclass
class OptimConfig:
    method: str = "AdamInverseSqrtWithWarmup"
    lr: float = 1e-3
    beta1: float = 0.9
    beta2: float = 0.999
    eps: float = 1e-8
    weight_decay: float = 0.01
    warmup_updates: int = 4000
    warmup_init_lr: float = 1e-7
    min_lr: float = 1e-9
    init_period: int = 1000000
    period_mult: float = 1
    lr_shrink: float = 0.75
    # lrsched
    step_patience: int = 3
    step_metric: str = "valid/acc"
    step_metric_mode: str = "max"


def build_optimizer(
    params: tp.Iterable[torch.Tensor], cfg: OptimConfig
) -> tp.Tuple[torch.optim.Optimizer, torch.optim.lr_scheduler._LRScheduler]:
    cls = getattr(cgoptim, cfg.method, None)
    if cls is None:
        cls = getattr(torch.optim, cfg.method)
    hparams: tp.Dict[str, tp.Any] = {
        f.name: getattr(cfg, f.name) for f in dataclasses.fields(cfg)
    }
    hparams["beta"] = (hparams.pop("beta1"), hparams.pop("beta2"))
    sig = list(inspect.signature(cls.__init__).parameters)
    assert sig[:2] == ["self", "params"]
    opt_params = {x: y for x, y in hparams.items() if x in sig[2:]}
    assert "lr" in opt_params
    info = f"Initializing {cls} with parameters {opt_params}"
    print(info, flush=True)
    logger.info(info)
    optim = cls(params, **opt_params)
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


############### DATALOADER #####################


@multixp.dataloaders.register.builder("standard_cg_type")
@dataclasses.dataclass
class CodegenLoaderCfg:
    data_path: str = "/checkpoint/jrapin/codegen/datasets/20220901_python_type_hints/XLM-syml"
    tokens_per_batch: int = 8000
    eval_tokens_per_batch: tp.Optional[int] = None
    lgs: str = "python_dictionary-python_hidden"
    lgs_id_mapping: str = ""
    # lgs_mapping: str = "python_dictionary:python,python_hidden:python"
    # @ steps @
    clm_steps: str = ""
    mlm_steps: str = ""
    mt_steps: str = ""
    mt_spans_steps: str = ""
    spans_emb_encoder: bool = False
    do_steps: str = "python_hidden-python_dictionary"
    classif_steps: str = ""
    ae_steps: str = ""
    tae_steps: str = ""
    bt_steps: str = ""
    st_steps: str = ""
    # @ eval @
    eval_computation_pivot: str = ""
    eval_only: bool = False
    train_only: bool = False
    n_sentences_eval: int = 1500
    eval_computation: str = ""
    eval_ir_similarity: str = ""
    validation_metrics: str = "test_python_obfuscated-python_dictionary-obf_proba_1.0_mt_subtoken_exact_match"
    obf_proba: float = 1.0
    stopping_criterion: str = ""
    # @ other %
    has_sentence_ids: str = ""
    bt_max_len: tp.Optional[int] = None
    max_len: int = 2000
    debug_train: bool = False
    max_vocab: int = 64000
    min_count: int = 0
    batch_size: int = 32
    max_batch_size: int = 128
    n_gpu_per_node: int = -1
    split_data: bool = False
    multi_gpu: bool = True
    split_data_accross_gpu: str = "local"
    local_rank: int = -1

    def build(self) -> tp.Mapping[str, tp.Iterable[tp.Any]]:
        print("Building standard dataloader!")
        assert self.do_steps == "python_hidden-python_dictionary"
        if self.n_gpu_per_node <= 0:
            mod = utils.Modulo.from_env()
            print(f"Loading {mod}")
            self.n_gpu_per_node = mod.mod
            self.local_rank = mod.index
        check_data_params(self)
        data = load_data(self)
        out = {
            n: CodegenBatcher(
                data["para"][("python_dictionary", "python_hidden")][n],
                tokens_per_batch=self.tokens_per_batch,
            )
            for n in ["train", "test", "valid"]
        }
        return out


class CodegenBatcher:
    def __init__(self, dataset: tp.Any, tokens_per_batch: int) -> None:
        self.dataset = dataset

    def __iter__(self) -> tp.Iterator[utils.Batch]:
        iterator = self.dataset.get_iterator(
            shuffle=True, group_by_size=True, n_sentences=-1, tokens_per_batch=8000,
        )
        for out in iterator:
            yield utils.Batch(
                x=out[1][0].T, x_len=out[1][1], y=out[0][0].T, y_len=out[0][1]
            )
