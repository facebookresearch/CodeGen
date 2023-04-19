# import time
# import datetime
# import submitit
# from pathlib import Path
# import git
# import nevergrad as ng
# from . import runner
#
#
# # # Other option:
#
#
# def main() -> None:
#     print(f"It is {datetime.datetime.now().isoformat()}")
#     base_folder = Path("/checkpoint/jrapin/ca/xps/autorun/")
#     base_folder.mkdir(exist_ok=True, parents=True)
#     code_folder = base_folder / "code"
#
#     if not code_folder.exists():
#         repo = git.Repo(Path())
#         repo.clone(code_folder)
#         repo2 = git.Repo(code_folder)
#         repo2.remotes.origin.set_url(repo.remotes.origin.url)
#
#     repo = git.Repo(code_folder)
#     sha = repo.head.object.hexsha
#     assert repo.remotes.origin.exists()
#     repo.git.reset("--hard")  # blast any current changes
#     repo.heads.main.checkout()  # ensure main is checked out
#     repo.git.reset("--hard")  # blast any changes there (only if it wasn't checked out)
#     repo.git.clean("-xdf")  # remove any extra non-tracked files (.pyc, etc)
#     repo.remotes.origin.pull()  # pull in the changes from the remote
#     # repo.heads.main.
#     # repo.git.pull("origin", "main")
#     # repo.git.merge("origin/main")
#     # print(repo.head.reference)  # -> main
#     # # repo.git.checkout("main")
#     # # repo.remotes["origin"].fetch()
#     # # repo.git.reset("--hard", "origin/main")
#     # repo.git.pull("origin", "main")  # safer to fetch and reset hard
#     sha2 = repo.head.object.hexsha
#     print(f"Last commit: {repo.head.object.message.strip()}")
#     if sha == sha2:
#         print("Nothing new")
#         return
#
#     base_params = {
#         "experiment": "autorun",
#         "agent": "fb_ddpg",
#         "use_hiplog": 1,
#         "use_tb": 1,
#         "num_train_episodes": 1200,
#         "agent.lr": ng.p.Scalar(lower=1e-5, upper=2e-4),
#         "snapshot_at": [],
#     }
#     date = datetime.date.today().isoformat()
#     executor = submitit.AutoExecutor(folder=base_folder / date / "%j")
#     executor.update_parameters(
#         timeout_min=6 * 60,
#         slurm_partition="scavenge",
#         gpus_per_node=1,
#         cpus_per_task=6,
#         name="url_autorun",
#     )
#     # hp = runner.HydraEntryPoint(base_folder / "code" / "url_benchmark" / "anytrain.py")
#     # budget = 2
#     # num_workers = budget
#     # cases = [
#     #     {"task": "walker_walk", "goal_space": "simplified_walker"},
#     #     {"task": "quadruped_walk", "goal_space": "simplified_quadruped"},
#     # ]
#     # with executor.batch():
#     #     for other_params in cases:
#     #         param = ng.p.Instrumentation(**{**base_params, **other_params})
#     #         optim = ng.optimizers.RandomSearch(param, budget=budget, num_workers=num_workers)
#     #         for _ in range(budget):
#     #             executor.submit(hp.validated(**param.kwargs), **optim.ask().kwargs)
#     # print(f"Launched on {sha2}")
#
#
# if __name__ == "__main__":
#     while True:
#         main()
#         time.sleep(60 * 60 * 16)
