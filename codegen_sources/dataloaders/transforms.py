# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import re
import itertools
from pathlib import Path
import torch
import fastBPE
from transformers import RobertaTokenizer
import codegen_sources
import typing as tp
import codegen_sources.preprocessing.lang_processors as langp
import codegen_sources.preprocessing.lang_processors.utils as lputils
import codegen_sources.model.src.data.dictionary as dic
from codegen_sources.preprocessing.bpe_modes import FastBPEMode, RobertaBPEMode
import codegen_sources.preprocessing.obfuscation.utils_deobfuscation as deobf
from codegen_sources.model.src.utils import restore_roberta_segmentation_sentence
from . import utils

# pylint: disable=arguments-differ


# code -> updated code(=obfuscated, formatted etc)
# updated code -> tokenized
# tokenized -> bpe
#
# bpe -> tokenized -> code
import sentencepiece as spm  # type: ignore

PathLike = tp.Union[str, Path]
X = tp.TypeVar("X")
Y = tp.TypeVar("Y")
Z = tp.TypeVar("Z")
BPE_FOLDER = (
    Path(codegen_sources.__file__).resolve().parents[1]
    / "data"
    / "bpe"
    / "cpp-java-python"
)
# TokCode = tp.NewType('TokCode', str)  # can help making sure we don't mix tok and untok
TokCode = tp.List[str]
# TODO: when it's clearer what we want tokenize code to be, let's port it
#       to the languange processors (starting from the base one)


class Transform(tp.Generic[X, Y]):
    def apply(self, data: X) -> Y:
        """Apply the transform"""
        raise NotImplementedError

    def revert(self, data: Y) -> X:
        """Revert the transform"""
        raise NotImplementedError

    def pipe(self, other: "Transform[Y,Z]") -> "Composition[X,Z]":
        """Create a new transform composing this transform followed by another
        transform.

        Parameter
        ----------
        other: Transform
            another transform taking as input the output of the current
            transform
        """
        return Composition(self, other)

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        params = sorted(
            f"{x}={y!r}" for x, y in self.__dict__.items() if not x.startswith("_")
        )
        return f"{cls}({','.join(params)})"

    def inverted(self) -> "Transform[Y, X]":
        """Creates the transform which is the inverted version
        from this one
        """
        return Inverted(self)


class Inverted(Transform[X, Y]):
    """Transform thant inverts another transform,
    aka apply->revert and revert->apply
    """

    def __init__(self, transform: Transform[Y, X]) -> None:
        self.transform = transform

    def apply(self, data: X) -> Y:
        return self.transform.revert(data)

    def revert(self, data: Y) -> X:
        return self.transform.apply(data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.transform})"


class _InitialSpaces(Transform[str, str]):
    """Converts initial spaces into a token and a number"""

    def __init__(self, space_char: str = "<special8>") -> None:
        self.space_char = space_char
        self.pat = re.compile(f"{space_char} [0-9]+ (.)?")

    def apply(self, string: str) -> str:
        lines = string.splitlines()
        new_lines = []
        for line in lines:
            length = len(line)
            stripped = line.lstrip(" ")
            count = length - len(stripped)
            if count:
                stripped = f"{self.space_char} {count} {stripped}"
            new_lines.append(stripped)
        return "\n".join(new_lines)

    def revert(self, string: str) -> str:
        lines = string.splitlines()
        new_lines = []
        for line in lines:
            if self.pat.match(line) is not None:
                _, num, rest = line.split(" ", maxsplit=2)
                line = int(num) * " " + rest
            new_lines.append(line)
        return "\n".join(new_lines)


class Composition(Transform[X, Z]):
    """Composition of several transforms

    Paramters
    ---------
    transform_1: Transform
        the first transform to be applied
    transform_2: Transform
        the second transform to be applied
    """

    def __init__(
        self, transform_1: Transform[X, Y], transform_2: Transform[Y, Z]
    ) -> None:
        self.transforms: tp.List[Transform[tp.Any, tp.Any]] = []
        for t in (transform_1, transform_2):
            self.transforms.extend(
                t.transforms if isinstance(t, Composition) else [t]  # type: ignore
            )

    def apply(self, data: X) -> Z:
        out: tp.Any = data
        for t in self.transforms:
            out = t.apply(out)
        return out  # type: ignore

    def revert(self, data: Z) -> X:
        out: tp.Any = data
        for t in reversed(self.transforms):
            out = t.revert(out)
        return out  # type: ignore


# pylint: disable=arguments-renamed


class CodeTokenizer(Transform[str, TokCode]):
    """Tokenize code

    Parameters
    ----------
    language: str
        language to be tokenized, this will call the corresponding
        language processor
    keep_comments: bool
        whether to keep the comments in the tokenized code
    process_strings: bool
        TODO
    """

    def __init__(
        self, language: str, keep_comments: bool = False, process_strings: bool = True
    ) -> None:
        self.language = language
        self.keep_comments = keep_comments
        self.process_strings = process_strings
        self._tokenizer: tp.Any = None

    @property
    def tokenizer(self) -> langp.LangProcessor:
        if self._tokenizer is None:
            self._tokenizer = langp.LangProcessor.processors[self.language]()
        return self._tokenizer

    def apply(self, code: str) -> TokCode:
        return self.tokenizer.tokenize_code(
            code, keep_comments=self.keep_comments, process_strings=self.process_strings
        )

    def revert(self, tok_code: TokCode) -> str:
        return self.tokenizer.detokenize_code(tok_code)

    # the following is needed for picklability
    # (because fast_bpe is not picklable)
    def __getstate__(self) -> tp.Dict[str, tp.Any]:
        return utils.extract_dict(self, reset_keys=["_tokenizer"])


class BpeBase(Transform[TokCode, str]):
    """Applies a BPE model to a tokenized code

    Parameter
    ---------
    code_path: str / Path
        path to the codes file to use
    """

    def __init__(self) -> None:
        # delayed init because can be slow/heavy/non-picklable
        self._bpe_model: tp.Any = None

    def _init_model(self) -> tp.Any:
        raise NotImplementedError

    @property
    def bpe_model(self) -> tp.Any:
        if self._bpe_model is None:
            self._bpe_model = self._init_model()
        return self._bpe_model

    # the following is needed for picklability
    # (because fast_bpe is not picklable)
    def __getstate__(self) -> tp.Dict[str, tp.Any]:
        return utils.extract_dict(self, reset_keys=["_bpe_model"])


class FastBpe(BpeBase):
    def __init__(self, code_path: tp.Optional[PathLike] = None) -> None:
        super().__init__()
        if code_path is None:
            code_path = BPE_FOLDER / "codes"
        assert Path(code_path).is_file(), f"{code_path} is not a file"
        self.code_path = str(code_path)

    def _init_model(self) -> tp.Any:
        # pylint: disable=not-callable
        return fastBPE.fastBPE(self.code_path)  # type: ignore

    def apply(self, tok_code: TokCode) -> str:
        if not isinstance(tok_code, list):
            raise TypeError("Tokenized code must be provided as a list")
        tokens: tp.List[str] = self.bpe_model.apply(tok_code)
        out = FastBPEMode.repair_bpe_for_obfuscation_line(" ".join(tokens))
        return out

    def revert(self, subtokens: str) -> TokCode:
        return subtokens.replace("@@ ", "").split()


class StrSplit(Transform[str, TokCode]):
    """Splits a string on spaces"""

    def apply(self, code: str) -> TokCode:
        return code.split(" ")

    def revert(self, tok_code: TokCode) -> str:
        return " ".join(tok_code)


class SentencePieceTokenizer(Transform[str, str]):
    """Computes tokenization + BPE in one step"""

    def __init__(self, code_path: tp.Optional[PathLike] = None) -> None:
        # delayed init because can be slow/heavy/non-picklable
        if code_path is None:
            code_path = BPE_FOLDER.parent / "sentencepiece/sentencepiece_32k_v2/model"
        self._bpe_model: tp.Any = None
        self.code_path = Path(code_path)
        assert self.code_path.is_file(), f"{self.code_path} doesn't exist"

    def _init_model(self) -> tp.Any:
        return spm.SentencePieceProcessor(model_file=str(self.code_path))

    @property
    def bpe_model(self) -> tp.Any:
        if self._bpe_model is None:
            self._bpe_model = self._init_model()
        return self._bpe_model

    @staticmethod
    def repl(match: tp.Match[str]) -> str:
        string = match.group(0)
        out = string.replace(" ", "")
        if match.group("next") is not None:
            out = out[:-1] + " " + match.group("next")
        if match.group("prev") is not None:
            out = match.group("prev") + " " + out[1:]
        out = out.replace("><", "> <")
        return out

    def apply(self, data: str) -> str:
        out = " ".join(self.bpe_model.encode_as_pieces(data))
        final = r"(?P<next>\S)?"
        start = r"(?P<prev>\S)?"
        for prefix in deobf.OBFUSCATED_PREFIXES:
            pattern = start + f'{"( )?".join(prefix)}(( )?[0-9]+)+' + final
            out = re.sub(pattern, self.repl, out)
        pattern = start + "(< special [0-9]+ >)+" + final
        out = re.sub(pattern, self.repl, out)
        return out

    def revert(self, subtokens: str) -> str:
        return self.bpe_model.decode_pieces(subtokens.split(" "))


class RobertaBpe(BpeBase):
    def __init__(
        self, new_line: str = "<special9>", space_char: str = "<special8>"
    ) -> None:
        super().__init__()
        self.new_line = f" {new_line} "
        self.spaces = _InitialSpaces(space_char=space_char)

    def _init_model(self) -> tp.Any:
        return RobertaTokenizer.from_pretrained("roberta-base")

    def apply(self, tok_code: TokCode) -> str:
        # TODO splitting on lines? so we should not use TokCode?
        lines = self.spaces.apply(" ".join(tok_code)).split("\n")
        lines = [self.bpe_model._tokenize(line.strip()) for line in lines]
        repair = RobertaBPEMode.repair_bpe_for_obfuscation_line
        lines = [repair(" ".join(line)) for line in lines]
        out = self.new_line.join(lines)
        return out

    def revert(self, subtokens: str) -> TokCode:
        out: str = restore_roberta_segmentation_sentence(subtokens)  # type: ignore
        out = out.replace(self.new_line.strip(), "\n")
        return self.spaces.revert(out).split()


class BpeTensorizer(Transform[str, torch.Tensor]):
    """Converts from BPE to tensor

    Parameter
    ---------
    vocab_path: str / Path
        path to the vocab file to use
    no_unk: bool
        disallow unknown tokens
    """

    def __init__(
        self, vocab_path: tp.Optional[PathLike] = None, no_unk: bool = False
    ) -> None:
        # check model preprocess.py
        if vocab_path is None:
            vocab_path = BPE_FOLDER / "vocab"
        self.vocab_path = Path(vocab_path)  # for representation
        self.no_unk = no_unk
        self.dico = dic.Dictionary.read_vocab(vocab_path)

    def apply(self, subtokens: str) -> torch.Tensor:
        tag = [dic.EOS_WORD]  # </s>
        sublist = tag + subtokens.split(" ") + tag
        word2id = self.dico.word2id
        unk = self.dico.unk_index
        if self.no_unk:
            data = [word2id[tok] for tok in sublist]
        else:
            data = [word2id.get(tok, unk) for tok in sublist]
        return torch.LongTensor(data)
        # simpler solution is slightly slower:
        # return torch.LongTensor(
        #     [self.dico.index(tok, no_unk=self.no_unk) for tok in sublist]
        # )

    def revert(self, tensor: torch.Tensor) -> str:
        tensor = tensor.squeeze()
        if not tensor.ndim == 1:
            raise ValueError(
                f"Only 1-dimensional tensors can be processed (got {tensor.shape})."
            )
        # wid = [self.dico[val.item()] for val in tensor]
        # return wid[: wid.index(dic.EOS_WORD)] if dic.EOS_WORD in wid else wid
        # skip initial eos if present
        start = 1 if tensor[0].item() == self.dico.eos_index else 0
        iterator: tp.Iterator[str] = (self.dico[val.item()] for val in tensor[start:])
        # with takewhile, we'll only fetch in the dict until we reach EOS
        iterator = itertools.takewhile(lambda x: x != dic.EOS_WORD, iterator)
        return " ".join(iterator)


class Tensorizer(Composition[TokCode, torch.Tensor]):
    """Converts from a tokenized string to a tensor, through BPE

    Parameter
    ---------
    bpe_folder: str / Path
        folder containing a codes file for bpe and a vocab file for
        tensorization.
    no_unk: bool
        disallow unknown tokens
    """

    def __init__(
        self, bpe_folder: tp.Optional[PathLike] = None, no_unk: bool = False
    ) -> None:
        if bpe_folder is None:
            bpe_folder = BPE_FOLDER
        bpe_folder = Path(bpe_folder)
        super().__init__(
            FastBpe(bpe_folder / "codes"),
            BpeTensorizer(bpe_folder / "vocab", no_unk=no_unk),
        )

    @property
    def dico(self) -> dic.Dictionary:
        return self.transforms[1].dico  # type: ignore


class SentencePieceTensorizer(Composition[str, torch.Tensor]):
    """Converts from a tokenized string to a tensor, with sentencepiece

    Parameter
    ---------
    folder: str / Path
        folder containing a codes file for model and a vocab file for
        tensorization.
    no_unk: bool
        disallow unknown tokens
    """

    def __init__(
        self, folder: tp.Optional[PathLike] = None, no_unk: bool = False
    ) -> None:
        tokenizer = SentencePieceTokenizer(
            Path(folder) / "model" if folder is not None else None
        )
        super().__init__(
            tokenizer,
            BpeTensorizer(tokenizer.code_path.with_name("vocab"), no_unk=no_unk),
        )

    @property
    def dico(self) -> dic.Dictionary:
        return self.transforms[1].dico  # type: ignore


class Dictifier(Transform[TokCode, tp.Dict[str, str]]):
    """Converts a list of tokens to the dict mapping mask_token -> result

    Parameters
    ----------
    separator: str
        separator used for encoding the dict as a string
    robust: bool
        if True, returns all entry that do parse instead of raising

    Note
    ----
    The order is different from the legacy one, to avoid VAR_10 following
    VAR_1
    """

    def __init__(self, separator: str = deobf.SEPARATOR, robust: bool = False) -> None:
        super().__init__()
        self.robust = robust
        self.separator = separator
        self._tok_order = {
            n: k for k, n in enumerate(lputils.obfuscation_tokens(raise_finished=False))
        }

    def apply(self, code_tokens: TokCode) -> tp.Dict[str, str]:
        if not isinstance(code_tokens, list):
            raise TypeError("Only lists are accepted")
        out = {}
        for entry in " ".join(code_tokens).split(self.separator):
            entry = entry.strip()
            if not entry:
                continue
            try:
                name, val = entry.split(" ", maxsplit=1)
            except ValueError as e:
                if not self.robust:
                    raise ValueError(f"Cannot split dict entry {entry!r}") from e
            else:
                out[name] = val
        return out

    def revert(self, dico: tp.Dict[str, str]) -> TokCode:
        keys = list(dico)
        keys.sort(key=lambda k: self._tok_order.get(k, -1))
        return self.separator.join(f"{k} {dico[k]}" for k in keys).split(" ")
