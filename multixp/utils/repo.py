import re
import copy
import subprocess
import dataclasses
import collections
import typing as tp
from pathlib import Path
from datetime import datetime


# permissive licenses for LicenseClassifier
PERMISSIVE = (
    "apache-2.0",
    "bsd-simplified",
    "clear-bsd",
    "bsd-3-clause-sun",
    "bsd-3-clause-sun",
    "boost-1.0",
    "mit",
    "mpl-2.0-no-copyleft-exception",
    "cc0-1.0",
    "isc",
)


class Repo:
    def __init__(self, identification: str) -> None:
        """Providing an id as a github repo or a full path,
        extracts relevant information and allows cloning
        (ssh for github, https for others)
        """
        self._input = identification
        identification = identification.strip(" /")
        identification = identification.replace("http://", "https://")
        self.address = ""
        if not identification.startswith("https://"):
            if identification.count("/") == 1:
                self.address = f"https://github.com/{identification}"
        else:
            self.address = identification
        if "github" in self.address and "/tree/" in self.address:
            self.address = self.address.split("/tree/", maxsplit=1)[0]
        if any(x in identification for x in ", ") or self.address.endswith("."):
            self.address = ""
        if self.address.count("/") < 4:
            self.address = ""

    @property
    def repo(self) -> str:
        """Eg: facebookresearch/nevergrad
        """
        if not self.address:
            raise ValueError(f"Invalid repo identified as {self._input}")
        right = self.address.split("//", maxsplit=1)[1]
        return right.split("/", maxsplit=1)[1]

    @property
    def name(self) -> str:
        """Eg: nevergrad
        """
        return self.repo.split("/")[-1]

    @property
    def foldername(self) -> str:
        """Eg: nevergrad
        """
        return self.repo.replace("/", ",")

    @property
    def clone_address(self) -> str:
        """Eg: git@github.com:facebookresearch/nevergrad
        """
        if "github" in self.address:
            right = self.address.split("//", maxsplit=1)[1]
            domain = right.split("/", maxsplit=1)[0]
            return f"git@{domain}:{self.repo}.git"
        # other cases use https
        gaddress = self.address
        if "https://git.sr.ht" not in self.address:
            gaddress += ".git"
        return gaddress

    def clone(self, folder: Path, force: bool = False) -> None:
        """Clones the repo to folder / name
        """
        if not force and (folder / self.name).exists():
            return
        try:
            proc = subprocess.run(
                ["git", "clone", self.clone_address, self.foldername],
                cwd=folder,
                capture_output=True,
                timeout=500,
                check=True,
            )
            proc.check_returncode()
        except Exception as e:
            print(e)
            # err = proc.stderr.decode("utf8")
            raise RuntimeError(e)

    def __repr__(self) -> str:
        return f"Repo({self._input!r})"


class RepoInfo:
    def __init__(self, folder: tp.Union[Path, str]) -> None:
        self.folder = Path(folder)
        if not self.folder.is_dir():
            self.folder = self.folder.parent
        # move to top level if no ".git"
        if not (self.folder / ".git").exists():
            self.folder = Path(self._call("git rev-parse --show-toplevel"))

    @property
    def origin(self) -> str:
        out = self._call("git remote -v")
        return out.split(maxsplit=2)[1]

    @property
    def link(self) -> str:
        out = self.origin
        tag = "git@"
        if out.startswith(tag):
            string = self.origin[len(tag) :]
            domain, repo = string.split(":", maxsplit=1)
            out = f"https://{domain}/{repo}"
        tag = ".git"
        if out.endswith(tag):
            out = out[: -len(tag)]
        return out

    def get_licenses(self) -> tp.Set[str]:
        from LicenseClassifier.classifier import LicenseClassifier

        classifier = LicenseClassifier()
        res = [
            x
            for y in classifier.scan_directory(str(self.folder))["files"]
            for x in y["licenses"]
        ]
        return {r["key"] for r in res}

    def _grep_mypy(self) -> tp.List[str]:
        out = self._call(
            r'grep -I -r --exclude-dir=".git" --exclude-dir="__pycache__" --exclude \*.py "mypy " .',
            default="",
        ).splitlines()
        out = [
            x for x in out if not any(y in x for y in ("==", ">=", "<="))
        ]  # those are requirements
        return out

    def _find_pyfiles(self, typed: bool = False) -> tp.Set[str]:
        if not typed:
            return set(
                self._call(
                    r'find . -type f -name "*.py" -not -path "*/\.*" -not -path "*__pycache__*"'
                ).splitlines()
            )
        out = self._call(
            r'grep -r -I --exclude-dir=".git" --exclude-dir="__pycache__" --include \*.py "\->\|from typing\|import typing" .',
            default="",
        )
        return {x.split(":", maxsplit=1)[0].strip() for x in out.splitlines()}

    def _find_site_packages(self) -> tp.List[Path]:
        """Find site packages containing .py files avoid leakage in test
        """
        folders = []
        out = self._call(
            r'find . -name "site-packages" -not -path "*/\.*" -not -path "*__pycache__*"'
        )
        for subfold in out.splitlines():
            check = self.folder / subfold.strip()
            if any(check.rglob("*.py")):
                folders.append(check)
        return folders

    def extract_type_info(self) -> tp.Dict[str, tp.Any]:
        info: tp.Dict[str, tp.Any] = dict(folder_name=self.folder.name, link=self.link)
        # number of non-init python files
        pyfiles = self._find_pyfiles(typed=False)
        info["num_py"] = len(pyfiles)
        info["num_noninit_py"] = sum(not x.endswith("__init__.py") for x in pyfiles)
        info["num_pyi"] = int(
            self._call(
                r'find . -type f -name "*.pyi" -not -path "*/\.*" -not -path "*__pycache__*" | wc -l'
            )
        )
        # number of typed pyhon files (approximately)
        pyfiles = self._find_pyfiles(typed=True)
        info["num_typed_py"] = len(pyfiles)
        info["num_noninit_typed_py"] = sum(
            not x.endswith("__init__.py") for x in pyfiles
        )
        info["num_mypy_ini"] = int(
            self._call(
                r'find . -type f -name "*mypy.ini" -not -path "*/\.git*" -not -path "*__pycache__*" | wc -l'
            )
        )
        for name in ["pyproject.toml", "setup.cfg"]:
            conf = self.folder / name
            if conf.exists():
                content = conf.read_text()
                if any(x in content for x in ["[mypy]", "[tools.mypy]"]):
                    info["num_mypy_ini"] += 1
        if not info["num_mypy_ini"]:
            # find for some weird config like in openstack/cinder
            info["num_mypy_ini"] += any(
                "mypy" in fp.name for fp in self.folder.iterdir()
            )
        info["num_py_dot_typed"] = int(
            self._call(
                r'find . -type f -name "py.typed" -not -path "*/\.*" -not -path "*__pycache__*" | wc -l'
            )
        )
        info["num_mypy_calls"] = len(self._grep_mypy())
        info["site_packages"] = len(self._find_site_packages())
        info["pycache"] = int(
            self._call(r'find . -name "__pycache__" -not -path "*/\.*" | wc -l')
        )
        licenses = self.get_licenses()
        info["licenses"] = ",".join(licenses)
        info["permissive"] = bool(licenses) and not bool(
            licenses - set(PERMISSIVE)
        )  # don't keep code with no license
        return info

    def _call(self, string: str, default: tp.Optional[str] = None) -> str:
        parts = string.split()
        try:
            out = (
                subprocess.check_output(" ".join(parts), shell=True, cwd=self.folder)
                .decode("utf8")
                .strip()
            )
        except Exception as e:
            if isinstance(default, str):
                return default
            raise RuntimeError(f"Failed on {self.folder}") from e
        return out


def flatten(data):
    for x, y in data.items():
        if isinstance(y, dict):
            for x2, y2 in flatten(y):
                yield f"{x}.{x2}", y2
        elif isinstance(y, list):
            for x2, y2 in flatten({str(k): yl for k, yl in enumerate(y)}):
                yield f"{x}.{x2}", y2
        else:
            yield x, y


string = (
    "update to github for the and add https from in of com this with fix by on readme is commit merge "
    "you new code be version if or no it details updated release updates dependency that summary "
    "been any main view are issues more your as remove notes set bump use actions added compare error have "
    "releases bug docs options upgrade can has at an config features ignore close when changes will "
    "block fixes rebase manually automerge properties package also example language build "
    "dependencies commits name generated default don page"
)
COMMON = set(string.split())  # those common names are not helpful


@dataclasses.dataclass
class RepoStats:
    """Aggregator of repo statistics from gharchive events"""

    name: str = ""
    first_time: datetime = dataclasses.field(default_factory=datetime.now)
    last_time: datetime = dataclasses.field(
        default_factory=lambda: datetime.fromisoformat("1900-01-01")
    )
    numbers: tp.Dict[str, int] = dataclasses.field(
        default_factory=lambda: collections.defaultdict(int)
    )
    events: tp.Dict[str, int] = dataclasses.field(
        default_factory=lambda: collections.defaultdict(int)
    )
    words: tp.Set[str] = dataclasses.field(default_factory=set)
    licenses: tp.Set[str] = dataclasses.field(default_factory=set)
    languages: tp.Set[str] = dataclasses.field(default_factory=set)
    forkees: tp.Set[str] = dataclasses.field(default_factory=set)
    users: tp.Set[int] = dataclasses.field(default_factory=set)
    paths: tp.Set[str] = dataclasses.field(default_factory=set)

    def add_time(self, time_: tp.Union[datetime, str]) -> None:
        if isinstance(time_, str):
            # with or without final Z
            if time_.endswith("Z"):
                time_ = time_[:-1]
            time_ = datetime.fromisoformat(time_)
        self.first_time = min(time_, self.first_time)
        self.last_time = max(time_, self.last_time)

    @classmethod
    def from_event(cls, info: tp.Dict[str, tp.Any]) -> "RepoStats":
        repo = info["repo"]["name"]
        out = cls(name=repo)
        out.events[info["type"]] = 1
        checked = {
            "CreateEvent",
            "PushEvent",
            "IssueCommentEvent",
            "PullRequestReviewCommentEvent",
            "PullRequestEvent",
            "ForkEvent",
            "WatchEvent",
            "DeleteEvent",
            "IssuesEvent",
            "CommitCommentEvent",
            "GollumEvent",
            "ReleaseEvent",
            "MemberEvent",
            "PublicEvent",
            "PullRequestReviewEvent",
            "FollowEvent",
        }
        if info["type"] not in checked:
            raise ValueError(f"Unknown event type {info['type']}")
        strings = []
        interesting = {
            f".{s1}{s2}"
            for s2 in ("", "_count")
            for s1 in ["stargazers", "watchers", "forks", "open_issues"]
        }
        interesting.add(".size")
        flattened = dict(flatten(info))
        text_fields = {
            ".description",
            ".title",
            ".body",
            ".name",
            ".message",
            ".summary",
        }
        out.add_time(info["created_at"])
        for field, content in flattened.items():
            splitted = field.split(".")
            last_part = "." + splitted[-1]
            if last_part in interesting and isinstance(content, int):
                if last_part == ".size" and not field.endswith("repo.size"):
                    continue
                if splitted[-2] == "repo":
                    ref = flattened[".".join(splitted[:-1] + ["full_name"])]
                    if repo != ref:
                        continue  # referring to another repo
                name = splitted[-1].replace("_count", "")
                out.numbers[name] = max(out.numbers[name], content)
            elif last_part in text_fields:
                if any(x in field for x in ("author.name", "repo.name")):
                    continue
                if isinstance(content, str):
                    strings.append(content)
            elif last_part == ".language":
                if isinstance(content, str):
                    out.languages.add(content)
            elif last_part == ".path":
                if isinstance(content, str):
                    out.paths.add(content)
            elif field.endswith(
                ("forkee.full_name", ".id", "license_.pdx_id")
            ):  # pack into one big endswith for optim
                if field.endswith(
                    ("actor.id", ".user.id", ".member.id")
                ) and isinstance(content, int):
                    out.users.add(content)
                elif field.endswith("forkee.full_name"):
                    if isinstance(content, str):
                        out.forkees.add(content)
                elif field.endswith("license.spdx_id"):
                    if isinstance(content, str):
                        out.licenses.add(content)
        words = set(
            x.lower()
            for x in re.findall(r"\w+", " ".join(strings))
            if not x.isnumeric()
        )
        out.words |= {
            x for x in words if len(x) > 1 and len(x) <= 24 and x not in COMMON
        }
        return out

    def __iadd__(self, other: "RepoStats") -> "RepoStats":
        if not other.name:
            raise ValueError("Only non empty infos can be right added")
        if not self.name:
            if self.users:
                raise RuntimeError("No name but data anyway, something went ugly")
            return other
        out = other
        if self.name != other.name:
            raise ValueError("Only same repos can be added")
        data = {
            field.name: getattr(self, field.name) for field in dataclasses.fields(self)
        }
        self._fill_with_data(out, data)
        return out

    def __add__(self, other: "RepoStats") -> "RepoStats":
        out = copy.deepcopy(other)
        out += other
        return out

    @staticmethod
    def _fill_with_data(out: "RepoStats", data: tp.Dict[str, tp.Any]) -> None:
        # convenient to have a function, for profiling purpose
        for name, content in data.items():
            val = getattr(out, name)
            if isinstance(content, datetime):
                out.add_time(content)
            elif isinstance(content, set):
                # setattr(out, name, content.union(val))
                val.update(content)
            elif isinstance(content, int):
                setattr(out, name, max(content, val))
            elif isinstance(content, dict):
                for name2, count in content.items():
                    # sum or max depending on field
                    if name == "numbers":
                        val[name2] = max(val[name2], count)
                    else:
                        val[name2] += count
            elif name != "name":
                raise RuntimeError(f"Weird field {name}")

    @classmethod
    def from_json(cls, data: tp.Dict[str, tp.Any]) -> "RepoStats":
        out = cls()
        if "words" not in data:
            raise ValueError("Missing words field in data")
        for key, val in data.items():
            current = getattr(out, key)
            if isinstance(current, (dict, set)):
                current.update(val)
            elif isinstance(current, datetime):
                out.add_time(val)
            elif isinstance(current, str):
                setattr(out, key, val)
            else:
                raise TypeError(f"Unexpected type {type(current)} for {key}")
        return out

    def export(self) -> tp.Dict[str, tp.Any]:
        data = {
            field.name: getattr(self, field.name) for field in dataclasses.fields(self)
        }
        data = {x: y if not isinstance(y, set) else sorted(y) for x, y in data.items()}
        data = {
            x: y if not isinstance(y, datetime) else y.isoformat()
            for x, y in data.items()
        }
        if not data:
            raise RuntimeError(f"All fields were filtered out from {self}")
        return data
