import re
import subprocess
from pathlib import Path


def get_root() -> Path:
    root = Path(__file__).parents[1]
    assert (root / "common").is_dir()
    return root


def test_package_init_annotations() -> None:
    # automatically updates the __init__ functions with "-> None:" if missing
    # it fails the first time when adding it, then it should work
    # feel free to deactivate if that helps, it's not that important :p
    failed = []
    pattern = re.compile(r"(def __init__\(self.*\)):")
    root = get_root()
    for fp in root.rglob("*.py"):
        if "test_" in fp.name:
            continue
        text = fp.read_text()
        text2 = pattern.sub(r"\g<1> -> None:", text)
        if text2 != text:
            failed.append(str(fp))
            fp.write_text(text2)
    if failed:
        string = "\n -".join(
            ["Missing -> None at the end of __init__ definition"] + failed
        )
        string += "\nUpdate, or run this test locally for automatic addition"
        raise AssertionError(string)


def test_property_syntax() -> None:
    # automatic linters tend to change @property to @ property for no reason
    root = get_root()
    errors = []
    for fp in root.rglob("*.py"):
        if fp == Path(__file__):
            continue
        if "@ property" in fp.read_text():
            errors.append(str(fp))
    if errors:
        msg = ["Additional space in @property, linter got crazy:"] + errors
        raise AssertionError("\n  - ".join(msg))


def test_black() -> None:
    out = subprocess.check_output(
        ["black", "multixp"], shell=False, stderr=subprocess.STDOUT, timeout=10
    ).decode("utf8")
    if "reformatted" in out:
        raise AssertionError(f"Running black made changes:\n{out}")
