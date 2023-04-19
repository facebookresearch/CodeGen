import re
import json
import time
import shutil
import logging
import tarfile
import getpass
import tempfile
import subprocess
import contextlib
import typing as tp
from pathlib import Path
import concurrent.futures


JobDict = tp.Dict[str, concurrent.futures.Future]
PathLike = tp.Union[str, Path]
logger = logging.getLogger(__name__)


class Naming:
    """Naming convention for repo tar.gz or failed downloads"""

    def __init__(self, repo: str) -> None:
        self.repo = repo
        if not repo.count("/") == 1:
            raise ValueError(f"Unexpected repo name {repo}")

    @classmethod
    def from_file(cls, filepath: PathLike) -> "Naming":
        """Create an instance from a filepath or a filename
        """
        name = str(filepath).split("/")[-1]
        ext = ".tar.gz"
        if name.endswith(ext):
            name = name[: -len(ext)]
        elif name.endswith(".txt"):
            name = name[:-4]
        else:
            raise ValueError(f"Unexpected extension: {filepath}")
        if name.count(",") != 1:
            raise ValueError(f"Unexpected file name {name}")
        return cls(name.replace(",", "/"))

    @property
    def failure(self) -> str:
        return self.repo.replace("/", ",") + ".txt"

    @property
    def success(self) -> str:
        return self.repo.replace("/", ",") + ".tar.gz"


class DownloadError(RuntimeError):
    pass


def download(
    repo: str, folder: PathLike = "", api_token: str = "", timeout: int = 1800
) -> Path:
    """Download the repo tarball in 2 different ways depending on the api_token:
    - empty string: uses the official API that provides the download path, without authentification
    - actual API token: uses the official API with authentification

    Note
    ----
    API tokens can be created through Settings / Developer settings / Fine-grained tokens / Generate
    https://github.com/settings/tokens?type=beta
    There are the "official" way to access the API with a rate limit of 5000 calls/hour

    Resources
    ---------
    - https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#download-a-repository-archive-tar
    - https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limits
    - watch-out for x-ratelimit: https://docs.github.com/en/rest/guides/best-practices-for-integrators?apiVersion=2022-11-28
    """
    naming = Naming(repo)
    folder = Path(folder).resolve().absolute()
    folder.mkdir(exist_ok=True)
    tarpath = folder / naming.success
    failpath = folder / naming.failure
    if failpath.exists():
        failpath.unlink()
    url = f"https://github.com/{repo}/tarball/master"  # non-identified non-api call
    # https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#download-a-repository-archive-tar
    headers = {}
    if api_token:  # use api call
        url = f"https://api.github.com/repos/{repo}/tarball"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {api_token}",
        }
    params = "".join(f'-H "{x}: {y}" ' for x, y in headers.items())
    # using curl is messier than using requests, but so far seemed much more robust
    command = rf"curl --retry 0 -L {params}{url} > {tarpath}"
    try:
        subprocess.run(
            command, shell=True, check=True, timeout=timeout, capture_output=True
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        string: str = e.stderr.decode("utf8")  # type: ignore
        failpath.write_text(string)
        raise DownloadError(f"Curl call {command!r} failed with {e}:\n{string}") from e
    #
    # find repository name / deal with errors (invalid tar)
    command = rf"tar -ztf {tarpath} | egrep '^[^/]+/?$'"
    try:
        out = subprocess.run(command, shell=True, check=True, capture_output=True)
        out.stdout.decode("utf8").rstrip("/ \n")
    except subprocess.CalledProcessError as e:
        tag = "{REPLACE-TAG] "
        try:
            content = tarpath.read_text()
        except UnicodeDecodeError:
            content = tag + "Could not read content"
        if not content.strip():
            content = tag + "No content was downloaded"
        for case in [
            "This repository is empty",
            "This repository is currently disabled",
        ]:
            if case in content:
                content = tag + case  # simplify because the text is way too long
        if content.startswith(tag):  # if we have to replace the content
            content = content[len(tag) :]
            tarpath.write_text(content)
        shutil.move(tarpath, failpath)
        raise DownloadError(f"Tar is corrupted: {content}") from e
    return tarpath


def postprocess_file(
    filepath: PathLike, folder: PathLike, check_license: bool = True
) -> Path:
    """Postprocess a downloaded file by removing big or binary files, and possibly
    check for licenses

    Parameters
    ----------
    filepath: PathLike
        file to postprocess
    folder: PathLike
        final folder to put the file into
    check_license: bool
        whether to look for licenses in the repo
        this is slow, but probably as slow as the limit rate we want to aim for
        BEWARE: this will load the license classifier, if you load it in the main
        thread, it will deadlock the workers :s

    Note
    ----
    - example of postprocessing impact for 724 tars: 9.3GB -> 1.8GB
    """
    filepath = Path(filepath)
    folder = Path(folder).resolve().absolute()
    folder.mkdir(exist_ok=True)
    naming = Naming.from_file(filepath)
    classifier: tp.Any = None
    # if failure file, just move it
    if filepath.name == naming.failure:
        outfile = folder / filepath.name
        if outfile != filepath:
            shutil.move(filepath, outfile)
        return outfile
    # remove any preexisting failure to start off clean
    failpath = folder / naming.failure
    if failpath.exists():
        failpath.unlink()
    if check_license:
        try:
            # pylint: disable=import-outside-toplevel
            from LicenseClassifier.classifier import LicenseClassifier

            classifier = LicenseClassifier()
            msg = "License classifier was loaded, it can deadlock workers"
        except (OSError, ImportError):
            msg = "License classifier not available (pip install golicense-classifier)"
        logger.info(msg)
    try:
        with temp_untar(filepath, replace=True) as tmp:
            metapath = tmp / "metadata.json"
            if metapath.exists():
                raise RuntimeError(
                    "Code needs to be updated to handle existing metadata"
                )
            content = list(tmp.iterdir())
            assert len(content) == 1
            to_remove = irrelevant_files(tmp, too_big=True, binaries=True)
            for fp in to_remove:
                if fp.exists():
                    fp.unlink()
            # check for licenses SLOOOW
            data: tp.Dict[str, tp.Any] = dict(
                name=naming.repo, extraction=time.strftime("%Y-%m-%d")
            )
            # assuming github format:
            data["commit"] = content[0].name.split("-")[-1]
            data["filtered_files"] = [
                str(fp.relative_to(content[0])) for fp in to_remove
            ]
            if classifier is not None:
                scanned = classifier.scan_directory(str(content[0]))["files"]
                licenses: tp.Dict[str, tp.Any] = {}
                for finfo in scanned:
                    path = str(Path(finfo["path"]).relative_to(content[0]))
                    for lic in finfo["licenses"]:
                        licenses.setdefault(lic["key"], []).append(path)
                data.update(
                    licenses=licenses, license_classifier="golicense-classifier"
                )
            with metapath.open("w") as f:
                json.dump(data, f, indent=4)
        outfile = folder / filepath.name
        if outfile != filepath:
            shutil.move(filepath, outfile)
        return outfile
    except (EOFError, OSError, tarfile.ReadError, DownloadError) as e:
        string = "Failed to untar file"
        filepath.unlink()
        failpath.write_text(f"{string}:\n{e}")
        raise DownloadError(string) from e


def get_rate_limit(api_token: tp.Optional[str] = None) -> tp.Dict[str, tp.Any]:
    """Returns the output of the rate-limit API request
    providing the current state of the rate limit for either the IP
    (api_token is None or "") or the user (valid api_token)
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if api_token is not None and api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    params = "".join(f'-H "{x}: {y}" ' for x, y in headers.items())
    command = rf"curl -v {params}https://api.github.com/rate_limit"
    try:
        out = subprocess.run(command, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Curl call {command!r} failed with:\n{e.stderr.decode('utf8')}"
        ) from e
    return json.loads(out.stdout)  # type: ignore


def irrelevant_files(
    folder: PathLike, too_big: bool = True, binaries: bool = True
) -> tp.List[Path]:
    """Returns irrelevant files from the folder

    Parameters
    ----------
    folder: str or Path
        folder to check
    too_big: bool
        finds files over 1MB as well as pdf, csv and json (which are a large amount of data but
        do not bring much)
    binaries: bool
        finds files with non-utf8 characters in the first 1,000 characters or so
        (from https://stackoverflow.com/questions/29516984/how-to-find-binary-files-in-a-directory)
    """
    folder = Path(folder)
    if not (too_big or binaries):
        raise ValueError("Either too_big or binaries should be True")
    if not folder.exists():
        raise ValueError(f"Folder {folder} does not exist")
    if not folder.is_dir():
        raise ValueError(f"{folder} is not a folder")
    # include list to make sure to avoid deleting important files
    include_list = {
        ".py",
        ".html",
        ".cpp",
        ".c",
        ".hpp",
        ".h",
        ".ipynb",
        ".java",
        ".cu",
    }
    include_list |= {".php", ".cs", ".vb", ".js", ".sql", ".asm", ".go", ".rs"}
    # clean big files
    fps = set()
    commands = []
    if too_big:
        commands.append("find . -type f -size +1M")
        # csv, json and some pdf are not identified as binaries and can be big while not bringing much
        commands.append(
            r"find . -type f \( -iname '*.csv' -o -iname '*.pdf' -o -iname '*.json' \)"
        )
    if binaries:  # or data
        # more effective than: grep -rIL .
        commands.append("find . -type f | perl -lne 'print if -B'")
    for command in commands:
        out = subprocess.check_output(command, cwd=folder, shell=True)
        splitted = [
            fp.strip("\n") for fp in re.split("\n./", out.decode("utf-8", "ignore"))
        ]
        tmp = [folder / fp for fp in splitted if fp]
        tmp = [x for x in tmp if x.exists() and x.is_file()]  # safety measure
        # some files do not "exist" for some reason, eg: veridu/veridu.github.io/article/Icon  (invisible last character)
        if "perl" in command:
            # keep empty files which can be useful for structure
            # (eg: __init__.py or py.typed)
            # and prevent from removing very common extensions
            tmp = [
                x for x in tmp if _safe_size(x) and x.suffix.lower() not in include_list
            ]
        fps |= set(tmp)
    return list(fps)


def _safe_size(path: Path, default: int = 0) -> int:
    try:
        return path.stat().st_size
    except OSError:
        # [Errno 36] File name too long (happened on ga4gh/server/README.rst
        return default


@contextlib.contextmanager
def temp_untar(
    tarpath: PathLike, replace: bool = False, allow_missing: bool = False
) -> tp.Generator[Path, None, None]:
    """Context manager providing a temporary folder with the context of the provided tar file

    Parameters
    ----------
    tarpath: Path
        path to the the tar file
    replace: bool
        if True, the tar file will be replaced with the possibly updated content
        of the folder
    allow_missing: bool
        if True and if replace is True, a file will be created if it does not exist
    """
    tarpath = Path(tarpath)
    targz = ".tar.gz"
    assert tarpath.name.endswith(targz)
    if not (allow_missing or tarpath.exists()):
        raise RuntimeError("File does not exist while allow_missing is False")
    if not (replace or tarpath.exists()):
        raise RuntimeError("File does not exist while replace is False")
    # use scratch if possible
    prefix: tp.Optional[str] = None
    tmp = "/scratch"
    if Path(tmp).exists():
        prefix = str(Path(tmp) / f"{getpass.getuser()}/tar_tmp") + "/"
        Path(prefix).mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=prefix) as tmp:
        tmppath = Path(tmp)
        # un-tar in the temporary directory
        if tarpath.exists():
            with tarfile.open(tarpath, "r:gz") as tar:
                try:
                    tar.extractall(tmp)
                except Exception as e:
                    raise DownloadError(f"Tar extraction failed with: {e}") from e
        yield tmppath
        # re-tar in the tar file
        if replace:
            if tarpath.exists():
                tarpath.unlink()  # delete to avoid corruption
            command = f"tar czf {tarpath} ."  # probably faster with subprocess
            subprocess.check_call(command, shell=True, cwd=tmp)
            # tar czf name_of_archive_file.tar.gz name_of_directory_to_tar
            # with tarfile.open(tarpath, "w:gz") as tar:
            #     for content in tmppath.iterdir():
            #         tar.add(content, arcname=content.relative_to(tmppath))


def filter_tar(tarpath: PathLike) -> None:
    """Removes big files and binary files from tar.gz files"""
    tarpath = Path(tarpath)
    with temp_untar(tarpath, replace=True) as tmp:
        # one at a time to be slighly (...) more efficient
        for fp in irrelevant_files(tmp, too_big=False, binaries=True):
            fp.unlink()
        for fp in irrelevant_files(tmp, too_big=True, binaries=False):
            fp.unlink()


def running_finished(
    jobs: JobDict, workers: int, wait_delay: float = 1.0
) -> tp.Tuple[JobDict, JobDict]:
    """From a dictionary of jobs, returns a dictionnary of the remaining
    jobs, and a dictionary of results.
    if workers < len(jobs) and the provided delay is strictly positive,
    this will wait until the number of running jobs is strictly below
    the number of workers

    Parameters
    ----------
    jobs: dict of jobs
        the dictionary of jobs
    workers: int
        maximum number of jobs we want to keep / the function will
        return if we reach a lower number
    wait_delay: float
        wait delay before rechecking if the jobs are over
    """
    assert workers > 0
    finished: JobDict = {}
    first = True
    # run at least once, and until there are fewer than "workers"
    # jobs if a strictly positive "wait_dealy is provided
    while first or (len(jobs) >= workers and wait_delay > 0.0):
        if not first:
            print("Waiting")
            time.sleep(wait_delay)
        first = False
        running: JobDict = {}
        for key, job in jobs.items():
            (finished if job.done() else running)[key] = job
        jobs = running
        # export results asap
    return jobs, finished
