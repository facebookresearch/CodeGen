import typing as tp

from codegen_sources.model.src.data.dictionary import (
    OBF,
    OBFS,
)


def obfuscation_tokens(raise_finished: bool = True) -> tp.Iterator[str]:
    """Iterates on all obfuscation tokens"""
    for name in ["VAR", "FUNC", "CLASS"]:
        for k in range(OBFS[name]):
            yield OBF[name] % k
    if raise_finished:
        raise RuntimeError("Running out of obfuscation tokens")
