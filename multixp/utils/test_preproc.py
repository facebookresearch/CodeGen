import concurrent.futures
from pathlib import Path
from codegen_sources.dataloaders.tests import test_utils
from . import preproc


def test_splitter() -> None:
    splitter = preproc.Splitter()
    assert splitter("sosgoeso/pandas:") == "test"
    assert splitter("blublu/blackred:filepath") == "valid"
    # must be the same as with trailing whitespace
    assert splitter("blublu/pandas :root/other") == "test"
    assert splitter("xxx/blackred :here/and/there") == "valid"
    assert splitter("xxx/nevergrad :here/and/there") == "train"


def _do_nothing() -> None:
    pass


def test_wait_for_jobs() -> None:
    jobs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as exc:
        for _ in range(2):
            jobs.append(exc.submit(_do_nothing))
            preproc.wait_for_jobs(jobs, sleep=0.04)


def test_get_content_summary() -> None:
    fp = test_utils.DATA_FOLDER / "python.000.json.gz"
    out = preproc.get_file_summary(fp)
    assert len(out) == 50


def test_fileframe(tmp_path: Path) -> None:
    ff = preproc.FileFrame(tmp_path / "test.csv")
    ff.append(repo="stuff", err="OOM")
    ff.append(repo="otherstuff", err="other OOM")
    df = ff.read()
    assert tuple(df["repo"]) == ("stuff", "otherstuff")


def test_dump_dicts(tmp_path: Path) -> None:
    folder = tmp_path / "python"
    preproc.dump_dicts(folder, [{}, {"whatever": 12}])
    preproc.dump_dicts(folder, [{"whatever": 1}])
    names = [x.name for x in folder.iterdir()]
    assert names == ["python.000000000000.json.gz", "python.000000000001.json.gz"]
