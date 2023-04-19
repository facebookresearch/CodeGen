import copy
from pathlib import Path
import multixp
from . import repo as rp


def test_repo_github() -> None:
    repo = rp.Repo("facebookresearch/nevergrad")
    assert repo.clone_address == "git@github.com:facebookresearch/nevergrad.git"


def test_repo_address() -> None:
    repo = rp.Repo("http://gitlab.fr.com/org/name/")
    assert repo.name == "name"
    assert repo.clone_address == "https://gitlab.fr.com/org/name.git"


def _py_list(folder: Path):
    queue = [folder]
    while queue:
        folder = queue.pop()
        for fp in folder.iterdir():
            if fp.is_dir() and not fp.name.startswith((".", "__pycache__")):
                queue.append(fp)
            else:
                if fp.suffix == ".py":
                    yield fp


def test_repo_info() -> None:
    info = rp.RepoInfo(multixp.__file__)
    assert (info.folder / "multixp").exists()
    assert info.link == "https://github.com/fairinternal/genVarNames"
    # HACK to make it faster
    info.folder = info.folder / "multixp"
    assert info.folder.exists()
    out = info.extract_type_info()
    assert out["num_py"] == sum(1 for _ in _py_list(info.folder))
    assert 0 < out["num_noninit_py"] < out["num_py"]
    assert 0 < out["num_typed_py"] < out["num_py"]


def test_repo_stats() -> None:
    repo = rp.RepoStats(
        name="dvd/dvb",
        words={"real", "jar", "deal", "again", "altered", "bingbot", "swapped"},
        users={9152315112},
    )
    repo.add_time("1987-03-30T17:45:45Z")
    repo.events["something"] += 1
    repo.numbers["stargazers"] = 10
    other = copy.deepcopy(repo)
    other.events["something"] = 3
    other.numbers["stargazers"] = 12
    last = "2023-03-30T17:45:00"
    other.add_time(last)
    repo += other
    out = repo.export()
    assert out and isinstance(out, dict)
    assert out["events"]["something"] == 4
    assert out["numbers"]["stargazers"] == 12
    assert out["last_time"] == last
