import re
import typing as tp
from pathlib import Path


def test_package_init_annotations() -> None:
    # automatically updates the __init__ functions with "-> None:" if missing
    # it fails the first time when adding it, then it should work
    # feel free to deactivate if that helps, it's not that important :p
    failed = []
    pattern = re.compile(r"(def __init__\(self.*\)):")
    for fp in Path(__file__).parents[1].rglob("*.py"):
        if "expected" in str(fp) or "test_" in fp.name:
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
