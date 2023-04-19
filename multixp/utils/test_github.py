import os
from pathlib import Path
import pytest
from . import github as gh


def test_safe_size() -> None:
    path = Path(__file__)
    assert gh._safe_size(path) > 0


def test_bad_files() -> None:
    folder = Path(__file__).parent
    out = gh.irrelevant_files(folder)
    assert not any(x.suffix == ".py" for x in out)


def test_tmp_untar(tmp_path: Path) -> None:
    tarpath = tmp_path / "something.tar.gz"
    with pytest.raises(RuntimeError):
        with gh.temp_untar(tarpath):
            pass
    with gh.temp_untar(tarpath, allow_missing=True, replace=True) as tarfolder:
        assert not list(tarfolder.iterdir())
        folder = tarfolder / "blublu"
        folder.mkdir()
        (folder / "text").write_text("Hello!")
    with gh.temp_untar(tarpath) as tarfolder:
        assert [x.name for x in tarfolder.iterdir()] == ["blublu"]
        assert (tarfolder / "blublu" / "text").read_text() == "Hello!"
        (tarfolder / "blublu2").touch()
    # now add a binary file
    with gh.temp_untar(tarpath, replace=True) as tarfolder:
        assert [x.name for x in tarfolder.iterdir()] == ["blublu"]
        with (tarfolder / "binary\r").open("wb") as fout:
            fout.write(os.urandom(1050 ** 2))  # > 1MB
        assert sorted([x.name for x in tarfolder.iterdir()]) == ["binary\r", "blublu"]
    with gh.temp_untar(tarpath) as tarfolder:
        assert len(list(tarfolder.iterdir())) == 2
    gh.filter_tar(tarpath)
    with gh.temp_untar(tarpath) as tarfolder:
        assert sorted([x.name for x in tarfolder.iterdir()]) == ["blublu"]


def test_naming_convention() -> None:
    repo = "fb/nevergrad"
    naming = gh.Naming(repo)
    assert naming.repo == repo
    assert naming.success == "fb,nevergrad.tar.gz"
    assert naming.failure == "fb,nevergrad.txt"
    for fname in (naming.success, naming.failure):
        fp = Path(__file__).parent / fname
        naming2 = gh.Naming.from_file(fp)
        assert naming2.repo == repo
