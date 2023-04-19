import time
import zlib
import gzip
import json
import hashlib
import typing as tp
from pathlib import Path
import pandas as pd
from codegen_sources.dataloaders import utils


class Splitter:
    """Utility for splitting reproducibly between train, test and valid
    Usage:
    splitter = Splitter(percent_test=1, percent_valid=1)
    split = splitter("org/repo:filename")
    """

    def __init__(self, percent_test: int = 1, percent_valid: int = 1) -> None:
        assert isinstance(percent_test, int)
        assert isinstance(percent_valid, int)
        assert percent_test + percent_valid < 100
        self.percent_test = percent_test
        self.percent_valid = percent_valid

    def __call__(self, id_: str) -> str:
        parts = id_.split(":", maxsplit=1)
        if len(parts) != 2:
            err = f"id must be provided as org/repo:filepath (got {id_})"
            raise ValueError(err)
        parts = parts[0].split("/")
        if len(parts) != 2:
            err = f"id must be provided as org/repo:filepath (got {id_})"
            raise ValueError(err)
        repo = parts[1].strip()
        # historical pipeline keeps an extra space at the end
        hash_repo = zlib.adler32(f"{repo} ".encode("utf-8")) % 100
        if hash_repo < self.percent_test:
            return "test"
        if hash_repo < self.percent_test + self.percent_valid:
            return "valid"
        return "train"


def wait_for_jobs(jobs: tp.Iterable[tp.Any], sleep: float = 10.0) -> None:
    """Very crude function for regularly printing the percent
    of finished jobs in a list
    """
    jobs = list(jobs)
    done = 0
    print(f"Submitted {len(jobs)} jobs")
    while done < 100:
        new_done = int(100 * sum(j.done() for j in jobs) / len(jobs))
        if new_done > done:
            print(f"{new_done}% done")
            jdone = [j for j in jobs if j.done()]
            # pylint: disable=expression-not-assigned
            [j.result() for j in jdone]  # raise asap
            done = new_done
        else:
            time.sleep(sleep)
    print("Waiting is over")


def get_file_summary(filepath: tp.Union[str, Path]) -> tp.List[tp.Dict[str, tp.Any]]:
    """Returns a list of dict containing code id and content hash
    """
    filepath = Path(filepath)
    data = []
    if not filepath.name.endswith(".json.gz"):
        raise ValueError("Only .json.gz files are currently supported")
    with gzip.open(filepath, "rb") as f:
        for line in f:  # readlines() would load all data -> bad idea
            reader = utils.DelayedReader.from_json_string(line)
            try:
                code = reader.code
            except Exception as e:
                continue
            typed = any(x in code for x in ["->", "from typing ", "import typing"])
            content_hash = hashlib.sha256(reader.code.encode("utf-8")).hexdigest()
            data.append({"id": reader.id, "hash": content_hash, "typed": typed})
    return data


class FileFrame:
    """Writes data to a csv on the fly
    This is useful to keep track of errors for instance
    """

    def __init__(self, filepath: tp.Union[str, Path]) -> None:
        self._filepath = Path(filepath).absolute()
        if self._filepath.suffix != ".csv":
            raise ValueError("Only csv files are supported, got {filepath}")

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self._filepath)

    def append(self, **kwargs: str) -> None:
        if not self._filepath.exists():
            df = pd.DataFrame([kwargs])
        else:
            df = self.read()
            df = pd.concat([df, pd.DataFrame([kwargs])], ignore_index=True)
        df.to_csv(self._filepath, index=False)


def dump_dicts(folder: Path, data: tp.List[tp.Dict[str, tp.Any]]) -> None:
    """Dump a list of dicts into a json.gz file
    filename is built using folder name and a new number each time
    """
    folder.mkdir(exist_ok=True, parents=True)
    num = len(list(folder.iterdir()))
    filepath = folder / f"{folder.name}.{num:012d}.json.gz"
    with gzip.open(filepath, "w") as g:
        for k, d in enumerate(data):
            g.write((b"\n" if k else b"") + json.dumps(d).encode("utf8"))


# checking may permissive licenses
# there are more though (all The Stack are permissive, and do not include copyleft):
# PERMISSIVE = (
#     "apache-1.1",
#     "apache-2.0",
#     "ecl-2.0",  # apache like
#     "bsd-simplified",
#     "clear-bsd",
#     "0bsd",
#     "bsd-source-code",
#     "bsd-1-clause",
#     "bsd-2-clause",
#     "bsd-2-clause-freebsd",
#     "bsd-3-clause",
#     "bsd-3-clause-lbnl",
#     "bsd-3-clause-sun",
#     "bsd-3-clause-clear",
#     "bsd-3-clause-open-mpi",
#     "bsd-3-clause-no-nuclear-warranty",
#     "bsd-3-clause-no-nuclear-license-2014",
#     "bsd-4-clause",
#     "bsd-4-clause-uc",
#     "boost-1.0",
#     "bsl-1.0",
#     "mit",
#     "mit-0",
#     "mpl-2.0-no-copyleft-exception",
#     "cc0-1.0",
#     "isc",
#     "wtfpl",
#     "rsa-md",
#     "zlib",
#     # python licenses
#     "python-2.0",
#     "psf-2.0",
#     "cnri-python",
# )
