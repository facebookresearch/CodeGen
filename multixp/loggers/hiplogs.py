import functools
import dataclasses
import collections
from collections import abc
from concurrent import futures
import time
import uuid
import json
import typing as tp
import logging
from datetime import datetime
import subprocess
from pathlib import Path
import omegaconf
import psutil

try:
    from typing import Protocol
except ImportError:
    # backward compatible
    from typing_extensions import Protocol  # type: ignore

import numpy as np


# pylint: disable=import-outside-toplevel


START_LINE = "# Hiplot logs"
logger: logging.Logger = logging.getLogger(__name__)
Hiplotable = tp.Union[bool, int, float, str, np.float_, np.int_, Path]


class _StatCall(Protocol):
    def __call__(self, **kwargs: float) -> "HipLog":
        ...


class HipLogfileError(RuntimeError):
    pass


class STYLE:  # pylint: disable=too-few-public-methods
    metrics = "badge badge-pill badge-primary"
    internal = "badge badge-pill badge-secondary"
    optim = "badge badge-pill badge-dark"
    model = "badge badge-pill badge-success"
    other = "badge badge-pill badge-danger"
    # "badge badge-pill badge-warning"


def _set_style(exp: tp.Any) -> None:
    import hiplot as hip

    assert isinstance(exp, hip.Experiment)
    # Don't display `uid` and `from_uid` columns to the user
    cols = set(x for dp in exp.datapoints for x in dp.values.keys())
    internals = [
        "workdir",
        "step",
        "cg:epoch",
        "train/epoch",
        "experiment",
    ]
    internals.extend([col for col in cols if col.startswith("#")])
    hidden = [x for x in cols if x.startswith(("valid/", "train/"))]
    important = [
        x
        for x in hidden
        if any(
            y in x for y in ("match", "epoch", "loss", "valid/pred", "train/lr", "_acc")
        )
        and "per_batch" not in x
        and "/batch" not in x
    ]
    hidden = [x for x in hidden if x not in important]
    exp.display_data(hip.Displays.PARALLEL_PLOT).update(
        {"hide": ["uid", "from_uid"] + hidden}
    )
    # for the record, some more options:
    exp.display_data(hip.Displays.XY).update(
        {"lines_thickness": 1.4, "lines_opacity": 0.9}
    )
    exp.display_data(hip.Displays.XY).update(
        {"axis_x": "step", "axis_y": "valid/exact_matches"}
    )
    # colors
    styles = {}
    # styles.update(
    #     {
    #         name: STYLE.metrics
    #         for name in cols
    #         if name.startswith(("valid/", "train/"))
    #         and name not in important
    #     }
    # )
    styles.update({name: STYLE.metrics for name in important})
    styles.update({name: STYLE.internal for name in internals})
    styles["experiment"] = STYLE.other
    for col in cols:
        for start, style in styles.items():
            if col.startswith(start):
                exp.parameters_definition[col].label_css = style


def load(uri: tp.Union[Path, str], step: int = 1) -> tp.Any:
    """Loader for hiplot
    Running:
    python -m hiplot controllable_agent.hiplogs..load --port=XXXX
    will run an hiplot server in which you can past one (or more) log paths
    to plot them
    Note
    ----
    if you install first: "pip install -e ."
    you can simplify to:
    hiplot xxxx.load --port=XXXX
    Then either provide the folder of the experiments in the freeform,
    or their parent directory, so that all subfolders will be parsed for logs.
    """
    import hiplot as hip

    uri = Path(uri)
    if str(uri).startswith("#"):  # deactivate a line
        return hip.Experiment()
    assert uri.is_dir(), f"uri should be a valid directory, got {uri}"
    jobs = []
    hloggers = list(HipLog.find_in_folder(uri))
    if len(hloggers) > 1:  # remove test ones
        hloggers = [
            hl for hl in hloggers if "data/mockpretrain" not in str(hl._filepath)
        ]
    with futures.ProcessPoolExecutor() as executor:
        jobs = [executor.submit(hlog.to_hiplot_experiment, step) for hlog in hloggers]
    exps = [j.result() for j in jobs]
    exp = hip.Experiment.merge({str(k): xp for k, xp in enumerate(exps)})
    _set_style(exp)
    return exp


def _sanitize(value: tp.Any) -> tp.Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.generic):
        value = value.item()
    return value


class HipLog:
    """Simple object for logging hiplot compatible content
    Parameters
    ----------
    filepath: str or Path
        path to the logfile. It will be created if it does not exist, otherwise
        data will be appended to it.
    Usage
    -----
    hiplogs are not mutable, adding content is done through
    `with_content` and creates a new instance. This way, you can prefill
    some content, then use the object to add more content and write.
    Example
    -------
    hiplog = hiplogs.HipLog(filepath)
    hiplog = hiplog.with_content(shared_key=12)
    hiplog.write()  # writes only {"shared_key": 12}
    hiplog.with_content(hello="world").write()  # writes shared_key and hello
    # writes shared_key and something
    hiplog.with_content(something="blublu").write()
    """

    def __init__(self, filepath: tp.Union[Path, str]) -> None:
        self._filepath = Path(filepath)
        if self._filepath.suffix not in (".txt", ".log"):
            raise ValueError("Filepath must have .txt or .log as extension")
        self._content: tp.Dict[str, tp.Any] = {
            "#start_time": f"{datetime.now():%Y-%m-%d %H:%M}"
        }
        self._floats: tp.Dict[str, tp.List[float]] = collections.defaultdict(list)
        self._stats: tp.Dict[str, tp.Tuple[str, ...]] = {}
        self._reloaded = 0
        try:
            self._filepath.parent.mkdir(parents=True, exist_ok=True)
            if not self._filepath.exists():
                logger.info(f"Starting json log file at {self._filepath}")
                self._filepath.write_text(START_LINE + " v1\n", encoding="utf8")
        except Exception as e:  # pylint: disable=broad-except
            string = f"Failing to log data to json: {e}"
            logger.warning(string)
        try:
            import submitit

            self._content["#job_id"] = submitit.JobEnvironment().job_id
        except Exception:  # pylint: disable=broad-except
            pass
        data = self.read()
        if data:
            self._reloaded = data[-1].get("#reloaded", -1) + 1  # type: ignore

    @property
    def num_reloaded(self) -> int:
        return self._reloaded

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}({self._filepath})"

    @classmethod
    def find_in_folder(
        cls, folder: tp.Union[str, Path], recursive: bool = True
    ) -> tp.Iterator["HipLog"]:
        """Instantiate all hiplog instances from the folder or subfolders

        Parameters
        ----------
        folder: str/Path
            folder to look into
        recursive: bool
            instantiate all hiplog logs recursively

        Yields
        ------
        HipLog
            hiplog instance
        """
        folder = Path(folder)
        for suffix in (".txt", ".log"):
            iterator = (folder.rglob if recursive else folder.glob)("*" + suffix)
            for fp in iterator:
                if fp.suffix in (".log", ".txt"):
                    with fp.open("r", encoding="utf8") as f:
                        is_hiplog = START_LINE in f.readline()
                    if is_hiplog:
                        yield cls(fp)

    def __call__(self, **kwargs: Hiplotable) -> "HipLog":
        sanitized = {x: _sanitize(y) for x, y in kwargs.items()}
        self._content.update(sanitized)
        return self

    def with_stats(self, *stats: tp.Sequence[str]) -> _StatCall:
        return functools.partial(self._with_stats, tuple(stats))

    def _with_stats(
        self, _internal_name_stats: tp.Tuple[str, ...], **kwargs: float
    ) -> "HipLog":
        for key, val in kwargs.items():
            self._stats[key] = _internal_name_stats  # overridden by last call
            self._floats[key].append(float(val))
        return self

    def read(self, step: int = 1) -> tp.List[tp.Dict[str, Hiplotable]]:
        """Returns the data recorded through the logger

        Parameter
        ---------
        step: int
            step for decimating the data if too big

        Returns
        -------
        list of dict
            all the timepoints. Data from past timepoints are used if not
            provided in newer timepoints (eg: initial hyperparameters are
            passed to all timepoints)
        """
        with self._filepath.open("r", encoding="utf8") as f:
            lines = f.readlines()
        if lines and not lines[0].startswith(START_LINE):
            raise HipLogfileError(
                f"Did not recognize first line: {lines[0]!r} instead of {START_LINE!r}"
            )
        data: tp.List[tp.Dict[str, Hiplotable]] = []
        last = {}
        for k, line in enumerate(lines):
            if not line.startswith("#"):
                line_dict = json.loads(line.strip())
                last.update(line_dict)
                if not k % step:
                    data.append(dict(last))
        return data

    def last_line(self) -> tp.Dict[str, Hiplotable]:
        data = self.read()
        return {} if not data else data[-1]

    @property
    def content(self) -> tp.Dict[str, Hiplotable]:
        return dict(self._content)

    def _export_floats(self) -> tp.Dict[str, float]:
        out: tp.Dict[str, float] = {}
        for key, vals in self._floats.items():
            for stat in self._stats[key]:
                out[f"{key}#{stat}"] = getattr(np, stat)(vals)
        return out

    def write(self) -> None:
        # avoid as much as possible any disruption
        self._content["#now"] = f"{datetime.now():%Y-%m-%d %H:%M}"
        self._content["#time"] = time.time()
        self._content["#reloaded"] = self._reloaded
        mem = psutil.virtual_memory()
        gb = float(1024 ** 3)
        self._content["#mem/RAM/used"] = mem.used / gb
        self._content["#mem/RAM/avail"] = mem.available / gb
        self._content.update(self._export_floats())
        if not self._filepath.exists():
            return  # initialization failed, can't do anything more
        try:
            string = json.dumps(self._content)
        except Exception as e:  # pylint: disable=broad-except
            string = f"Failing to write data to json: {e}"
            logger.warning(string)
            return  # can't be json-ed, stop there
        # if it reaches here, it should be safe to write
        with self._filepath.open("a", encoding="utf8") as f:
            f.write(string + "\n")
        self._content.clear()
        self._floats.clear()
        self._stats.clear()

    def flattened(self, data: tp.Any) -> "HipLog":
        """Flattens a structured configuration and adds it to the content"""
        flat = flatten(data)
        self(**flat)
        return self

    def to_hiplot_experiment(self, step: int = 1) -> tp.Any:
        """Returns the Experiment recorded  through the logger

        Parameter
        ---------
        step: int
            step for decimating the data if too big

        Returns
        -------
        Experiment
            Hiplot Experiment instance containing the logger data
        """
        import hiplot as hip

        prev_uid: tp.Optional[str] = None
        exp = hip.Experiment()
        name = uuid.uuid4().hex[:8]
        rename = {
            "valid/GPU/mem/max": "#mem/GPU/max",
            "#RAM/avail": "#mem/RAM/avail",
            "#RAM/used": "#mem/RAM/used",
        }
        all_data = self.read(step=step)
        if all_data:
            for key in all_data[-1]:
                if "_per_" in key:
                    rename[key] = key.replace("_per_", "/")
        for k, data in enumerate(all_data):
            # updata field names
            for key, new_key in rename.items():
                if key in data:
                    data[new_key] = data.pop(key)
            # update the displayed name to something readable
            if not k:
                xp = data.get("experiment", "#UNKNOWN#")
                job_id = data.get("#job_id", name)
                name = f"{xp} / {job_id}"
            # try to match epoch in cg
            step: int = data.get("step", 0)  # type: ignore
            data["cg:epoch"] = 32.0 / 150000 * step
            if not (data.get("#mem/GPU/max", 0) < 128):  # type: ignore
                data["#mem/GPU/max"] = np.nan  # temporary fix
            dp = hip.Datapoint(
                uid=f"{name} / {k}", from_uid=prev_uid, values=data,  # type: ignore
            )
            prev_uid = dp.uid
            exp.datapoints.append(dp)
        _set_style(exp)
        logger.info("Finished loading %s", self._filepath)
        return exp


def flatten(data: tp.Any, sep: str = "/") -> tp.Dict[str, Hiplotable]:  # type: ignore
    output: tp.Dict[str, Hiplotable] = {}
    if dataclasses.is_dataclass(data):
        output[""] = data.__class__.__name__
        data = dataclasses.asdict(data)
    if isinstance(data, abc.Mapping):
        for x in data:
            try:
                y = data[x]
            except omegaconf.errors.MissingMandatoryValue:
                continue
            if isinstance(y, abc.Mapping) or dataclasses.is_dataclass(y):
                content = flatten(y)
                output.update(
                    {f"{x}{sep}{x2}".rstrip(sep): y2 for x2, y2 in content.items()}
                )
            elif isinstance(y, abc.Sequence) and not isinstance(y, str):
                # ignoring weird structures
                if y and isinstance(y[0], (int, float, np.int_, np.float_, str)):
                    output[x] = ",".join(str(z) for z in y)
            elif isinstance(y, (int, float, np.float_, np.int_, str)):
                output[x] = y
    return output


def repository_information() -> tp.Dict[str, str]:
    commands = {
        "commit": "git rev-parse --short HEAD",
        "branch": "git rev-parse --abbrev-ref HEAD",
        "closest_ir_proj": "git rev-parse --short IR_project",
    }
    here = Path(__file__).parent
    output: tp.Dict[str, str] = {}
    for name, command in commands.items():
        try:
            output[name] = (
                subprocess.check_output(command.split(), shell=False, cwd=here)
                .strip()
                .decode()
            )
        except Exception:  # pylint: disable=broad-except
            pass
    return output
