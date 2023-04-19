import uuid
import typing as tp
import pickle
import json
import logging
from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)


def get_secs(time_string: str) -> int:
    """Converts strings formated as '7:14:05' or '1 day, 4:55:05'"""
    split = "days" if "days" in time_string else "day"
    parts = time_string.split(f" {split}, ")
    fmt = "%H:%M:%S"
    delta = datetime.strptime(parts[-1], fmt) - datetime.strptime("0:00:00", fmt)
    seconds = int(delta.total_seconds())
    if len(parts) > 1:
        assert parts[0].isdigit()
        seconds += 86400 * int(parts[0])
    return seconds


def parse_logs(path: tp.Union[str, Path]) -> tp.List[tp.Dict[str, tp.Any]]:
    path = Path(path)
    if not path.is_dir():
        raise ValueError("Please provide a valid xp folder")
    path = Path(path)
    name = int(path.name) if path.name.isdigit() else path.name
    base = dict(exp_id=name, exp_name=path.parent.name)
    # params
    params_path = path / "params.pkl"
    if not params_path.exists():
        raise RuntimeError(f"Missing params file {params_path}")
    with params_path.open("rb") as f:
        data = pickle.load(f).__dict__
    base.update(
        {
            x: y if isinstance(y, (str, int, float, bool)) or y is None else str(y)
            for x, y in data.items()
        }
    )
    useless = ["master_addr", "is_master", "master_port", "local_rank", "global_rank"]
    base = {x: y for x, y in base.items() if x not in useless}
    # logs
    log_path = path / "train.log"
    assert log_path.exists(), f"Missing log file {log_path}"
    with log_path.open("r") as f2:
        lines = [line.rstrip() for line in f2.readlines()]
    logs = []
    log_pattern = "__log__:"
    for line in lines:
        pos = line.find(log_pattern)
        if pos < 0:
            continue
        split = line.split(" - ")
        try:
            data = json.loads(line[pos + len(log_pattern) :])
        except Exception as e:
            logger.warning(f"Could not read json line: {e}")
            continue
        if len(data) == 1:  # TODO: remove
            continue
        assert len(split) == 4, split
        assert "seconds" not in data and "hours" not in data
        sec = get_secs(split[2])
        data.update(base, seconds=sec, hours=sec / 3600.0)
        logs.append(data)
    return logs


# def get_exp_ids(exp_names: tp.List[str]) -> tp.List[:
#     exp_ids = []
#     dump_paths = [Path(path) for path in DUMP_PATHS]
#     for exp_name in exp_names:
#         if exp_name.endswith('*') and 'evaluations' in exp_name:
#             folder = '/'.join(exp_name.split('/')[:-1])
#             sufix = exp_name.split('/')[-1][:-1]
#             tmp = [name for name in os.listdir(folder) if name.startswith(sufix) ]
#             exp_names += tmp
#     for exp_name in exp_names:
#         for dump_path in dump_paths:
#             current = []
#             if not (dump_path / exp_name).is_dir():
#                 continue
#             print("Looking into: %s" % os.path.join(dump_path, exp_name))
#             for exp_id in sorted(os.listdir(os.path.join(dump_path, exp_name))):
#                 if not os.path.isdir(os.path.join(dump_path, exp_name, exp_id)):
#                     print('"%s/%s" is not a directory' % (exp_name, exp_id))
#                     continue
#                 current.append((dump_path, exp_name, exp_id))
#             if current:
#                 print('%s - %s (%i)' % (dump_path, exp_name, len(current)))
#             exp_ids.extend(current)
#     print('Found %i experiments grouped in %i categories.' % (len(exp_ids), len(exp_names)))
#     return exp_ids
#
# def parse_experiments(exp_ids, overwrite):
#     for dump_path, exp_name, exp_id in exp_ids:
#         try:
#             exp_path = os.path.join(dump_path, exp_name, exp_id)
#             log_path = os.path.join(exp_path, 'train.log')
# #             if os.path.isfile(os.path.join(exp_path, 'train.log-2')):
# #                 log_path = os.path.join(exp_path, 'train.log-2')
#             params_path = os.path.join(exp_path, 'params.pkl')
#             if not os.path.isfile(log_path):
#                 print('No log file in %s' % exp_path)
#                 continue
#             if not os.path.isfile(params_path):
#                 print('No parameter file in %s' % exp_path)
#                 continue
#             with open(params_path, 'rb') as f:
#                 params = pickle.load(f).__dict__
#             if exp_id in experiments:
#                 if overwrite:
#                     del experiments[exp_id]
#                 else:
#                     assert False, exp_id
#             assert exp_id not in experiments
#             logs = parse_logs(log_path)
#             params = dict(params)
#             if 'name' not in params:
#                 params['name'] = exp_name
#             assert params['name'] == exp_name
#             # if 'gpu_id' in params:
#             #     del params['gpu_id']  # ignore the GPU ID
#             experiments[exp_id] = {
#                 'id': exp_id,
#                 'name': exp_name,
#                 'params' : params,
#                 'logs': logs
#             }
#         except Exception as e:
#             print("Failed %s - %s" % (exp_name, exp_id))
#             print(traceback.format_exc())
#     print('Parsed %i experiments.' % len(experiments))
#     return experiments


class STYLE:
    metrics = "badge badge-pill badge-primary"
    internal = "badge badge-pill badge-secondary"
    optim = "badge badge-pill badge-dark"
    model = "badge badge-pill badge-success"
    # "badge badge-pill badge-danger"
    # "badge badge-pill badge-warning"


def _set_style(exp: tp.Any) -> None:
    import hiplot as hip

    assert isinstance(exp, hip.Experiment)
    # Don't display `uid` and `from_uid` columns to the user
    cols = set(x for dp in exp.datapoints for x in dp.values.keys())
    losses = [x for x in cols if x.startswith("valid_") or x.startswith("test_")]
    internals = ["epoch", "exp_id", "exp_name", "hours", "seconds"]
    exp.display_data(hip.Displays.PARALLEL_PLOT).update(
        {
            "hide": ["uid", "from_uid"] + losses,
            "order": internals + [x for x in cols if x not in internals],
        }
    )
    # for the record, some more options:
    exp.display_data(hip.Displays.XY).update(
        {"lines_thickness": 1.4, "lines_opacity": 0.9}
    )
    exp.display_data(hip.Displays.XY).update({"axis_x": "epoch", "axis_y": "hours"})
    # colors
    styles = {}
    styles.update({name: STYLE.metrics for name in ["test_", "valid_"]})
    styles.update({name: STYLE.internal for name in internals})
    for col in cols:
        for start, style in styles.items():
            if col.startswith(start):
                exp.parameters_definition[col].label_css = style


def create_hiplot_experiment(uri: tp.Union[str, Path]) -> tp.Any:
    import hiplot as hip

    # one xp case
    uri = Path(uri)
    logs = parse_logs(uri)
    exp = hip.Experiment()
    xpuid = uuid.uuid4().hex[:4]
    prev_uid: tp.Optional[str] = None
    for k, xp in enumerate(logs):
        ptuid = uuid.uuid4().hex[:4]
        dp = hip.Datapoint(  # type: ignore
            uid=f"{xpuid}_{ptuid}_{k}", from_uid=prev_uid, values=xp,
        )
        prev_uid = dp.uid
        exp.datapoints.append(dp)
    _set_style(exp)
    return exp


def load(uri: str) -> tp.Any:
    """Loader for hiplot
    Running:
    python -m hiplot codegen_sources.utils.hiplog.load --port=XXXX
    will run an hiplot server in which you can past one (or more) log paths
    to plot them
    Note
    ----
    if you install bm first: "pip install -e ."
    you can simplify to:
    hiplot codegen_sources.utils.hiplog.load --port=XXXX
    Then either provide the folder of the experiments in the freeform,
    or their parent directory, so that all subfolders will be parsed for logs.
    """
    import hiplot as hip

    tag = "recursive:"
    if uri.startswith("#"):  # deactivate a line
        return hip.Experiment()
    if uri.startswith(tag):
        folder = Path(uri[len(tag) :])
        exps = []
        for path in folder.rglob("params.pkl"):
            if path.with_name("train.log").exists():
                exps.append(create_hiplot_experiment(path.parent))
        exp = hip.Experiment.merge({str(k): xp for k, xp in enumerate(exps)})
        for dp in exp.datapoints:
            dp.values["#recursive"] = str(folder)
        _set_style(exp)
        return exp

    # one experiment
    return create_hiplot_experiment(uri)
